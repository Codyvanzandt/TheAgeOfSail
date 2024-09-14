// Load the map image
const mapImage = new Image();
mapImage.src = '/static/map.png';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 500;
canvas.height = 500;

let gameState = null;
let socket = null;

// Draw the map once when it's loaded
mapImage.onload = () => {
    ctx.drawImage(mapImage, 0, 0);
};

function drawShip(x, y, heading, color = 'red') {
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

function initWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws/game`);

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
    if (!gameState || !gameState.ships) {
        console.error('Invalid game state received');
        return;
    }

    // Clear the entire canvas and redraw the map
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(mapImage, 0, 0);

    // Draw all ships
    for (const [shipId, ship] of Object.entries(gameState.ships)) {
        drawShip(ship.x, ship.y, ship.heading);
        console.log(`Ship ${shipId} - Position: (${ship.x.toFixed(2)}, ${ship.y.toFixed(2)}), Heading: ${ship.heading.toFixed(2)}, Speed: ${ship.speed.toFixed(2)}`);
    }
}

// Initialize WebSocket connection
initWebSocket();