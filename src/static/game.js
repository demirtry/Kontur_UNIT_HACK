const ITEM_TYPES = {
    common: {
        color: '#a8a878',
        icon: '🟫',
    }
};

const initialGameState = {
    backpackSize: typeof backpack_size !== 'undefined' ? backpack_size : 100,
    currentWeight: typeof weight_sum !== 'undefined' ? weight_sum : 0,
    currentTreasure: typeof treasure_sum !== 'undefined' ? treasure_sum : 0,
    bestTreasure: typeof best_treasure !== 'undefined' ? best_treasure : 0,
    selectedIds: typeof selected_ids !== 'undefined' ? selected_ids : []
};

let selectedCells = new Set(initialGameState.selectedIds);
let currentWeight = initialGameState.currentWeight;
let currentTreasure = initialGameState.currentTreasure;
let bestTreasure = initialGameState.bestTreasure;
const maxWeight = initialGameState.backpackSize;
let items = [];
let isGameEnded = false;

async function loadItems() {
    const savedState = localStorage.getItem('knapsackGameState');
    if (savedState) {
        const state = JSON.parse(savedState);
        if (state.items && Array.isArray(state.items)) {
            return state.items;
        }
    }

    try {
        const response = await fetch('/api/get_items');
        if (!response.ok) {
            throw new Error('Failed to load items');
        }
        const itemsData = await response.json();

        if (itemsData.error) {
            throw new Error(itemsData.error);
        }

        shuffleArray(itemsData);
        return itemsData;
    } catch (error) {
        console.error('Error loading items:', error);
        alert('Не удалось загрузить предметы. Пожалуйста, попробуйте позже.');
        throw error;
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function saveGameState() {
    const gameState = {
        selectedCells: Array.from(selectedCells),
        currentWeight,
        currentTreasure,
        bestTreasure,
        timeLeft: parseInt(document.getElementById('time-left').textContent.split(':')[0]) * 60 +
            parseInt(document.getElementById('time-left').textContent.split(':')[1]),
        items
    };
    localStorage.setItem('knapsackGameState', JSON.stringify(gameState));
}

function loadGameState() {
    const savedState = localStorage.getItem('knapsackGameState');
    if (savedState) {
        const state = JSON.parse(savedState);
        selectedCells = new Set(state.selectedCells);
        currentWeight = state.currentWeight;
        currentTreasure = state.currentTreasure;
        bestTreasure = state.bestTreasure;
        return state.timeLeft;
    }
    return 120;
}

async function initGame() {
    try {
        items = await loadItems();
        const gameGrid = document.getElementById('game-grid');
        gameGrid.innerHTML = '';

        items.forEach((item, index) => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.id = index;

            cell.innerHTML = `
                <div class="cell-icon">💰</div>
                <div class="cell-weight">Вес: ${item.weight}</div>
                <div class="cell-treasure">Ценность: ${item.treasure}</div>
            `;

            cell.addEventListener('click', () => handleCellClick(index, item));
            gameGrid.appendChild(cell);

            if (selectedCells.has(index)) {
                cell.classList.add('selected');
            }
        });

        updateStats();
    } catch (error) {
        document.getElementById('game-grid').innerHTML = `
            <div class="error-message">
                Не удалось загрузить предметы. Пожалуйста, проверьте файл items.json
            </div>
        `;
    }
}

function handleCellClick(index, item) {
    if (isGameEnded) return;

    if (selectedCells.has(index)) {
        selectedCells.delete(index);
        currentWeight -= item.weight;
        currentTreasure -= item.treasure;
    } else {
        if (currentWeight + item.weight > maxWeight) {
            alert('Превышен максимальный вес рюкзака!');
            return;
        }
        selectedCells.add(index);
        currentWeight += item.weight;
        currentTreasure += item.treasure;

        if (currentTreasure > bestTreasure) {
            bestTreasure = currentTreasure;
        }
    }

    updateCellAppearance(index);
    updateStats();
    saveGameState();
}

function updateCellAppearance(index) {
    const cell = document.querySelector(`.cell[data-id="${index}"]`);
    if (cell) {
        if (selectedCells.has(index)) {
            cell.classList.add('selected');
        } else {
            cell.classList.remove('selected');
        }
    }
}

function updateStats() {
    document.getElementById('current-weight').textContent = `${currentWeight}/${maxWeight}`;
    document.getElementById('current-score').textContent = currentTreasure;
    document.getElementById('best-score').textContent = bestTreasure;
}

async function endGame() {
    try {
        const response = await fetch('/api/game_end', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                best_treasure: bestTreasure
            })
        });

        if (!response.ok) {
            throw new Error('Ошибка при сохранении результата');
        }

        return await response.json();
    } catch (error) {
        console.error('Error ending game:', error);
        throw error;
    }
}

document.getElementById('finish-btn').addEventListener('click', async () => {
    try {
        isGameEnded = true;
        await endGame();
        localStorage.removeItem('knapsackGameState');
        location.reload();
    } catch (error) {
        alert('Ошибка при завершении игры: ' + error.message);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const timeLeft = loadGameState();
    if (timeLeft <= 0) {
        isGameEnded = true;
        document.querySelector('.game-container').classList.add('game-ended');
    }
    initGame();
    startTimer();
});

function startTimer() {
    let timeLeft = loadGameState();
    const timerElement = document.getElementById('time-left');
    const gameContainer = document.querySelector('.game-container');
    updateTimerDisplay();

    const timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();

        if (timeLeft <= 0) {
            clearInterval(timer);
            isGameEnded = true; // Устанавливаем флаг окончания игры
            gameContainer.classList.add('game-ended');
            endGame().then(() => {
                alert(`Время вышло!\nВаш лучший счёт: ${bestTreasure}`);
                localStorage.removeItem('knapsackGameState');
            }).catch(error => {
                alert('Ошибка при сохранении результата: ' + error.message);
            });
        }

        saveGameState();
    }, 1000);

    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}