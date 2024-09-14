from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import time
import math
from typing import List, Dict, Tuple
from map_generation import load_final_map_as_grid
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI()

# Mount a static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Game state
game_state: Dict[str, Dict[str, Dict]] = {"ships": {}}

# Load map data (500x500 list of lists with 1 for land, 0 for water)
map_data: List[List[int]] = load_final_map_as_grid()

MAP_WIDTH = 500
MAP_HEIGHT = 500

# WebSocket connections
active_connections: Dict[str, WebSocket] = {}


class ShipUpdate(BaseModel):
    ship_id: str
    value: float


class ShipUpdateRequest(BaseModel):
    ship_id: str
    key: str
    value: float


@app.websocket("/ws/game")
async def game_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send the entire game state
            await websocket.send_json(game_state)
            await asyncio.sleep(0.01)  # Update every 50ms
    except WebSocketDisconnect:
        logger.info("Game WebSocket disconnected")


@app.websocket("/ws/{ship_id}")
async def ship_websocket_endpoint(websocket: WebSocket, ship_id: str):
    await websocket.accept()
    active_connections[ship_id] = websocket
    try:
        while True:
            # Send full game state
            await websocket.send_json(game_state)

            # Receive control updates
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.05)
                if "heading" in data:
                    await update_heading(
                        ShipUpdate(ship_id=ship_id, value=data["heading"])
                    )
                elif "speed" in data:
                    await update_speed(ShipUpdate(ship_id=ship_id, value=data["speed"]))
            except asyncio.TimeoutError:
                pass  # No input received, continue to next iteration

            await asyncio.sleep(0.01)  # Update every 50ms
    except WebSocketDisconnect:
        logger.info(f"Ship WebSocket disconnected for ship {ship_id}")
        del active_connections[ship_id]


def calculate_new_position(
    x: float, y: float, heading: float, speed: float, delta_time: float
) -> Tuple[float, float]:
    radians = math.radians(heading)
    dx = speed * math.sin(radians) * delta_time
    dy = (
        -speed * math.cos(radians) * delta_time
    )  # Negative because y increases downwards
    new_x = (x + dx) % MAP_WIDTH
    new_y = (y + dy) % MAP_HEIGHT
    return (new_x, new_y)


def is_point_on_land(x: float, y: float) -> bool:
    x = x % MAP_WIDTH
    y = y % MAP_HEIGHT
    tile_x, tile_y = int(x), int(y)
    tile_type = map_data[tile_y][tile_x]
    if tile_type == "l":
        return True
    elif tile_type in ["tl", "tr", "bl", "br"]:
        x_offset, y_offset = x % 1, y % 1
        if tile_type == "tl" and x_offset + y_offset < 1:
            return True
        elif tile_type == "tr" and x_offset > y_offset:
            return True
        elif tile_type == "bl" and x_offset < y_offset:
            return True
        elif tile_type == "br" and x_offset + y_offset > 1:
            return True
    return False


def get_ship_head_position(x: float, y: float, heading: float) -> Tuple[float, float]:
    ship_length = 20
    radians = math.radians(heading)
    head_x = (x + ship_length / 2 * math.sin(radians)) % MAP_WIDTH
    head_y = (y - ship_length / 2 * math.cos(radians)) % MAP_HEIGHT
    return (head_x, head_y)


def is_ship_head_on_land(x: float, y: float, heading: float) -> bool:
    head_x, head_y = get_ship_head_position(x, y, heading)
    return is_point_on_land(head_x, head_y)


@app.get("/home", response_class=HTMLResponse)
async def get_html():
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/game_state")
async def get_game_state():
    return game_state


async def update_game_state():
    last_update = time.time()
    while True:
        current_time = time.time()
        delta_time = current_time - last_update
        last_update = current_time

        for ship_id, ship_data in game_state["ships"].items():
            speed = ship_data["speed"]
            heading = ship_data["heading"]
            current_x, current_y = ship_data["x"], ship_data["y"]

            if speed > 0:
                new_x, new_y = calculate_new_position(
                    current_x, current_y, heading, speed, delta_time
                )

                if not is_ship_head_on_land(new_x, new_y, heading):
                    ship_data["x"], ship_data["y"] = new_x, new_y
                else:
                    ship_data["speed"] = 0

        # Send updated game state to all connected clients
        for connection in active_connections.values():
            try:
                await connection.send_json(game_state)
            except WebSocketDisconnect:
                # Handle disconnected clients
                disconnected_ship_id = next(
                    ship_id
                    for ship_id, conn in active_connections.items()
                    if conn == connection
                )
                del active_connections[disconnected_ship_id]
                logger.info(f"Client disconnected: {disconnected_ship_id}")

        await asyncio.sleep(0.01)  # Update every 50ms for smoother movement


@app.on_event("startup")
async def startup_event():
    global game_state
    game_state = {"ships": {}}  # Reset the game state

    # Initialize only one test ship
    game_state["ships"]["ship1"] = {
        "x": 250.0,
        "y": 250.0,
        "heading": 0.0,
        "speed": 0.0,
    }

    game_state["ships"]["ship2"] = {
        "x": 250.0,
        "y": 290.0,
        "heading": 0.0,
        "speed": 0.0,
    }

    asyncio.create_task(update_game_state())


@app.get("/ship/{ship_id}")
async def serve_ship_view(ship_id: str):
    if ship_id not in game_state["ships"]:
        raise HTTPException(status_code=404, detail="Ship not found")

    with open("static/ship_view.html", "r") as f:
        html_content = f.read()

    html_content = html_content.replace("{{ship_id}}", ship_id)
    return HTMLResponse(content=html_content)


@app.post("/update_ship")
async def update_ship(update: ShipUpdateRequest):
    if update.ship_id not in game_state["ships"]:
        raise HTTPException(status_code=404, detail="Ship not found")

    if update.key not in ["heading", "speed"]:
        raise HTTPException(
            status_code=400, detail="Invalid update key. Must be 'heading' or 'speed'"
        )

    ship_update = ShipUpdate(ship_id=update.ship_id, value=update.value)

    if update.key == "heading":
        await update_heading(ship_update)
    elif update.key == "speed":
        await update_speed(ship_update)

    return {"message": f"Updated {update.key} for ship {update.ship_id}"}


async def update_heading(update: ShipUpdate):
    if update.ship_id not in game_state["ships"]:
        raise ValueError(
            f"ship_id {update.ship_id} not in game_state['ships'] {game_state['ships']}"
        )
    game_state["ships"][update.ship_id]["heading"] = update.value % 360


async def update_speed(update: ShipUpdate):
    if update.ship_id not in game_state["ships"]:
        raise ValueError(
            f"ship_id {update.ship_id} not in game_state['ships'] {game_state['ships']}"
        )
    game_state["ships"][update.ship_id]["speed"] = max(0, min(update.value, 100))
