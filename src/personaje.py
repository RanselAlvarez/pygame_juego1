import pygame
import src.opciones as opciones

class Personaje():
    def __init__(self, x, y):
        # Coordenadas 0, 0 es la esquina superior izquierda de la pantalla
        # 50, 50 es el tamaño del personaje (ancho y alto)
        self.forma = pygame.Rect(0, 0, opciones.ANCHO_PERSONAJE, opciones.ALTO_PERSONAJE)

        # Posicion que le damos al personaje en la pantalla
        # Se crea en la posicion 0, 0 pero nosotros hacemos que salga en x, y
        self.forma.center = (x, y)
        
    # Pantalla es donde va a dibujarse el personaje
    def dibujar_personaje(self, interfaz):
        # Dibujame el rectangulo en la pantalla con el color que le hemos dado al personaje
        # El primer parametro es la superficie donde se dibar (la pantalla), 
        # Self.forma es el rectangulo que queremos dibujar
        pygame.draw.rect(interfaz, opciones.COLOR_PERSONAJE, self.forma)
