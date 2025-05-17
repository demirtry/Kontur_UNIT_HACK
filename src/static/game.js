const ITEM_TYPES = {
    common: {
        color: '#a8a878',
        icon: '🟫',
    }
};

async function startGame() {
    const response = await fetch('/start_game');
//    функция Отобразить ячейки

}
async function show_progress() {
    const response = await fetch('/start_game');
//    функция Отобразить ячейки

}

async function process_click() {
    const response = await fetch('/process_click');
//    [снять выделение, выделить, не влезает]
//    values
//        values = {
//        "backpack_size": game.backpack_size,
//        "treasure_sum": game.matrix.treasure_sum,
//        "best_treasure": game.best_treasure,
//        "selected_ids": game.matrix.get_selected_ids()
    }
//    функция Отобразить ячейки

}

//async function createGameGrid() {
//    const response = await fetch('/get_matrix');
//    const matrix = await response.json();
//
//    const gameContainer = document.getElementById('game-container');
//    gameContainer.innerHTML = '';
//    gameContainer.style.gridTemplateColumns = `repeat(${matrix[0].length}, 80px)`;
//
//    matrix.forEach(row => {
//        row.forEach(cell => {
//            const cellElement = document.createElement('div');
//            cellElement.className = 'cell';
//            cellElement.dataset.id = cell.id;
//
//            const itemType = ITEM_TYPES[cell.type];
//
//            cellElement.innerHTML = `
//                <div class="cell-icon">${itemType.icon}</div>
//                <div class="cell-type">${itemType.name}</div>
//                <div class="cell-weight">Вес: ${cell.weight}</div>
//                <div class="cell-treasure">Ценность: ${cell.treasure}</div>
//            `;
//
//            cellElement.style.backgroundColor = itemType.color;
//            cellElement.addEventListener('click', handleCellClick);
//            gameContainer.appendChild(cellElement);
//        });
//    });
//}
//
//async function handleCellClick(event) {
//    const cellId = event.currentTarget.dataset.id;
//    const response = await fetch(`/process_click?cell_id=${cellId}`);
//    const result = await response.json();
//
//    if (result.success) {
//        updateGameState(result);
//        updateCellAppearance(event.currentTarget, result.cell);
//    }
//}
//
//function updateCellAppearance(cellElement, cellData) {
//    if (cellData.status) {
//        cellElement.classList.add('selected');
//        cellElement.style.opacity = '0.7';
//    } else {
//        cellElement.classList.remove('selected');
//        cellElement.style.opacity = '1';
//    }
//}