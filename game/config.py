# ============================================
# PING PONG ULTIMATE EDITION
# Configuraciones y Constantes Globales
# ============================================

import pygame
import os

# ============ RESOLUCIÓN ============
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# ============ COLORES ============
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 100)
NEON_GREEN = (0, 255, 127)
CYAN = (0, 255, 255)
BLUE = (0, 150, 255)
PURPLE = (200, 0, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# ============ VELOCIDADES ============
BALL_SPEED = 9
PADDLE_SPEED = 8
MAX_BALL_SPEED = 18
BALL_ACCELERATION = 1.02

# ============ TAMAÑOS ============
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
BALL_SIZE = 8
CENTER_LINE_SEGMENT = 10
CENTER_LINE_GAP = 10

# ============ PHYSICS ============
BALL_FRICTION = 0.99
PADDLE_HITBOX_EXTRA = 5

# ============ PUNTUACIÓN ============
MAX_SCORE = 21
POINTS_PER_GOAL = 1

# ============ MODOS DE JUEGO ============
MODE_SINGLE_PLAYER = "single"
MODE_LOCAL_MULTIPLAYER = "local"
MODE_ONLINE = "online"

# ============ DIFICULTADES IA ============
DIFFICULTY_EASY = "easy"
DIFFICULTY_NORMAL = "normal"
DIFFICULTY_HARD = "hard"

# ============ PATHS ============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# ============ NETWORK ============
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5555
NETWORK_TIMEOUT = 5
BUFFER_SIZE = 4096

# ============ ANIMACIÓN ============
MENU_TRANSITION_SPEED = 300
PARTICLE_LIFETIME = 30

# ============ ESTADOS ============
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_WAITING = "waiting"
