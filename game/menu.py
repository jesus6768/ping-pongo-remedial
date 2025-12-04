# ============================================
# PING PONG ULTIMATE EDITION
# Sistema de Menú
# ============================================

import pygame
import socket
from game.config import *


def get_local_ip():
    """Obtiene la IP local de la computadora"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


class Menu:
    """Menú principal del juego"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 96)
        self.font_option = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.selected_option = 0
        self.options = [
            {"text": "1 JUGADOR vs IA", "action": "single"},
            {"text": "2 JUGADORES LOCAL", "action": "local"},
            {"text": "MULTIJUGADOR ONLINE", "action": "online"},
            {"text": "SALIR", "action": "quit"}
        ]
        self.animation_offset = 0
        self.animation_direction = 1
    
    def draw(self):
        """Dibuja el menú"""
        self.screen.fill(BLACK)
        
        # Efecto de animación del fondo
        self.animation_offset += self.animation_direction
        if self.animation_offset >= 10 or self.animation_offset <= -10:
            self.animation_direction *= -1
        
        # Líneas de decoración animadas
        for i in range(5):
            y = 20 + i * 50 + self.animation_offset
            pygame.draw.line(self.screen, GRAY, (50, y), (WINDOW_WIDTH - 50, y), 1)
        
        # Título
        title = self.font_title.render("PING-PONG", True, NEON_GREEN)
        subtitle = self.font_title.render("ULTIMATE", True, CYAN)
        
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 180))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Versión
        version = self.font_small.render("v1.0 - EDITION", True, GRAY)
        version_rect = version.get_rect(center=(WINDOW_WIDTH // 2, 240))
        self.screen.blit(version, version_rect)
        
        # Línea separadora
        pygame.draw.line(self.screen, NEON_GREEN, (100, 260), (WINDOW_WIDTH - 100, 260), 2)
        
        # Opciones del menú
        option_start_y = 320
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_option
            color = NEON_GREEN if is_selected else WHITE
            
            # Efecto de parpadeo en opción seleccionada
            if is_selected:
                current_time = pygame.time.get_ticks()
                if (current_time // 200) % 2 == 0:
                    color = YELLOW
            
            option_text = self.font_option.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, option_start_y + i * 70))
            
            # Dibuja selector
            if is_selected:
                pygame.draw.rect(self.screen, color, 
                               (option_rect.x - 20, option_rect.y - 10, 
                                option_rect.width + 40, option_rect.height + 20), 3)
            
            self.screen.blit(option_text, option_rect)
        
        # Instrucciones
        instructions = self.font_small.render("↑/↓ Seleccionar | ENTER Confirmar", True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(instructions, instructions_rect)
    
    def handle_input(self, event):
        """Maneja entrada del usuario"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
                return None
            
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
                return None
            
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]["action"]
        
        return None
    
    def reset(self):
        """Reinicia el menú"""
        self.selected_option = 0
        self.animation_offset = 0


class DifficultyMenu:
    """Menú de selección de dificultad"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_option = pygame.font.Font(None, 48)
        
        self.selected_option = 0
        self.options = [
            {"text": "FÁCIL", "difficulty": DIFFICULTY_EASY},
            {"text": "NORMAL", "difficulty": DIFFICULTY_NORMAL},
            {"text": "DIFÍCIL", "difficulty": DIFFICULTY_HARD}
        ]
    
    def draw(self):
        """Dibuja menú de dificultad"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_title.render("SELECCIONA DIFICULTAD", True, NEON_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Opciones
        option_start_y = 280
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_option
            color = NEON_GREEN if is_selected else WHITE
            
            option_text = self.font_option.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, option_start_y + i * 80))
            
            if is_selected:
                pygame.draw.rect(self.screen, color, 
                               (option_rect.x - 20, option_rect.y - 10,
                                option_rect.width + 40, option_rect.height + 20), 3)
            
            self.screen.blit(option_text, option_rect)
    
    def handle_input(self, event):
        """Maneja entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]["difficulty"]
        
        return None
    
    def reset(self):
        """Reinicia el menú"""
        self.selected_option = 0


class ScoreMenu:
    """Menú para seleccionar el puntuaje máximo de la partida"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_option = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.selected_option = 0
        self.options = [
            {"text": "5 PUNTOS", "score": 5},
            {"text": "11 PUNTOS", "score": 11},
            {"text": "15 PUNTOS", "score": 15},
            {"text": "21 PUNTOS", "score": 21},
            {"text": "PERSONALIZADO", "score": None}
        ]
        self.custom_score = 11
    
    def draw(self):
        """Dibuja menú de puntuaje"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_title.render("SELECCIONA PUNTUAJE", True, NEON_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Opciones
        option_start_y = 220
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_option
            color = NEON_GREEN if is_selected else WHITE
            
            option_text = self.font_option.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, option_start_y + i * 70))
            
            if is_selected:
                pygame.draw.rect(self.screen, color, 
                               (option_rect.x - 20, option_rect.y - 10,
                                option_rect.width + 40, option_rect.height + 20), 3)
            
            self.screen.blit(option_text, option_rect)
        
        # Instrucciones
        instructions = self.font_small.render("↑/↓ Seleccionar | ENTER Confirmar", True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(instructions, instructions_rect)
    
    def handle_input(self, event):
        """Maneja entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                score = self.options[self.selected_option]["score"]
                if score is None:
                    return "custom"
                return score
        
        return None
    
    def reset(self):
        """Reinicia el menú"""
        self.selected_option = 0


class OnlineRoleMenu:
    """Menú para seleccionar rol en multijugador (HOST o CLIENTE)"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)
        self.font_option = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.selected_option = 0
        self.local_ip = get_local_ip()
        self.options = [
            {"text": "SER HOST (SERVIDOR)", "role": "host"},
            {"text": "UNIRSE A PARTIDA", "role": "client"}
        ]
    
    def draw(self):
        """Dibuja menú de selección de rol"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_title.render("MULTIJUGADOR ONLINE", True, NEON_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Mostrar IP local
        ip_text = self.font_small.render(f"Tu IP: {self.local_ip}", True, CYAN)
        ip_rect = ip_text.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(ip_text, ip_rect)
        
        # Línea separadora
        pygame.draw.line(self.screen, GRAY, (100, 200), (WINDOW_WIDTH - 100, 200), 1)
        
        # Opciones
        option_start_y = 280
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_option
            color = NEON_GREEN if is_selected else WHITE
            
            option_text = self.font_option.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, option_start_y + i * 100))
            
            if is_selected:
                pygame.draw.rect(self.screen, color, 
                               (option_rect.x - 20, option_rect.y - 10,
                                option_rect.width + 40, option_rect.height + 20), 3)
            
            self.screen.blit(option_text, option_rect)
        
        # Instrucciones
        instructions = self.font_small.render("↑/↓ Seleccionar | ENTER Confirmar | ESC Atrás", True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(instructions, instructions_rect)
    
    def handle_input(self, event):
        """Maneja entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]["role"]
            elif event.key == pygame.K_ESCAPE:
                return "back"
        
        return None
    
    def reset(self):
        """Reinicia el menú"""
        self.selected_option = 0
