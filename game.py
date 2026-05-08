import pygame
import sys
import random

# ==========================================
# 🔧 1. CONSTANTES GLOBALES
# ==========================================
ANCHO, ALTO = 800, 800  # Pantalla cuadrada: ejes iguales, dificultad justa
TAMANO_BASE = 50
TAMANO_MINIMO = 20
REDUCCION_POR_NIVEL = 5

TIEMPO_MEMORIZAR = 6000  # 6s para memorizar
TIEMPO_JUGAR = 12000     # 12s para ejecutar

# Colores
COLOR_FONDO = (12, 12, 18)
COLOR_RUTA = (0, 180, 0)
COLOR_RUTA_BORDE = (0, 110, 0)
COLOR_INICIO = (0, 140, 255)
COLOR_INICIO_BORDE = (0, 80, 150)
COLOR_META = (255, 60, 60)
COLOR_META_BORDE = (160, 30, 30)
COLOR_JUGADOR = (255, 215, 0)   # Dorado/Amarillo
COLOR_JUGADOR_BORDE = (190, 150, 0)
COLOR_TEXTO = (240, 240, 240)
COLOR_ERROR = (255, 90, 90)

# Estilo visual
RADIO_BORDE = 10   # Redondeado de esquinas
GROSOR_BORDE = 3   # Grosor del borde

# ==========================================
# 🎮 2. INICIALIZACIÓN
# ==========================================
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Memoria de Ruta - 800x800")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("consolas", 28)

# ==========================================
# 🖌️ 3. HELPER VISUAL
# ==========================================
def dibujar_celda(pantalla, col, fila, tamano, color_fondo, color_borde, radio, grosor):
    """Dibuja una celda con bordes redondeados de forma consistente"""
    rect = pygame.Rect(col * tamano, fila * tamano, tamano, tamano)
    # 1. Dibujar borde (width dibuja hacia adentro)
    pygame.draw.rect(pantalla, color_borde, rect, border_radius=radio, width=grosor)
    # 2. Dibujar relleno por encima
    pygame.draw.rect(pantalla, color_fondo, rect, border_radius=radio)

# ==========================================
# 🧠 4. CLASE JUEGO
# ==========================================
class Juego:
    def __init__(self):
        self.nivel = 1
        self.estado = "MENU"
        self.ruta = []
        self.ruta_set = set()       # Para validación O(1)
        self.jugador_celda = (0, 0)
        self.tamano_personaje = TAMANO_BASE
        self.meta = (0, 0)
        self.tiempo_inicio = 0
        self.mensaje_error = ""
        self.reiniciar_nivel()

    def calcular_tamano(self):
        tamano = TAMANO_BASE - (self.nivel - 1) * REDUCCION_POR_NIVEL
        return max(tamano, TAMANO_MINIMO)

    def reiniciar_nivel(self):
        self.tamano_personaje = self.calcular_tamano()
        self.generar_ruta()
        self.jugador_celda = self.ruta[0]
        self.meta = self.ruta[-1]
        self.ruta_set = set(self.ruta)  # Optimización de búsqueda
        self.estado = "MEMORIZAR"
        self.tiempo_inicio = pygame.time.get_ticks()
        self.mensaje_error = ""

    def generar_ruta(self):
        """Genera una ruta SIEMPRE contigua de extremo a extremo"""
        ruta = []
        COLUMNAS = ANCHO // self.tamano_personaje
        FILAS = ALTO // self.tamano_personaje
        
        # Dirección aleatoria: horizontal o vertical (ahora son iguales por 800x800)
        direccion = random.choice(['horizontal', 'vertical'])

        if direccion == 'horizontal':
            y = random.randint(1, FILAS - 2)
            x = 0
            ruta.append((x, y))
            
            while x < COLUMNAS - 1:
                # 35% de probabilidad de desviarse en la MISMA columna
                if random.random() < 0.35:
                    dy = random.choice([-1, 1])
                    if 0 <= y + dy < FILAS:
                        y += dy
                        ruta.append((x, y))  # Celda vertical contigua
                x += 1
                ruta.append((x, y))          # Avance horizontal contiguo

        else:  # vertical
            x = random.randint(1, COLUMNAS - 2)
            y = 0
            ruta.append((x, y))
            
            while y < FILAS - 1:
                if random.random() < 0.35:
                    dx = random.choice([-1, 1])
                    if 0 <= x + dx < COLUMNAS:
                        x += dx
                        ruta.append((x, y))  # Celda horizontal contigua
                y += 1
                ruta.append((x, y))          # Avance vertical contiguo

        self.ruta = ruta

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if self.estado == "MENU":
                    self.reiniciar_nivel()
                elif self.estado == "JUGANDO":
                    self.mover_jugador(evento.key)
        return True

    def mover_jugador(self, tecla):
        x, y = self.jugador_celda
        COLUMNAS = ANCHO // self.tamano_personaje
        FILAS = ALTO // self.tamano_personaje

        if tecla == pygame.K_LEFT: nx, ny = x - 1, y
        elif tecla == pygame.K_RIGHT: nx, ny = x + 1, y
        elif tecla == pygame.K_UP: nx, ny = x, y - 1
        elif tecla == pygame.K_DOWN: nx, ny = x, y + 1
        else: return

        if not (0 <= nx < COLUMNAS and 0 <= ny < FILAS):
            return

        # 🔴 VALIDACIÓN: ¿La celda destino pertenece a la ruta original?
        if (nx, ny) not in self.ruta_set:
            self.estado = "DERROTA"
            self.tiempo_inicio = pygame.time.get_ticks()
            self.mensaje_error = "¡Saliste de la ruta!"
            return

        self.jugador_celda = (nx, ny)
        if self.jugador_celda == self.meta:
            self.estado = "VICTORIA"
            self.tiempo_inicio = pygame.time.get_ticks()

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if self.estado == "MEMORIZAR" and ahora - self.tiempo_inicio > TIEMPO_MEMORIZAR:
            self.estado = "JUGANDO"
            self.tiempo_inicio = ahora
        elif self.estado == "JUGANDO" and ahora - self.tiempo_inicio > TIEMPO_JUGAR:
            self.estado = "DERROTA"
            self.tiempo_inicio = ahora
        elif self.estado == "VICTORIA" and ahora - self.tiempo_inicio > 1500:
            self.nivel += 1
            self.reiniciar_nivel()
        elif self.estado == "DERROTA" and ahora - self.tiempo_inicio > 2500:
            self.nivel = 1
            self.estado = "MENU"

    def dibujar(self):
        pantalla.fill(COLOR_FONDO)
        ahora = pygame.time.get_ticks()
        t = self.tamano_personaje

        if self.estado == "MENU":
            self.escribir_texto(f"Nivel {self.nivel}", (ANCHO//2, ALTO//2 - 20))
            self.escribir_texto("Presiona cualquier tecla", (ANCHO//2, ALTO//2 + 20))
            self.escribir_texto(f"Personaje: {t}x{t}px", (ANCHO//2, ALTO//2 + 60), color=(140,140,180))

        elif self.estado == "MEMORIZAR":
            for px, py in self.ruta:
                dibujar_celda(pantalla, px, py, t, COLOR_RUTA, COLOR_RUTA_BORDE, RADIO_BORDE, GROSOR_BORDE)
            # Inicio marcado
            dibujar_celda(pantalla, self.ruta[0][0], self.ruta[0][1], t, COLOR_INICIO, COLOR_INICIO_BORDE, RADIO_BORDE, GROSOR_BORDE)
            # Meta marcada
            dibujar_celda(pantalla, self.meta[0], self.meta[1], t, COLOR_META, COLOR_META_BORDE, RADIO_BORDE, GROSOR_BORDE)
            
            restante = max(0, (TIEMPO_MEMORIZAR - (ahora - self.tiempo_inicio)) / 1000)
            self.escribir_texto(f"Memoriza: {restante:.1f}s", (ANCHO//2, 30))

        elif self.estado == "JUGANDO":
            # Meta visible
            dibujar_celda(pantalla, self.meta[0], self.meta[1], t, COLOR_META, COLOR_META_BORDE, RADIO_BORDE, GROSOR_BORDE)
            # Jugador
            dibujar_celda(pantalla, self.jugador_celda[0], self.jugador_celda[1], t, COLOR_JUGADOR, COLOR_JUGADOR_BORDE, RADIO_BORDE, GROSOR_BORDE)
            
            restante = max(0, (TIEMPO_JUGAR - (ahora - self.tiempo_inicio)) / 1000)
            self.escribir_texto(f"Tiempo: {restante:.1f}s", (ANCHO//2, 30))
            if self.mensaje_error:
                self.escribir_texto(self.mensaje_error, (ANCHO//2, ALTO//2), color=COLOR_ERROR)

        elif self.estado == "VICTORIA":
            self.escribir_texto("¡Nivel Completado!", (ANCHO//2, ALTO//2), color=(0, 255, 0))
            self.escribir_texto("Siguiente nivel...", (ANCHO//2, ALTO//2 + 30))
        elif self.estado == "DERROTA":
            texto = self.mensaje_error if self.mensaje_error else "¡Tiempo Agotado!"
            self.escribir_texto(texto, (ANCHO//2, ALTO//2), color=COLOR_ERROR)
            self.escribir_texto("Reiniciando...", (ANCHO//2, ALTO//2 + 30))

        pygame.display.flip()

    def escribir_texto(self, texto, pos, color=COLOR_TEXTO):
        surf = fuente.render(texto, True, color)
        rect = surf.get_rect(center=pos)
        pantalla.blit(surf, rect)

    def ejecutar(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            reloj.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Juego().ejecutar()