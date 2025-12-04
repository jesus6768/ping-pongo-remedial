# ============================================
# PING PONG ULTIMATE EDITION
# Clase Paleta
# ============================================

import pygame
from game.config import *


class Paddle:
    """Clase que representa una paleta del juego"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.velocity = 0  # Para suavidad de movimiento
        self.acceleration = 0.5
        self.max_velocity = PADDLE_SPEED
        self.glow_intensity = 0  # Para efecto de brillo
    
    def update(self, keys=None, mouse_y=None, analog_input=None):
        """Actualiza la posición de la paleta"""
        target_velocity = 0
        
        if keys is not None:
            # Movimiento con teclado
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                target_velocity = -self.max_velocity
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                target_velocity = self.max_velocity
        
        elif mouse_y is not None:
            # Movimiento suave hacia la posición del ratón
            center_y = self.y + self.height // 2
            difference = mouse_y - center_y
            
            if abs(difference) > 5:
                target_velocity = max(-self.max_velocity, 
                                    min(self.max_velocity, difference * 0.1))
        
        elif analog_input is not None:
            # Entrada analógica (para joystick)
            target_velocity = analog_input * self.max_velocity
        
        # Aplicar aceleración suave
        self.velocity += (target_velocity - self.velocity) * self.acceleration
        self.y += self.velocity
        
        # Mantener dentro de los límites
        self.y = max(0, min(WINDOW_HEIGHT - self.height, self.y))
        
        # Efecto de brillo
        self.glow_intensity = max(0, self.glow_intensity - 2)
        if abs(self.velocity) > self.max_velocity * 0.5:
            self.glow_intensity = 100
    
    def draw(self, screen, color=WHITE):
        """Dibuja la paleta"""
        # Paleta principal
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Efecto de brillo
        if self.glow_intensity > 0:
            glow_color = tuple(min(255, c + self.glow_intensity) for c in [0, 100, 255])
            pygame.draw.rect(screen, glow_color, 
                           (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)
        
        # Línea central de la paleta
        mid = self.height // 2
        pygame.draw.line(screen, CYAN, 
                        (self.x, self.y + mid),
                        (self.x + self.width, self.y + mid), 1)
    
    def get_rect(self):
        """Retorna rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_center(self):
        """Retorna centro de la paleta"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def reset(self, y=None):
        """Reinicia la paleta a posición central"""
        if y is None:
            y = WINDOW_HEIGHT // 2 - self.height // 2
        self.y = y
        self.velocity = 0
    
    def collides_with(self, rect):
        """Verifica colisión con otro rectángulo"""
        return self.get_rect().colliderect(rect)
