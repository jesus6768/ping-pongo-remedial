# ============================================
# PING PONG ULTIMATE EDITION
# Sistema de IA Imbatible
# ============================================

import random
import math
from game.config import *


class AI:
    """IA con dificultades ajustables - Difícil 10%, Medio 30%, Fácil 40% de ganar"""
    
    def __init__(self, paddle, ball, difficulty=DIFFICULTY_NORMAL):
        self.paddle = paddle
        self.ball = ball
        self.difficulty = difficulty
        self.target_y = paddle.y + paddle.height // 2
        
        # Configurar parámetros según dificultad
        self._setup_difficulty_params(difficulty)
        
        # Contador para el tiempo de reacción
        self.reaction_counter = 0
    
    def predict_ball_position_advanced(self):
        """Predicción avanzada de la posición de la pelota"""
        # La IA está en paddle2 (derecha), por lo que verifica si pelota se acerca (speed_x > 0)
        # Si la pelota se aleja (speed_x < 0), no hacer nada
        if self.ball.speed_x <= 0:
            return None
        
        # Distancia desde la pelota a la paleta (paddle2 está a la derecha)
        distance_x = self.paddle.x - self.ball.x
        
        if distance_x <= 0 or abs(self.ball.speed_x) < 0.1:
            return None
        
        # Calcular tiempo hasta colisión
        time_to_collision = distance_x / abs(self.ball.speed_x)
        
        # Predecir posición Y simulando toda la trayectoria
        predicted_y = self.ball.y
        predicted_vy = self.ball.speed_y
        
        for _ in range(int(time_to_collision) + 1):
            predicted_y += predicted_vy
            
            # Simular rebotes
            if predicted_y < 0:
                predicted_y = -predicted_y
                predicted_vy = -predicted_vy
            elif predicted_y > WINDOW_HEIGHT:
                predicted_y = 2 * WINDOW_HEIGHT - predicted_y
                predicted_vy = -predicted_vy
        
        return predicted_y
    
    def update(self):
        """Actualiza posición de la IA con inteligencia y reacción según dificultad"""
        # Incrementar contador de reacción
        self.reaction_counter += 1
        
        # Si aún no ha pasado el tiempo de reacción, no hacer nada
        if self.reaction_counter < self.reaction_time:
            # Mantener movimiento con fricción
            self.paddle.velocity *= 0.9
            self.paddle.y += self.paddle.velocity
            self.paddle.y = max(0, min(WINDOW_HEIGHT - self.paddle.height, self.paddle.y))
            return
        
        # Resetear contador cuando es tiempo de reaccionar
        self.reaction_counter = 0
        
        # Predicción avanzada
        predicted_y = self.predict_ball_position_advanced()
        
        # Obtener centro actual de la paleta
        current_center = self.paddle.y + self.paddle.height // 2
        
        if predicted_y is not None:
            # Ir DIRECTAMENTE al punto predicho
            target = predicted_y
            
            # Agregar error según probabilidad y dificultad
            if random.random() < self.error_chance:
                target += random.randint(-self.prediction_error, self.prediction_error)
            
            # Calcular diferencia
            difference = target - current_center
            
            # Mover a velocidad según dificultad
            if abs(difference) > 2:
                direction = 1 if difference > 0 else -1
                # Usar velocidad ajustada por dificultad
                self.paddle.velocity = direction * self.paddle.max_velocity * self.max_speed_ratio
            else:
                # Cuando está muy cerca, micro-ajustes
                self.paddle.velocity = (difference * 0.5)
        else:
            # Pelota alejada - ir al centro más lentamente según dificultad
            center_y = WINDOW_HEIGHT // 2
            difference = center_y - current_center
            
            if abs(difference) > 10:
                direction = 1 if difference > 0 else -1
                self.paddle.velocity = direction * self.paddle.max_velocity * (self.max_speed_ratio * 0.6)
            else:
                self.paddle.velocity *= 0.5
        
        # Aplicar movimiento
        self.paddle.y += self.paddle.velocity
        self.paddle.y = max(0, min(WINDOW_HEIGHT - self.paddle.height, self.paddle.y))
    
    
    def _setup_difficulty_params(self, difficulty):
        """Configura los parámetros de IA según la dificultad seleccionada"""
        if difficulty == DIFFICULTY_HARD:  # 10% de ganar (casi imposible)
            self.reaction_time = 0
            self.max_speed_ratio = 1.15  # Muy rápido
            self.prediction_error = 3    # Casi sin error
            self.error_chance = 0.005    # Casi nunca falla (0.5%)
        
        elif difficulty == DIFFICULTY_NORMAL:  # 30% de ganar (moderado)
            self.reaction_time = 2        # Pequeña demora
            self.max_speed_ratio = 0.95   # Velocidad normal
            self.prediction_error = 15    # Error moderado
            self.error_chance = 0.15      # Falla 15% de las veces
        
        elif difficulty == DIFFICULTY_EASY:  # 40% de ganar (fácil)
            self.reaction_time = 5        # Demora notable
            self.max_speed_ratio = 0.75   # Velocidad lenta
            self.prediction_error = 30    # Error significativo
            self.error_chance = 0.30      # Falla 30% de las veces
    
    def set_difficulty(self, difficulty):
        """Cambia la dificultad de la IA"""
        self.difficulty = difficulty
        self._setup_difficulty_params(difficulty)
