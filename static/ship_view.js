const canvas = document.getElementById('shipCanvas');
const ctx = canvas.getContext('2d');

const VIEWPORT_WIDTH = 200;
const VIEWPORT_HEIGHT = 200;

canvas.width = VIEWPORT_WIDTH;
canvas.height = VIEWPORT_HEIGHT;

const mapImage = new Image();
mapImage.src = '/static/map.png';

let shipId = null;
let gameState = null;
let socket = null;

let keyStates = {
    'a': false,
    'd': false,
    'w': false,
    's': false
};
const KEY_REPEAT_INTERVAL = 50;

function initShipView() {
    shipId = window.location.pathname.split('/')[1];
    if (!shipId) {
        console.error('No ship ID provided');
        return;
    }

    console.log('Initializing view for ship:', shipId);
    initWebSocket();
    initKeyboardControls();
}

function initWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws/${shipId}`);

    socket.onopen = () => {
        console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
        gameState = JSON.parse(event.data);
        console.log('Received game state:', gameState);
        updateGameView();
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed');
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

function updateGameView() {
    if (!gameState || !gameState.ships || !gameState.ships[shipId]) {
        console.error('Invalid game state received');
        return;
    }

    drawViewport();
    updateGameDataDisplay();
}

function drawViewport() {
    const shipState = gameState.ships[shipId];
    const { x, y, heading } = shipState;
    console.log(`Drawing viewport for ship ${shipId} at (${x}, ${y}) with heading ${heading}`);

    ctx.clearRect(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT);

    // Calculate viewport offset
    const viewportOffsetX = x - VIEWPORT_WIDTH / 2;
    const viewportOffsetY = y - VIEWPORT_HEIGHT / 2;

    ctx.drawImage(
        mapImage,
        viewportOffsetX, viewportOffsetY, VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
        0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    );

    // Draw other ships
    for (const [id, ship] of Object.entries(gameState.ships)) {
        const shipX = ship.x - viewportOffsetX;
        const shipY = ship.y - viewportOffsetY;
        if (shipX >= 0 && shipX < VIEWPORT_WIDTH && shipY >= 0 && shipY < VIEWPORT_HEIGHT) {
            drawShip(shipX, shipY, ship.heading, id === shipId ? 'red' : 'yellow');
        }
    }
}

function drawShip(x, y, heading, color) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(heading * Math.PI / 180);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(0, -10);
    ctx.lineTo(5, 10);
    ctx.lineTo(-5, 10);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
}

function updateGameDataDisplay() {
    const shipState = gameState.ships[shipId];
    document.getElementById('position').textContent = `(${shipState.x.toFixed(2)}, ${shipState.y.toFixed(2)})`;
    document.getElementById('heading').textContent = `${shipState.heading.toFixed(2)}°`;
    document.getElementById('speed').textContent = shipState.speed.toFixed(2);
}

function updateShipControl(control, value) {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error('WebSocket is not connected');
        return;
    }

    console.log(`Updating ${control} for ship ${shipId} to ${value}`);
    socket.send(JSON.stringify({ [control]: value }));
}

function initKeyboardControls() {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    setInterval(handleKeyHold, KEY_REPEAT_INTERVAL);
}

function handleKeyDown(event) {
    if (keyStates.hasOwnProperty(event.key)) {
        keyStates[event.key] = true;
    }
}

function handleKeyUp(event) {
    if (keyStates.hasOwnProperty(event.key)) {
        keyStates[event.key] = false;
    }
}

function handleKeyHold() {
    if (!gameState || !gameState.ships || !gameState.ships[shipId]) {
        return;
    }

    const shipState = gameState.ships[shipId];
    if (keyStates['a']) {
        updateShipControl('heading', (shipState.heading - 5 + 360) % 360);
    }
    if (keyStates['d']) {
        updateShipControl('heading', (shipState.heading + 5) % 360);
    }
    if (keyStates['w']) {
        updateShipControl('speed', Math.min(shipState.speed + 2, 100));
    }
    if (keyStates['s']) {
        updateShipControl('speed', Math.max(shipState.speed - 2, 0));
    }
}

// Initialize the ship view
initShipView();