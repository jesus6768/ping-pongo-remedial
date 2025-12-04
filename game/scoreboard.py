# ============================================
# PING PONG ULTIMATE EDITION
# Sistema de Puntuación
# ============================================

import pygame
from game.config import *


class Scoreboard:
    """Gestiona la puntuación del juego"""
    
    def __init__(self, max_score=MAX_SCORE):
        self.player1_score = 0
        self.player2_score = 0
        self.max_score = max_score
        self.font_large = pygame.font.Font(None, 120)
        self.font_small = pygame.font.Font(None, 32)
        self.last_scorer = None
        self.last_score_time = 0
    
    def update_score(self, player):
        """Actualiza puntuación de un jugador"""
        if player == 1:
            self.player1_score += POINTS_PER_GOAL
            self.last_scorer = 1
        elif player == 2:
            self.player2_score += POINTS_PER_GOAL
            self.last_scorer = 2
        
        self.last_score_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        """Dibuja la puntuación en pantalla"""
        # Puntuación grande
        p1_text = self.font_large.render(str(self.player1_score).zfill(2), True, GREEN)
        p2_text = self.font_large.render(str(self.player2_score).zfill(2), True, BLUE)
        
        # Posicionar puntuaciones
        p1_rect = p1_text.get_rect(center=(WINDOW_WIDTH // 4, 60))
        p2_rect = p2_text.get_rect(center=(3 * WINDOW_WIDTH // 4, 60))
        
        screen.blit(p1_text, p1_rect)
        screen.blit(p2_text, p2_rect)
        
        # Dibuja separador
        pygame.draw.line(screen, GRAY, (WINDOW_WIDTH // 2 - 20, 40), 
                        (WINDOW_WIDTH // 2 + 20, 40), 2)
        
        # Indicador de último punto
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_time < 1000:
            flash_alpha = 200 if (current_time // 100) % 2 == 0 else 100
            if self.last_scorer == 1:
                pygame.draw.circle(screen, GREEN, (WINDOW_WIDTH // 4, 60), 80, 3)
            elif self.last_scorer == 2:
                pygame.draw.circle(screen, BLUE, (3 * WINDOW_WIDTH // 4, 60), 80, 3)
    
    def draw_match_score(self, screen):
        """Dibuja puntuación pequeña (útil para matches)"""
        score_text = self.font_small.render(f"{self.player1_score} - {self.player2_score}", 
                                            True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        screen.blit(score_text, score_rect)
    
    def reset(self):
        """Reinicia la puntuación"""
        self.player1_score = 0
        self.player2_score = 0
        self.last_scorer = None
        self.last_score_time = 0
    
    def is_game_over(self):
        """Verifica si el juego ha terminado"""
        return self.player1_score >= self.max_score or self.player2_score >= self.max_score
    
    def get_winner(self):
        """Retorna el nombre del ganador"""
        if self.player1_score >= MAX_SCORE:
            return "JUGADOR 1"
        elif self.player2_score >= MAX_SCORE:
            return "JUGADOR 2"
        return None
    
    def get_leading_player(self):
        """Retorna el jugador que va ganando"""
        if self.player1_score > self.player2_score:
            return 1
        elif self.player2_score > self.player1_score:
            return 2
        return 0  # Empate
    
    def get_score_difference(self):
        """Retorna diferencia de puntos"""
        return abs(self.player1_score - self.player2_score)
