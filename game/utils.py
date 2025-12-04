# ============================================
# PING PONG ULTIMATE EDITION
# Funciones Auxiliares y Utilidades
# ============================================

import pygame
import math
from game.config import *


class Particle:
    """Partículas para efectos visuales"""
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # gravedad
        self.lifetime -= 1
        self.vx *= 0.98  # fricción
    
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            size = max(2, int(4 * (self.lifetime / self.max_lifetime)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
    
    def is_alive(self):
        return self.lifetime > 0


def check_collision(ball, paddle):
    """Verifica colisión entre pelota y paleta"""
    ball_rect = ball.get_rect()
    paddle_rect = paddle.get_rect()
    return ball_rect.colliderect(paddle_rect)


def handle_ball_collision(ball, paddle, from_left=True):
    """Maneja colisión realista de pelota con paleta"""
    if check_collision(ball, paddle):
        # Evitar colisiones múltiples
        current_time = pygame.time.get_ticks()
        if hasattr(ball, 'last_collision_time') and current_time - ball.last_collision_time < 50:
            return False
        
        ball.last_collision_time = current_time
        
        # Posicionar la pelota fuera de la paleta
        if from_left:
            ball.x = paddle.x + paddle.width + ball.size + 2
        else:
            ball.x = paddle.x - ball.size - 2
        
        # Calcular ángulo según donde golpee la paleta (0.0 = arriba, 1.0 = abajo)
        hit_pos = (ball.y - paddle.y) / paddle.height
        hit_pos = max(0.0, min(1.0, hit_pos))  # Limitar entre 0 y 1
        
        # Convertir a ángulo (-70 a 70 grados) para mayor variedad
        angle = (hit_pos - 0.5) * 140  # rango de -70 a 70
        angle_rad = math.radians(angle)
        
        # Velocidad base aumentada con bonus según la velocidad de la paleta
        paddle_velocity = abs(paddle.velocity) if hasattr(paddle, 'velocity') else 0
        velocity_bonus = 1.0 + (paddle_velocity / paddle.max_velocity) * 0.5 if hasattr(paddle, 'max_velocity') else 1.0
        
        # Base speed + bonus
        base_speed = MAX_BALL_SPEED * 0.9 * velocity_bonus
        
        # Aplicar ángulo a la velocidad
        ball.speed_x = math.cos(angle_rad) * base_speed
        ball.speed_y = math.sin(angle_rad) * base_speed
        
        # Invertir dirección X según el lado que golpea
        if from_left:
            ball.speed_x = abs(ball.speed_x)  # Hacia la derecha
        else:
            ball.speed_x = -abs(ball.speed_x)  # Hacia la izquierda
        
        # Asegurar velocidad mínima horizontal
        min_x_speed = MAX_BALL_SPEED * 0.7
        if abs(ball.speed_x) < min_x_speed:
            ball.speed_x = min_x_speed if ball.speed_x > 0 else -min_x_speed
        
        # Limitar velocidad máxima
        speed = math.sqrt(ball.speed_x ** 2 + ball.speed_y ** 2)
        if speed > MAX_BALL_SPEED:
            ratio = MAX_BALL_SPEED / speed
            ball.speed_x *= ratio
            ball.speed_y *= ratio
        
        return True
    return False


def draw_center_line(screen):
    """Dibuja línea central punteada"""
    y = CENTER_LINE_GAP
    while y < WINDOW_HEIGHT:
        pygame.draw.line(
            screen,
            GRAY,
            (WINDOW_WIDTH // 2, y),
            (WINDOW_WIDTH // 2, y + CENTER_LINE_SEGMENT),
            2
        )
        y += CENTER_LINE_SEGMENT + CENTER_LINE_GAP


def draw_game_background(screen):
    """Dibuja fondo del juego"""
    screen.fill(BLACK)
    draw_center_line(screen)
    
    # Línea de bordes
    pygame.draw.line(screen, GRAY, (10, 10), (WINDOW_WIDTH - 10, 10), 2)
    pygame.draw.line(screen, GRAY, (10, WINDOW_HEIGHT - 10), (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10), 2)


def draw_text(screen, text, font, color, center_pos):
    """Dibuja texto centrado"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    screen.blit(text_surface, text_rect)
    return text_rect


def clamp(value, min_val, max_val):
    """Limita un valor entre mín y máx"""
    return max(min_val, min(max_val, value))


def distance(x1, y1, x2, y2):
    """Calcula distancia entre dos puntos"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def create_collision_particles(x, y, color, count=8):
    """Crea partículas de colisión"""
    particles = []
    for i in range(count):
        angle = (2 * math.pi * i) / count
        vx = math.cos(angle) * 3
        vy = math.sin(angle) * 3
        particles.append(Particle(x, y, vx, vy, color, PARTICLE_LIFETIME))
    return particles


def format_score(score):
    """Formatea puntuación para mostrar"""
    return str(score).zfill(2)


def get_asset_path(asset_type, filename):
    """Obtiene ruta de un asset"""
    if asset_type == "font":
        return os.path.join(FONTS_DIR, filename)
    elif asset_type == "sound":
        return os.path.join(SOUNDS_DIR, filename)
    elif asset_type == "image":
        return os.path.join(IMAGES_DIR, filename)
    return None
