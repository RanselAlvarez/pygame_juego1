import pygame
import sys
import src.opciones as opciones
from src.personaje import Personaje

pygame.init()

# 🖥️ Configuración visual
pantalla = pygame.display.set_mode((opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))
pygame.display.set_caption("Mi Juego1")

# 🧍 Crear personaje
jugador = Personaje(375, 275)

run = True
while run:
    # 🧹 1. Limpiar pantalla en CADA frame
    pantalla.fill(opciones.COLOR_FONDO)
    
    # 📥 2. Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # 🎯 MOVIMIENTO POR PASOS: 50px por CADA pulsación
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                jugador.rect.x -= 50
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                jugador.rect.x += 50
            elif event.key in (pygame.K_w, pygame.K_UP):
                jugador.rect.y -= 50
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                jugador.rect.y += 50
            
            # 🔒 Límites de pantalla (se aplica inmediatamente tras mover)
            jugador.rect.clamp_ip(pygame.Rect(0, 0, opciones.ANCHO_PANTALLA, opciones.ALTO_PANTALLA))
            print(f"Posición: {jugador.rect.topleft}")

    # 🎨 3. Dibujar personaje
    jugador.dibujar_personaje(pantalla)
    
    # 📺 4. Actualizar ventana
    pygame.display.flip()

pygame.quit()
sys.exit()