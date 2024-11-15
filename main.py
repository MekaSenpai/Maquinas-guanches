import pygame
import sys
import os
import time
import threading

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG Canario")

# Colores
WHITE = (255, 255, 255)

# Cargar imágenes
fondo = pygame.image.load("fondo.jpg")
logo = pygame.image.load("logo.png")

# Clase para el personaje principal
class Personaje:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nivel = 1
        self.fragmentos = []

# Función para mostrar el menú principal
def menu_principal():
    opciones = ["Nueva Partida", "Cargar Partida", "Opciones", "Salir"]
    seleccion = 0

    while True:
        screen.blit(fondo, (0, 0))
        screen.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 2, 50))
        
        font = pygame.font.Font(None, 36)
        text = font.render("Menú Principal", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        
        for i, opcion in enumerate(opciones):
            color = (0, 0, 0) if i != seleccion else (255, 0, 0)  # Resaltar la opción seleccionada
            text = font.render(opcion, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + (i + 1) * 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)  # Mover hacia abajo
                elif event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)  # Mover hacia arriba
                elif event.key == pygame.K_RETURN:
                    return seleccion  # Retorna el índice de la opción seleccionada

# Función para iniciar una nueva partida
def nueva_partida():
    nombre = ""
    font = pygame.font.Font(None, 36)
    input_active = True  # Variable para saber si el cuadro de texto está activo

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Cuando se presiona Enter
                    input_active = False  # Termina la entrada
                elif event.key == pygame.K_BACKSPACE:  # Maneja la tecla de retroceso
                    nombre = nombre[:-1]  # Elimina el último carácter
                else:
                    nombre += event.unicode  # Agrega el carácter ingresado

        # Dibuja el fondo y el texto
        screen.blit(fondo, (0, 0))
        text_surface = font.render("Introduce el nombre de tu personaje:", True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        # Dibuja el nombre ingresado
        input_surface = font.render(nombre, True, (0, 0, 0))
        screen.blit(input_surface, (SCREEN_WIDTH // 2 - input_surface.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    jugador = Personaje(nombre)
    print(f"¡Bienvenido, {jugador.nombre}! Comienza tu aventura.")
    guardar_partida(jugador)
    return jugador


# Función para guardar la partida
def guardar_partida(jugador):
    if not os.path.exists("Partidas"):
        os.makedirs("Partidas")
    
    with open(f"Partidas/{jugador.nombre}.save", "w") as f:
        f.write(f"Nombre: {jugador.nombre}\nNivel: {jugador.nivel}\nFragmentos: {len(jugador.fragmentos)}")
    print("Partida guardada.")

# Función para cargar una partida
def cargar_partida():
    partidas = [f for f in os.listdir("Partidas") if f.endswith(".save")]
    if not partidas:
        print("No hay partidas guardadas.")
        return None

    print("Partidas guardadas:")
    for i, partida in enumerate(partidas):
        print(f"{i + 1}. {partida[:-5]}")  # Mostrar el nombre sin la extensión

    seleccion = int(input("Selecciona la partida a cargar (número): ")) - 1
    if 0 <= seleccion < len(partidas):
        nombre_partida = partidas[seleccion][:-5]  # Nombre sin la extensión
        with open(f"Partidas/{partidas[seleccion]}", "r") as f:
            data = f.readlines()
            nombre = data[0].split(": ")[1].strip()
            nivel = int(data[1].split(": ")[1].strip())
            fragmentos = int(data[2].split(": ")[1].strip())
            jugador = Personaje(nombre)
            jugador.nivel = nivel
            jugador.fragmentos = ["Fragmento"] * fragmentos
            print(f"Partida '{nombre_partida}' cargada exitosamente.")
            return jugador
    else:
        print("Selección inválida.")
        return None

# Func ión para guardar opciones
def guardar_opciones(opciones):
    with open("Opciones.txt", "w") as f:
        for opcion in opciones:
            f.write(f"{opcion}\n")

# Función para guardar automáticamente cada 10 minutos
def guardar_periodicamente(jugador):
    while True:
        time.sleep(600)  # Espera 10 minutos
        guardar_partida(jugador)

# Función para mostrar el menú de opciones
def menu_opciones():
    opciones_graficas = ["800x600", "1024x768", "1280x720"]
    opciones_sonido = ["Volumen: 100%", "Volumen: 75%", "Volumen: 50%", "Volumen: 25%", "Volumen: 0%"]
    seleccion_grafica = 0
    seleccion_sonido = 0

    while True:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Opciones", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

        text_graficas = font.render("Opciones Gráficas", True, (0, 0, 0))
        screen.blit(text_graficas, (50, 100))
        for i, opcion in enumerate(opciones_graficas):
            color = (0, 0, 0) if i != seleccion_grafica else (255, 0, 0)
            text = font.render(opcion, True, color)
            screen.blit(text, (70, 140 + i * 30))

        text_sonido = font.render("Opciones de Sonido", True, (0, 0, 0))
        screen.blit(text_sonido, (50, 240))
        for i, opcion in enumerate(opciones_sonido):
            color = (0, 0, 0) if i != seleccion_sonido else (255, 0, 0)
            text = font.render(opcion, True, color)
            screen.blit(text, (70, 280 + i * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if seleccion_grafica < len(opciones_graficas) - 1:
                        seleccion_grafica += 1
                    else:
                        seleccion_sonido = (seleccion_sonido + 1) % len(opciones_sonido)
                elif event.key == pygame.K_UP:
                    if seleccion_sonido > 0:
                        seleccion_sonido -= 1
                    else:
                        seleccion_grafica = max(0, seleccion_grafica - 1)
                elif event.key == pygame.K_RETURN:
                    if seleccion_grafica < len(opciones_graficas):
                        resolucion = opciones_graficas[seleccion_grafica].split("x")
                        SCREEN_WIDTH = int(resolucion[0])
                        SCREEN_HEIGHT = int(resolucion[1])
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cambia la resolución
                        print(f"Resolución cambiada a: {opciones_graficas[seleccion_grafica]}")
                    else:
                        # Ajustar el volumen
                        volumen = 1 - (seleccion_sonido * 0.25)  # Convierte la selección a un valor entre 0 y 1
                        pygame.mixer.music.set_volume(volumen)
                        print(f"Volumen ajustado a: {opciones_sonido[seleccion_sonido]}")
                    return  # Regresar al menú principal

# Bucle principal del juego
def main():
    jugador = None
    opciones = ["Opción1", "Opción2"]  # Opciones predeterminadas
    guardar_opciones(opciones)  # Guardar opciones al inicio

    while True:
        seleccion = menu_principal()
        if seleccion == 0:  # Nueva Partida
            jugador = nueva_partida()
            # Iniciar el hilo de guardado automático
            threading.Thread(target=guardar_periodicamente, args=(jugador,), daemon=True).start()
        elif seleccion == 1:  # Cargar Partida
            jugador = cargar_partida()
        elif seleccion == 2:  # Opciones
            menu_opciones()
        elif seleccion == 3:  # Salir
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
