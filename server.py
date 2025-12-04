# ============================================
# PING PONG ULTIMATE EDITION
# Servidor Multijugador
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.network import NetworkServer
from game.config import DEFAULT_HOST, DEFAULT_PORT
import signal


def signal_handler(sig, frame):
    """Maneja Ctrl+C"""
    print("\n[SERVIDOR] Recibida señal de cierre...")
    global server
    if 'server' in globals():
        server.stop()
    sys.exit(0)


def main():
    """Función principal del servidor"""
    global server
    
    print("=" * 50)
    print("PING PONG ULTIMATE - SERVIDOR MULTIJUGADOR")
    print("=" * 50)
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    # Crear e iniciar servidor
    server = NetworkServer(host=DEFAULT_HOST, port=DEFAULT_PORT)
    
    if server.start():
        print(f"\n✓ Servidor escuchando en {DEFAULT_HOST}:{DEFAULT_PORT}")
        print("Esperando 2 jugadores para iniciar...\n")
        
        # Mantener el servidor corriendo
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        print("✗ Error al iniciar el servidor")
        sys.exit(1)


if __name__ == "__main__":
    main()
