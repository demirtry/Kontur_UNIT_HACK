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

async function loadItems() {
    try {
        const response = await fetch('/api/get_items');
        if (!response.ok) {
            throw new Error('Failed to load items');
        }
        const itemsData = await response.json();

        if (itemsData.error) {
            throw new Error(itemsData.error);
        }

        return itemsData;
    } catch (error) {
        console.error('Error loading items:', error);
        alert('Не удалось загрузить предметы. Пожалуйста, попробуйте позже.');
        throw error;
    }
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
        });

        initialGameState.selectedIds.forEach(id => {
            updateCellAppearance(id);
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
}

function updateCellAppearance(index) {
    const cell = document.querySelector(`.cell[data-id="${index}"]`);
    if (cell) {  // Проверяем, существует ли элемент
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

document.getElementById('finish-btn').addEventListener('click', () => {
    alert(`Игра завершена!\nВаш счёт: ${currentTreasure}\nЛучший счёт: ${bestTreasure}`);
});

function startTimer() {
    let timeLeft = 91; // 1:31 in seconds
    const timerElement = document.getElementById('time-left');

    const timer = setInterval(() => {
        timeLeft--;
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (timeLeft <= 0) {
            clearInterval(timer);
            alert('Время вышло!');
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
    initGame();
    startTimer();
});

// async function startGame() {
//     const response = await fetch('/game');
//
// }
// async function show_progress() {
//     const response = await fetch('/start_game');
// //    функция Отобразить ячейки
//
// }
//
// async function process_click() {
//     const response = await fetch('/process_click');
// //    [снять выделение, выделить, не влезает]
// //    values
// //        values = {
// //        "backpack_size": game.backpack_size,
// //        "treasure_sum": game.matrix.treasure_sum,
// //        "best_treasure": game.best_treasure,
// //        "selected_ids": game.matrix.get_selected_ids()
//     }
// //    функция Отобразить ячейки
//
// }
