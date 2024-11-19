function startNewGame() {
    window.location.href = "juego.html";
}

function openLoadMenu() {
    document.getElementById('loadMenu').style.display = 'block';
}

function closeLoadMenu() {
    document.getElementById('loadMenu').style.display = 'none';
}

function loadGame(slot) {
    // Aquí se debería implementar la lógica para cargar el archivo .save desde el directorio Guardadas
    console.log(`Cargando ${slot}`);
}

function executeLoad() {
    // Implementar la lógica para cargar la partida seleccionada
    alert('Partida cargada');
    closeLoadMenu();
}

function openSettings() {
    document.getElementById('settingsMenu').style.display = 'block';
}

function closeSettingsMenu() {
    document.getElementById('settingsMenu').style.display = 'none';
}

function setVolume(volume) {
    // Implementar la lógica para ajustar el volumen del juego
    console.log(`Volumen ajustado a ${volume}`);
}

function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

function exitGame() {
    window.close(); // Esto solo funcionará si se ejecuta desde una aplicación NW.js o similar
}
