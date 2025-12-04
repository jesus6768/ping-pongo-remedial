import pygame
import sys
from game.config import *
from game.menu import Menu, DifficultyMenu, ScoreMenu, OnlineRoleMenu
from game.game import Game
from game.network import NetworkClient


def init_pygame():
    """Inicializa Pygame"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PING PONG ULTIMATE EDITION")
    
    # Icono (si existe)
    # try:
    #     icon = pygame.image.load("assets/images/icon.png")
    #     pygame.display.set_icon(icon)
    # except:
    #     pass
    
    return screen


def show_single_player_menu(screen, clock):
    """Menú para seleccionar dificultad en modo 1 jugador"""
    difficulty_menu = DifficultyMenu(screen)
    selected = None
    
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                selected = difficulty_menu.handle_input(event)
        
        difficulty_menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    return selected


def show_score_menu(screen, clock):
    """Menú para seleccionar puntuaje máximo"""
    score_menu = ScoreMenu(screen)
    selected = None
    
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                result = score_menu.handle_input(event)
                if result == "custom":
                    # Menú para ingresar puntuaje personalizado
                    custom_score = show_custom_score_input(screen, clock)
                    if custom_score:
                        selected = custom_score
                else:
                    selected = result
        
        score_menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    return selected


def show_custom_score_input(screen, clock):
    """Menú para ingresar puntuaje personalizado"""
    font_title = pygame.font.Font(None, 72)
    font_input = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    score_input = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                
                elif event.key == pygame.K_RETURN:
                    if score_input and score_input.isdigit():
                        score = int(score_input)
                        if 1 <= score <= 999:
                            return score
                
                elif event.key == pygame.K_BACKSPACE:
                    score_input = score_input[:-1]
                
                elif event.unicode.isdigit():
                    if len(score_input) < 3:
                        score_input += event.unicode
        
        screen.fill(BLACK)
        
        title = font_title.render("PUNTUAJE PERSONALIZADO", True, NEON_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        input_text = font_input.render(score_input or "0", True, NEON_GREEN)
        input_rect = input_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        pygame.draw.rect(screen, NEON_GREEN, (input_rect.x - 20, input_rect.y - 10, input_rect.width + 40, input_rect.height + 20), 3)
        screen.blit(input_text, input_rect)
        
        info = font_small.render("Ingresa un número entre 1 y 999", True, GRAY)
        info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, 350))
        screen.blit(info, info_rect)
        
        instructions = font_small.render("ENTER: confirmar | ESC: cancelar", True, GRAY)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(FPS)


def show_online_role_menu(screen, clock):
    """Menú para seleccionar si ser HOST o CLIENTE"""
    role_menu = OnlineRoleMenu(screen)
    selected = None
    
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                result = role_menu.handle_input(event)
                if result == "back":
                    return None
                selected = result
        
        role_menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    return selected


def show_online_menu(screen, clock):
    """Menú para multijugador online - Conexión intuitiva y con click en campos"""
    font_title = pygame.font.Font(None, 64)
    font_label = pygame.font.Font(None, 36)
    font_input = pygame.font.Font(None, 42)
    font_small = pygame.font.Font(None, 28)
    font_tiny = pygame.font.Font(None, 24)

    host = ""
    port = str(DEFAULT_PORT)
    input_mode = "host"  # "host" o "port"
    status_message = ""
    status_time = 0

    while True:
        # Calcular posiciones (necesarias para detectar clicks)
        host_section_y = 120
        host_input_rect_area = pygame.Rect(50, host_section_y + 85, 750, 60)
        port_section_y = host_section_y + 230
        port_input_rect_area = pygame.Rect(50, port_section_y + 85, 750, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                elif event.key == pygame.K_TAB:
                    input_mode = "port" if input_mode == "host" else "host"

                elif event.key == pygame.K_RETURN:
                    # Si el puerto es válido intentar conectar. Si la IP está vacía, usar localhost
                    try:
                        port_int = int(port)
                        if not (1 <= port_int <= 65535):
                            raise ValueError("Puerto fuera de rango")
                        if not host:
                            host = "127.0.0.1"
                            status_message = "Usando localhost (127.0.0.1) porque no ingresaste IP"
                            status_time = pygame.time.get_ticks()
                        return host, port_int
                    except Exception:
                        status_message = "Puerto inválido. Ingresa un número entre 1 y 65535"
                        status_time = pygame.time.get_ticks()

                elif event.key == pygame.K_BACKSPACE:
                    if input_mode == "host" and len(host) > 0:
                        host = host[:-1]
                    elif input_mode == "port" and len(port) > 0:
                        port = port[:-1]

                elif event.unicode.isprintable():
                    if input_mode == "host" and len(host) < 45:
                        host += event.unicode
                    elif input_mode == "port" and event.unicode.isdigit() and len(port) < 6:
                        port += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Cambiar foco si hace click en los rectángulos
                if host_input_rect_area.collidepoint(mx, my):
                    input_mode = "host"
                elif port_input_rect_area.collidepoint(mx, my):
                    input_mode = "port"

        # Dibujar fondo
        screen.fill(BLACK)

        # Título
        title = font_title.render("UNIRSE A SERVIDOR", True, NEON_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
        screen.blit(title, title_rect)

        # ============ SECCIÓN HOST (IP) ============
        host_label = font_label.render("Dirección IP:", True, WHITE)
        host_label_rect = host_label.get_rect(topleft=(50, host_section_y))
        screen.blit(host_label, host_label_rect)

        # Ejemplo de IP
        example_text = font_tiny.render("Ejemplo: 192.168.1.102  o  127.0.0.1", True, GRAY)
        example_rect = example_text.get_rect(topleft=(50, host_section_y + 40))
        screen.blit(example_text, example_rect)

        # Input para IP (texto y rectángulo interactivo)
        host_color = NEON_GREEN if input_mode == "host" else GRAY
        pygame.draw.rect(screen, host_color, host_input_rect_area, 3)
        host_input_text = font_input.render(host or "Ingresa la IP aquí", True, host_color)
        host_input_text_rect = host_input_text.get_rect(topleft=(host_input_rect_area.x + 8, host_input_rect_area.y + 8))
        screen.blit(host_input_text, host_input_text_rect)

        # Explicación
        explanation = font_small.render("→ Pídele al anfitrión (HOST) la dirección IP que aparece en su pantalla", True, CYAN)
        explanation_rect = explanation.get_rect(topleft=(50, host_section_y + 160))
        screen.blit(explanation, explanation_rect)

        # ============ SECCIÓN PUERTO ============
        port_label = font_label.render("Puerto:", True, WHITE)
        port_label_rect = port_label.get_rect(topleft=(50, port_section_y))
        screen.blit(port_label, port_label_rect)

        # Ejemplo de puerto
        port_example = font_tiny.render(f"Ejemplo: {DEFAULT_PORT}  (normalmente es {DEFAULT_PORT})", True, GRAY)
        port_example_rect = port_example.get_rect(topleft=(50, port_section_y + 40))
        screen.blit(port_example, port_example_rect)

        # Input para puerto (texto y rectángulo interactivo)
        port_color = NEON_GREEN if input_mode == "port" else GRAY
        pygame.draw.rect(screen, port_color, port_input_rect_area, 3)
        port_input_text = font_input.render(port, True, port_color)
        port_input_text_rect = port_input_text.get_rect(topleft=(port_input_rect_area.x + 8, port_input_rect_area.y + 8))
        screen.blit(port_input_text, port_input_text_rect)

        # Mensaje de estado/errores temporal
        if status_message and pygame.time.get_ticks() - status_time < 4000:
            status_txt = font_small.render(status_message, True, NEON_GREEN if "Usando localhost" in status_message else RED)
            status_rect = status_txt.get_rect(topleft=(50, port_section_y + 160))
            screen.blit(status_txt, status_rect)

        # ============ INSTRUCCIONES ============
        instructions_y = WINDOW_HEIGHT - 80

        tab_text = font_small.render("TAB: Cambiar entre IP y Puerto | Click: seleccionar campo", True, NEON_GREEN)
        tab_rect = tab_text.get_rect(topleft=(50, instructions_y))
        screen.blit(tab_text, tab_rect)

        enter_text = font_small.render("ENTER: Conectar (si no pones IP usa localhost)", True, GREEN)
        enter_rect = enter_text.get_rect(topleft=(50, instructions_y + 35))
        screen.blit(enter_text, enter_rect)

        esc_text = font_small.render("ESC: Volver al menú", True, RED)
        esc_rect = esc_text.get_rect(topleft=(WINDOW_WIDTH - 350, instructions_y))
        screen.blit(esc_text, esc_rect)

        # Estado actual
        if input_mode == "host":
            current_mode = "↓ Editando IP ↓"
            current_color = NEON_GREEN
        else:
            current_mode = "↓ Editando Puerto ↓"
            current_color = NEON_GREEN

        mode_text = font_small.render(current_mode, True, current_color)
        mode_rect = mode_text.get_rect(center=(WINDOW_WIDTH // 2, instructions_y + 35))
        screen.blit(mode_text, mode_rect)

        pygame.display.flip()
        clock.tick(FPS)
def play_single_player(screen, clock):
    """Inicia modo 1 jugador"""
    difficulty = show_single_player_menu(screen, clock)
    
    if difficulty is None:
        return
    
    max_score = show_score_menu(screen, clock)
    
    if max_score is None:
        return
    
    game = Game(mode=MODE_SINGLE_PLAYER, difficulty=difficulty, max_score=max_score)
    game.init_display(screen, clock)
    game.run()


def play_local_multiplayer(screen, clock):
    """Inicia modo 2 jugadores local"""
    max_score = show_score_menu(screen, clock)
    
    if max_score is None:
        return
    
    game = Game(mode=MODE_LOCAL_MULTIPLAYER, max_score=max_score)
    game.init_display(screen, clock)
    game.run()


def play_online(screen, clock):
    """Inicia modo multijugador online"""
    role = show_online_role_menu(screen, clock)
    
    if role is None:
        return
    
    if role == "host":
        # Modo HOST
        print("[ANFITRIÓN] Iniciando servidor local...")
        from game.network import NetworkServer
        
        server = NetworkServer(host="0.0.0.0", port=DEFAULT_PORT)
        
        if not server.start():
            show_error_message(screen, clock, "Error al iniciar el servidor")
            return
        
        # Esperar a que se conecte un cliente y luego iniciar el juego
        show_waiting_host_message(screen, clock, server)
        
        server.stop()
    
    else:  # role == "client"
        # Modo CLIENTE
        connection_info = show_online_menu(screen, clock)
        
        if connection_info is None:
            return
        
        host, port = connection_info
        
        # Conectar al servidor
        client = NetworkClient(host=host, port=port)
        
        show_connecting_message(screen, clock, host, port, client)
        
        if client.is_connected():
            # TODO: Iniciar juego como cliente
            print(f"[CLIENTE] Conectado como Jugador {client.player_id}")
            pygame.time.wait(2000)
            client.disconnect()
        else:
            show_error_message(screen, clock, "No se pudo conectar al servidor")


def show_connecting_message(screen, clock, host, port, client):
    """Muestra pantalla de conexión"""
    font = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    connecting = True
    error_msg = None
    max_attempts = 0
    
    while connecting and max_attempts < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    client.disconnect()
                    return
        
        screen.fill(BLACK)
        
        if not client.is_connected() and max_attempts == 0:
            success = client.connect()
            max_attempts = 1
            if not success:
                error_msg = "No se pudo conectar al servidor"
        
        if client.is_connected():
            msg = f"✓ Conectado como Jugador {client.player_id}"
            msg_color = GREEN
            msg_text = "Esperando al otro jugador..."
            connecting = False
        elif error_msg:
            msg = f"✗ Error: {error_msg}"
            msg_color = RED
            msg_text = "ESC para volver"
        else:
            msg = f"Conectando a {host}:{port}..."
            msg_color = CYAN
            msg_text = "ESC para cancelar"
        
        text1 = font.render(msg, True, msg_color)
        text1_rect = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(text1, text1_rect)
        
        if msg_text:
            text2 = font_small.render(msg_text, True, GRAY)
            text2_rect = text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            screen.blit(text2, text2_rect)
        
        pygame.display.flip()
        clock.tick(FPS)


def show_waiting_message(screen, clock, message):
    """Muestra pantalla de espera"""
    font = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    for _ in range(int(FPS * 5)):  # Esperar 5 segundos o hasta que el usuario presione ESC
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        screen.fill(BLACK)
        
        text = font.render(message, True, CYAN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        
        # Animación de puntos
        dots = "." * ((pygame.time.get_ticks() // 300) % 4)
        dots_text = font_small.render(f"Esperando{dots}", True, GRAY)
        dots_rect = dots_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(dots_text, dots_rect)
        
        pygame.display.flip()
        clock.tick(FPS)


def show_waiting_host_message(screen, clock, server):
    """Muestra pantalla de espera en modo HOST y monitorea conexiones"""
    font = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    import socket
    
    # Obtener IP local
    try:
        # Para obtener la IP local sin depender de internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"
    
    start_time = pygame.time.get_ticks()
    max_wait_time = 60000  # 60 segundos de espera máximo
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        screen.fill(BLACK)
        
        # Verificar si un cliente se ha conectado
        if server.get_connected_clients() >= 1:
            title = font.render("✓ Jugador conectado", True, GREEN)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            screen.blit(title, title_rect)
            
            msg = font_small.render(f"Jugadores: {server.get_connected_clients()} / 2", True, CYAN)
            msg_rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(msg, msg_rect)
            
            if server.get_connected_clients() >= 2:
                # Ambos jugadores conectados
                start_msg = font_small.render("¡Iniciando juego!", True, GREEN)
                start_rect = start_msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
                screen.blit(start_msg, start_rect)
                pygame.display.flip()
                clock.tick(FPS)
                pygame.time.wait(2000)
                return
        else:
            title = font.render("Esperando jugador...", True, CYAN)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            screen.blit(title, title_rect)
            
            # Animación de puntos
            dots = "." * ((pygame.time.get_ticks() // 300) % 4)
            waiting_text = font_small.render(f"Esperando{dots}", True, GRAY)
            waiting_rect = waiting_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(waiting_text, waiting_rect)
        
        # Mostrar dirección IP
        ip_text = font_small.render(f"IP: {local_ip}:{DEFAULT_PORT}", True, NEON_GREEN)
        ip_rect = ip_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        screen.blit(ip_text, ip_rect)
        
        # Instrucciones
        escape_text = font_small.render("ESC: cancelar", True, GRAY)
        escape_rect = escape_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(escape_text, escape_rect)
        
        # Verificar timeout
        if pygame.time.get_ticks() - start_time > max_wait_time:
            show_error_message(screen, clock, "Tiempo de espera agotado")
            return
        
        pygame.display.flip()
        clock.tick(FPS)
def show_error_message(screen, clock, error):
    """Muestra un mensaje de error"""
    font = pygame.font.Font(None, 48)
    
    for _ in range(int(FPS * 3)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                return
        
        screen.fill(BLACK)
        
        text = font.render(f"✗ {error}", True, RED)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Función principal"""
    screen = init_pygame()
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    running = True
    
    print("=" * 50)
    print("PING PONG ULTIMATE EDITION - Iniciando...")
    print("=" * 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                action = menu.handle_input(event)
                
                if action == "single":
                    play_single_player(screen, clock)
                    menu.reset()
                
                elif action == "local":
                    play_local_multiplayer(screen, clock)
                    menu.reset()
                
                elif action == "online":
                    play_online(screen, clock)
                    menu.reset()
                
                elif action == "quit":
                    running = False
        
        menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    print("\nGracias por jugar PING PONG ULTIMATE EDITION!")
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
