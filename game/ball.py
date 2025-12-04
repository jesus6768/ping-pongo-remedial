# ============================================
# PING PONG ULTIMATE EDITION
# Clase Pelota
# ============================================

import pygame
import math
import random
from game.config import *


class Ball:
    """Clase que representa la pelota del juego"""
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.start_x = x
        self.start_y = y
        self.size = BALL_SIZE
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-0.5, 0, 0.5])
        self.trail = []  # Para efecto de rastro
        self.max_trail_length = 15
        self.last_collision_time = 0
    
    def update(self):
        """Actualiza posición de la pelota"""
        # Guardar posición anterior para el rastro
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
        
        # Actualizar posición
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Aplicar fricción mínima (mantener velocidad)
        self.speed_x *= 0.999
        self.speed_y *= 0.999
        
        # Asegurar que no sea demasiado lenta
        speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
        if speed < BALL_SPEED * 0.8:
            ratio = (BALL_SPEED * 0.8) / speed if speed > 0 else 1
            self.speed_x *= ratio
            self.speed_y *= ratio
        
        # Rebote en bordes superior e inferior
        if self.y - self.size // 2 <= 0:
            self.y = self.size // 2
            self.speed_y = abs(self.speed_y) * 0.95
        elif self.y + self.size // 2 >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.size // 2
            self.speed_y = -abs(self.speed_y) * 0.95
    
    def draw(self, screen):
        """Dibuja la pelota con efecto de rastro"""
        # Dibujar rastro
        for i, (x, y) in enumerate(self.trail):
            alpha = int(50 * (i / len(self.trail)))
            color = (255 - alpha, 255 - alpha, 200)
            size = max(1, int(self.size // 2 * (i / len(self.trail))))
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
        
        # Dibujar pelota principal
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2)
        
        # Efecto de brillo
        pygame.draw.circle(screen, CYAN, (int(self.x) - 2, int(self.y) - 2), self.size // 3, 1)
    
    def reset(self, x=None, y=None):
        """Reinicia la pelota a posición central"""
        if x is None:
            x = self.start_x
        if y is None:
            y = self.start_y
        
        self.x = float(x)
        self.y = float(y)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 0.5, -0.5, 1])
        self.trail = []
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
    
    def get_speed(self):
        """Retorna velocidad actual"""
        return math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
    
    def is_out_of_bounds(self):
        """Verifica si está fuera de los límites"""
        return self.x < 0 or self.x > WINDOW_WIDTH
