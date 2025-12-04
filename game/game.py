# ============================================
# PING PONG ULTIMATE EDITION
# Motor Principal del Juego
# ============================================

import pygame
import math
from game.config import *
from game.ball import Ball
from game.paddle import Paddle
from game.scoreboard import Scoreboard
from game.ai import AI
from game.utils import *


class Game:
    """Clase principal del juego"""
    
    def __init__(self, mode=MODE_SINGLE_PLAYER, difficulty=DIFFICULTY_NORMAL, max_score=MAX_SCORE):
        self.mode = mode
        self.difficulty = difficulty
        self.max_score = max_score
        self.screen = None
        self.clock = None
        self.running = True
        self.game_active = True
        self.paused = False
        
        # Componentes del juego
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.paddle1 = Paddle(20, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle2 = Paddle(WINDOW_WIDTH - 20 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.scoreboard = Scoreboard(max_score=max_score)
        
        # IA y efectos
        self.ai = None
        self.particles = []
        self.countdown = 0
        self.font_large = pygame.font.Font(None, 120)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        if mode == MODE_SINGLE_PLAYER:
            self.ai = AI(self.paddle2, self.ball, difficulty=difficulty)
    
    def init_display(self, screen, clock):
        """Inicializa la pantalla"""
        self.screen = screen
        self.clock = clock
    
    def handle_events(self):
        """Maneja eventos del usuario"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_active = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_active = False
                
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
    
    def update(self):
        """Actualiza lógica del juego"""
        if self.paused:
            return
        
        # Input del jugador 1
        keys = pygame.key.get_pressed()
        self.paddle1.update(keys=keys)
        
        # Input del jugador 2 o IA
        if self.mode == MODE_SINGLE_PLAYER:
            self.ai.update()
        elif self.mode == MODE_LOCAL_MULTIPLAYER:
            # W/S para jugador 2
            local_keys = {
                pygame.K_w: keys[pygame.K_w],
                pygame.K_s: keys[pygame.K_s],
                pygame.K_UP: keys[pygame.K_UP],
                pygame.K_DOWN: keys[pygame.K_DOWN]
            }
            if local_keys[pygame.K_w]:
                self.paddle2.y = max(0, self.paddle2.y - PADDLE_SPEED)
            if local_keys[pygame.K_s]:
                self.paddle2.y = min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.paddle2.y + PADDLE_SPEED)
        
        # Actualizar pelota
        self.ball.update()
        
        # Colisiones con paletas
        if handle_ball_collision(self.ball, self.paddle1, from_left=True):
            # Crear partículas
            self.particles.extend(create_collision_particles(
                self.ball.x, self.ball.y, GREEN, count=12
            ))
        
        if handle_ball_collision(self.ball, self.paddle2, from_left=False):
            # Crear partículas
            self.particles.extend(create_collision_particles(
                self.ball.x, self.ball.y, BLUE, count=12
            ))
        
        # Verificar puntos
        if self.ball.x < 0:
            self.scoreboard.update_score(2)
            self.ball.reset()
            self.countdown = FPS  # Pequeña pausa antes de continuar
        
        elif self.ball.x > WINDOW_WIDTH:
            self.scoreboard.update_score(1)
            self.ball.reset()
            self.countdown = FPS
        
        # Actualizar partículas
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
        
        # Countdown
        if self.countdown > 0:
            self.countdown -= 1
    
    def draw(self):
        """Dibuja todo en pantalla"""
        draw_game_background(self.screen)
        
        # Dibujar pelota
        self.ball.draw(self.screen)
        
        # Dibujar paletas
        self.paddle1.draw(self.screen, color=GREEN if self.mode == MODE_SINGLE_PLAYER else NEON_GREEN)
        self.paddle2.draw(self.screen, color=BLUE)
        
        # Dibujar puntuación
        self.scoreboard.draw(self.screen)
        
        # Dibujar partículas
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Dibujar pausa
        if self.paused:
            self._draw_pause_screen()
        
        # Dibujar countdown
        if self.countdown > 0:
            alpha = int(255 * (self.countdown / FPS))
            size_multiplier = 1 + (1 - self.countdown / FPS) * 0.5
            countdown_text = self.font_large.render("", True, WHITE)
            countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(countdown_text, countdown_rect)
        
        pygame.display.flip()
    
    def _draw_pause_screen(self):
        """Dibuja pantalla de pausa"""
        # Overlay semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        pause_text = self.font_large.render("PAUSA", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instrucciones
        resume_text = self.font_small.render("ESPACIO para continuar | ESC para salir", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def run(self):
        """Loop principal del juego"""
        self.game_active = True
        
        while self.running and self.game_active:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
            if self.scoreboard.is_game_over():
                self.show_game_over()
                self.game_active = False
    
    def show_game_over(self):
        """Muestra pantalla de fin del juego"""
        waiting = True
        font_title = pygame.font.Font(None, 96)
        font_text = pygame.font.Font(None, 48)
        
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        waiting = False
            
            # Dibujar
            draw_game_background(self.screen)
            
            # Overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Textos
            title = font_title.render("¡GAME OVER!", True, YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            self.screen.blit(title, title_rect)
            
            winner = self.scoreboard.get_winner()
            if winner:
                winner_color = GREEN if "1" in winner else BLUE
                winner_text = font_title.render(f"{winner}", True, winner_color)
                winner_text += font_text.render("¡GANA!", True, winner_color)
                winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
                self.screen.blit(winner_text, winner_rect)
                
                # Score final
                score_text = font_text.render(
                    f"{self.scoreboard.player1_score} - {self.scoreboard.player2_score}",
                    True, WHITE
                )
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
                self.screen.blit(score_text, score_rect)
            
            # Instrucciones
            instr_text = font_text.render("ENTER para volver al menú", True, GRAY)
            instr_rect = instr_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            self.screen.blit(instr_text, instr_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def reset(self):
        """Reinicia el juego"""
        self.ball.reset()
        self.paddle1.reset()
        self.paddle2.reset()
        self.scoreboard.reset()
        self.particles = []
        self.paused = False
        self.game_active = False
