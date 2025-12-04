# ============================================
# PING PONG ULTIMATE EDITION
# Sistema de Red para Multijugador
# ============================================

import socket
import pickle
import threading
import time
from game.config import *


class NetworkClient:
    """Cliente de red para multijugador online"""
    
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.player_id = None
        self.receive_thread = None
        self.running = False
        self.last_data = None
        self.lock = threading.Lock()
    
    def connect(self):
        """Conecta al servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(NETWORK_TIMEOUT)
            self.socket.connect((self.host, self.port))
            
            # Recibir ID del jugador
            self.player_id = pickle.loads(self.socket.recv(BUFFER_SIZE))
            
            self.connected = True
            self.running = True
            
            # Iniciar thread de recepción
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            return True
        
        except socket.timeout:
            print(f"Error: Conexión expirada a {self.host}:{self.port}")
            self.connected = False
            return False
        except ConnectionRefusedError:
            print(f"Error: Servidor no disponible en {self.host}:{self.port}")
            self.connected = False
            return False
        except Exception as e:
            print(f"Error de conexión: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Desconecta del servidor"""
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def send_data(self, data):
        """Envía datos al servidor"""
        if not self.connected:
            return False
        
        try:
            self.socket.sendall(pickle.dumps(data))
            return True
        except Exception as e:
            print(f"Error enviando datos: {e}")
            self.connected = False
            return False
    
    def get_data(self):
        """Obtiene datos recibidos"""
        with self.lock:
            data = self.last_data
            self.last_data = None
        return data
    
    def _receive_loop(self):
        """Loop de recepción en thread separado"""
        while self.running and self.connected:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                if data:
                    with self.lock:
                        self.last_data = pickle.loads(data)
                else:
                    self.connected = False
                    break
            
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error recibiendo datos: {e}")
                self.connected = False
                break
    
    def is_connected(self):
        """Verifica si está conectado"""
        return self.connected and self.socket is not None


class NetworkServer:
    """Servidor de red para multijugador"""
    
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.accept_thread = None
    
    def start(self):
        """Inicia el servidor"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)
            
            self.running = True
            
            # Thread para aceptar conexiones
            self.accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            self.accept_thread.start()
            
            print(f"[SERVIDOR] Iniciado en {self.host}:{self.port}")
            return True
        
        except OSError as e:
            print(f"Error iniciando servidor: {e}")
            self.running = False
            return False
    
    def _accept_connections(self):
        """Acepta conexiones de clientes"""
        player_counter = 1
        self.server_socket.settimeout(1.0)  # Timeout de 1 segundo
        
        while self.running and len(self.clients) < 2:
            try:
                client_socket, address = self.server_socket.accept()
                player_id = player_counter
                player_counter += 1
                
                # Enviar ID al cliente
                client_socket.send(pickle.dumps(player_id))
                
                # Guardar cliente
                self.clients[player_id] = {
                    "socket": client_socket,
                    "address": address,
                    "data": None
                }
                
                print(f"[SERVIDOR] Jugador {player_id} conectado desde {address}")
                
                # Si hay 2 jugadores, iniciar el loop de juego
                if len(self.clients) == 2:
                    self._game_loop()
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error aceptando conexión: {e}")
    
    def _game_loop(self):
        """Loop principal de sincronización del juego"""
        while self.running and len(self.clients) == 2:
            try:
                for player_id, client_info in list(self.clients.items()):
                    try:
                        data = client_info["socket"].recv(BUFFER_SIZE)
                        if data:
                            client_info["data"] = pickle.loads(data)
                        else:
                            self._disconnect_client(player_id)
                    
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f"Error recibiendo de jugador {player_id}: {e}")
                        self._disconnect_client(player_id)
                
                # Enviar datos de ambos jugadores a cada cliente
                if len(self.clients) == 2:
                    game_state = {
                        1: self.clients.get(1, {}).get("data"),
                        2: self.clients.get(2, {}).get("data")
                    }
                    
                    for player_id, client_info in self.clients.items():
                        try:
                            client_info["socket"].sendall(pickle.dumps(game_state))
                        except:
                            self._disconnect_client(player_id)
                
                time.sleep(1 / FPS)
            
            except Exception as e:
                print(f"Error en game_loop: {e}")
    
    def _disconnect_client(self, player_id):
        """Desconecta un cliente"""
        if player_id in self.clients:
            try:
                self.clients[player_id]["socket"].close()
            except:
                pass
            del self.clients[player_id]
            print(f"[SERVIDOR] Jugador {player_id} desconectado")
    
    def get_connected_clients(self):
        """Retorna el número de clientes conectados"""
        return len(self.clients)
    
    def is_running(self):
        """Verifica si el servidor está corriendo"""
        return self.running
    
    def stop(self):
        """Detiene el servidor"""
        self.running = False
        
        # Cerrar conexiones
        for player_id in list(self.clients.keys()):
            self._disconnect_client(player_id)
        
        # Cerrar socket del servidor
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("[SERVIDOR] Detenido")
