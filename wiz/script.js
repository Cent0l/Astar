const gridElement = document.getElementById('grid');
const rows = 20;
const cols = 20;
let grid = [];

// Funkcja do wczytywania mapy z pliku
async function wczytajMape() {
    try {
        const response = await fetch('grid.txt');
        const text = await response.text();
        grid = text.trim().split('\n').map(row => row.trim().split(' ').map(Number));
        initGrid();
        aStar();
    } catch (error) {
        console.error('Błąd podczas wczytywania mapy:', error);
        alert('Nie udało się wczytać pliku grid.txt!');
    }
}

// Inicjalizacja siatki w HTML
function initGrid() {
    gridElement.innerHTML = '';
    gridElement.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
    gridElement.style.gridTemplateRows = `repeat(${rows}, 30px)`;

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.x = x;
            cell.dataset.y = y;

            if (grid[y][x] === 5) cell.classList.add('wall');
            if (x === 0 && y === rows - 1) cell.classList.add('start');
            if (x === cols - 1 && y === 0) cell.classList.add('end');

            gridElement.appendChild(cell);
        }
    }
}

// Algorytm A*
function aStar() {
    const start = [rows - 1, 0];
    const end = [0, cols - 1];
    
    let openList = [start];
    let costs = Array.from({ length: rows }, () => Array(cols).fill(Infinity));
    let cameFrom = Array.from({ length: rows }, () => Array(cols).fill(null));
    costs[start[0]][start[1]] = 0;

    while (openList.length > 0) {
        openList.sort((a, b) => costs[a[0]][a[1]] - costs[b[0]][b[1]]);
        const current = openList.shift();

        if (current[0] === end[0] && current[1] === end[1]) {
            reconstructPath(cameFrom, current);
            return;
        }

        for (const [dx, dy] of [[0, 1], [1, 0], [0, -1], [-1, 0]]) {
            const nx = current[0] + dx;
            const ny = current[1] + dy;

            if (nx >= 0 && ny >= 0 && nx < rows && ny < cols && grid[nx][ny] !== 5) {
                const newCost = costs[current[0]][current[1]] + 1;
                if (newCost < costs[nx][ny]) {
                    costs[nx][ny] = newCost;
                    openList.push([nx, ny]);
                    cameFrom[nx][ny] = current;
                }
            }
        }
    }
    alert("Brak ścieżki!");
}

// Odtwarzanie ścieżki
function reconstructPath(cameFrom, current) {
    while (current) {
        const [x, y] = current;
        document.querySelector(`[data-x="${y}"][data-y="${x}"]`).classList.add('path');
        current = cameFrom[x][y];
    }
}

// Uruchomienie
wczytajMape();
