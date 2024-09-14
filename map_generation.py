import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 50
PIXEL_SIZE = 10
SCREEN_SIZE = GRID_SIZE * PIXEL_SIZE

# Colors
LAND_COLOR = (0, 255, 0)  # Green
WATER_COLOR = (0, 0, 255)  # Blue

# Temporary save file
TEMP_SAVE_FILE = "temp_save.json"


def draw_square(surface, x, y, square_type):
    rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
    if square_type == "l":
        pygame.draw.rect(surface, LAND_COLOR, rect)
    elif square_type == "w":
        pygame.draw.rect(surface, WATER_COLOR, rect)
    elif square_type == "tl":
        pygame.draw.rect(surface, WATER_COLOR, rect)
        pygame.draw.polygon(
            surface,
            LAND_COLOR,
            [
                (x * PIXEL_SIZE, y * PIXEL_SIZE),
                ((x + 1) * PIXEL_SIZE, y * PIXEL_SIZE),
                (x * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
            ],
        )
    elif square_type == "tr":
        pygame.draw.rect(surface, WATER_COLOR, rect)
        pygame.draw.polygon(
            surface,
            LAND_COLOR,
            [
                ((x + 1) * PIXEL_SIZE, y * PIXEL_SIZE),
                ((x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
                (x * PIXEL_SIZE, y * PIXEL_SIZE),
            ],
        )
    elif square_type == "bl":
        pygame.draw.rect(surface, WATER_COLOR, rect)
        pygame.draw.polygon(
            surface,
            LAND_COLOR,
            [
                (x * PIXEL_SIZE, y * PIXEL_SIZE),
                ((x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
                (x * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
            ],
        )
    elif square_type == "br":
        pygame.draw.rect(surface, WATER_COLOR, rect)
        pygame.draw.polygon(
            surface,
            LAND_COLOR,
            [
                ((x + 1) * PIXEL_SIZE, y * PIXEL_SIZE),
                ((x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
                (x * PIXEL_SIZE, (y + 1) * PIXEL_SIZE),
            ],
        )


def get_valid_input():
    valid_types = ["l", "w", "tl", "tr", "bl", "br"]
    while True:
        user_input = (
            input(
                "Enter square type (l, w, tl, tr, bl, br) [optional: number] or 'q' to quit: "
            )
            .strip()
            .split()
        )
        if not user_input:
            print("Empty input. Please try again.")
            continue
        if user_input[0] == "q":
            return "q"
        if user_input[0] not in valid_types:
            print(f"Invalid square type. Please use one of {', '.join(valid_types)}.")
            continue
        if len(user_input) > 1:
            try:
                repeat = int(user_input[1])
                if repeat <= 0:
                    print("Number must be positive. Please try again.")
                    continue
            except ValueError:
                print("Invalid number. Please try again.")
                continue
        return user_input


def save_results(grid, filename_prefix="map"):
    # Create surface and draw the map
    surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    for y, row in enumerate(grid):
        for x, square_type in enumerate(row):
            draw_square(surface, x, y, square_type)

    # Save as PNG
    png_filename = f"{filename_prefix}.png"
    pygame.image.save(surface, png_filename)
    print(f"Map saved as '{png_filename}'")

    # Save as JSON
    json_filename = f"{filename_prefix}.json"
    with open(json_filename, "w") as f:
        json.dump(grid, f, indent=2)
    print(f"Map data saved as '{json_filename}'")


def save_temp_state(grid):
    with open(TEMP_SAVE_FILE, "w") as f:
        json.dump({"grid": grid}, f, indent=2)
    print(f"Progress saved. You can resume from this point later.")


def load_temp_state():
    if os.path.exists(TEMP_SAVE_FILE):
        with open(TEMP_SAVE_FILE, "r") as f:
            state = json.load(f)
        return state["grid"]
    return None


def load_final_map():
    with open("final_map.json", "r") as f:
        return json.load(f)


def load_final_map_as_grid():
    final_map = load_final_map()
    return [
        [square for square in row for _ in range(10)]
        for row in final_map
        for _ in range(10)
    ]


def draw_final_map():
    map_data = load_final_map()
    surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    for y, row in enumerate(map_data):
        for x, square_type in enumerate(row):
            draw_square(surface, x, y, square_type)

    # Save as PNG
    png_filename = f"final_map.png"
    pygame.image.save(surface, png_filename)
    print(f"Map saved as '{png_filename}'")


def compute_position(grid):
    for row, row_data in enumerate(grid):
        if len(row_data) < GRID_SIZE:
            return row, len(row_data)
    return len(grid), 0


def main():
    grid = load_temp_state()
    if grid is None:
        grid = []

    row, col = compute_position(grid)
    print(f"Resuming from Row {row + 1}, Column {col + 1}")

    while row < GRID_SIZE:
        while len(grid) <= row:
            grid.append([])

        while col < GRID_SIZE:
            print(f"Row {row + 1}, Column {col + 1}")
            if col < len(grid[row]):
                print(f"Current: {grid[row][col]}")
                col += 1
                continue

            user_input = get_valid_input()

            if user_input == "q":
                print("Quitting and saving progress...")
                save_temp_state(grid)
                save_results(grid, "current_state")
                return  # Exit the function

            square_type = user_input[0]
            repeat = int(user_input[1]) if len(user_input) > 1 else 1

            for _ in range(repeat):
                if col >= GRID_SIZE:
                    break
                grid[row].append(square_type)
                col += 1
        row += 1
        col = 0

    # Save final results
    save_results(grid, "final_map")

    # Remove temporary save file as map is complete
    os.remove(TEMP_SAVE_FILE)
    print("Temporary save file removed as map is complete.")
