PING PONG ULTIMATE EDITION
=========================

Resumen
------
"Ping Pong Ultimate Edition" es un juego de pong/ping-pong desarrollado en Python + Pygame. Incluye:
- 1 jugador vs IA (3 dificultades: Fácil, Medio, Difícil)
- 2 jugadores (local)
- Multijugador online (HOST / CLIENT) por sockets TCP
- Menús, selección de puntaje, efectos visuales y ajustes de IA

Objetivo
-------
Golpear la pelota con la paleta para marcar puntos. Gana quien alcance el puntaje seleccionado.

Requisitos
---------
- Windows (probado en Windows 10/11)
- Python 3.11+ (probado con Python 3.13.5)
- Virtualenv (opcional, recomendado)
- Paquetes Python (listados en `requirements.txt`):
  - `pygame`
  - `numpy`

Comandos rápidos (Git hub)
---------------------------
Abrir PowerShell/terminal y ejecutar el https de mi perfil o tambien:

```powershell
# Crear y activar entorno virtual (opcional)
python -m venv .venv_new
.\.venv_new\Scripts\Activate.ps1

# Instalar dependencias
.venv_new\Scripts\pip install -r requirements.txt

# Ejecutar el juego
.venv_new\Scripts\python main.py
```

Estructura del proyecto
----------------------
(versión simplificada)

- `main.py`                  - Punto de entrada (menús, modos de juego)
- `server.py`                - Servidor independiente (opcional)
- `requirements.txt`         - Dependencias
- `README.md`                - Este archivo
- `game/`
  - `config.py`             - Constantes de configuración (puertos, tamaños, colores)
  - `game.py`               - Bucle principal / manager de escenas
  - `ball.py`               - Lógica y física de la pelota
  - `paddle.py`             - Clase paleta / jugador
  - `ai.py`                 - IA (dificultades ajustables)
  - `scoreboard.py`         - Marcador y lógica de puntuación
  - `menu.py`               - Menús (principal, dificultad, online, score)
  - `network.py`            - Cliente y servidor TCP para multiplayer
  - `utils.py`              - Utilidades (colisiones, dibujado, partículas)
- `assets/` (opcional)      - Imágenes, sonidos, fuentes (si existen)

Cómo jugar (paso a paso)
-----------------------
1. Ejecutar `main.py`:
   - `.\.venv_new\Scripts\python main.py`
2. En el menú principal elegir el modo:
   - 1 Jugador: seleccionar dificultad (Fácil/Medio/Difícil) y puntaje.
   - 2 Jugadores (local): se juega en la misma pantalla.
   - Online: elegir `HOST` o `CLIENT`.

Modo HOST (anfitrión)
---------------------
1. En el menú Online seleccionar `HOST`.
2. Se inicia un servidor local y se muestra la IP (ej. `192.168.1.102:5555`) en pantalla.
3. Esperar a que el otro jugador se conecte (la pantalla de espera muestra el número de jugadores).
4. Una vez ambos conectados, el juego se inicia automáticamente.

Notas importantes de red (HOST):
- El server por defecto escucha en el puerto definido en `game/config.py` (por defecto `5555`).
- Ambos equipos deben estar en la misma LAN (misma subred) para poder conectarse usando la IP mostrada (192.168.x.x). Si usas `127.0.0.1` o `localhost`, ambos procesos deben ejecutarse en la misma máquina.
- Si el sistema operativo pregunta por permisos de red/firewall, permite la conexión para Python o el puerto `5555`.

Modo CLIENT (unirse)
--------------------
1. En otra máquina (o la misma), ejecutar `main.py` y seleccionar `CLIENT` en Online.
2. En la pantalla "UNIRSE A SERVIDOR" ingresar la IP mostrada por el HOST en el campo "Dirección IP" y el puerto (ej: `5555`).
   - Si prefieres solo ingresar el puerto, puedes dejar la IP vacía y presionar ENTER: el cliente usará `127.0.0.1` (localhost).
3. Pulsa `ENTER` para conectar.
4. Cuando estés conectado, el cliente indica tu `player_id` y espera al otro jugador.

Controles
--------
- JUGADOR 1: W / S o flechas (arriba/abajo) (depende de la configuración en `paddle.py`)
- JUGADOR 2: Up / Down (si es local)
- Pausa: Esc (en menús además cancela / vuelve atrás)

Configuración útil
------------------
- `game/config.py` contiene constantes como:
  - `WINDOW_WIDTH`, `WINDOW_HEIGHT` (resolución)
  - `FPS` (frames por segundo)
  - `DEFAULT_PORT` (puerto por defecto para multiplayer)
  - `DIFFICULTY_*` (constantes de dificultad)

Sugerencias para jugar en red
----------------------------
- Ambos equipos deben estar en la misma red local (Wi‑Fi o cable). Comprueba las IPs con `ipconfig` (Windows) para verificar la subred.
- Si no puedes conectar, prueba primero con `localhost` en la misma máquina para descartar errores del socket.
- Revisa el firewall de Windows: permite la aplicación Python o el puerto `5555`.

Solución de problemas comunes
----------------------------
- Error: "Servidor no disponible" / "Conexión expirada"
  - Asegúrate de que el HOST haya iniciado el servidor y que muestre la IP.
  - Verifica que la IP ingresada por el CLIENT es exactamente la que aparece en la pantalla del HOST.
  - Comprueba que no haya un bloqueo por firewall.

- Error: Pygame no se instala o falla al importar
  - Asegúrate de usar la versión adecuada de Python y de activar el virtualenv.
  - Ejecuta: `.venv_new\Scripts\pip install -r requirements.txt`

- Si el juego se cierra con excepción, copia aquí la salida del terminal y la revisaré.

Personalización y desarrollo
----------------------------
- Para cambiar la dificultad de la IA revisa `game/ai.py`.
- Para ajustar física o velocidad de la pelota mira `game/ball.py`.
- Para modificar el puerto por defecto edita `game/config.py` (constante `DEFAULT_PORT`).

Convertir a ejecutable (opcional)
---------------------------------
Puedes usar `pyinstaller` para generar un ejecutable:

```powershell
. .venv_new\Scripts\Activate.ps1
.venv_new\Scripts\pip install pyinstaller
.venv_new\Scripts\pyinstaller --onefile --add-data "assets;assets" main.py
```

Contribuir
---------
Si quieres que mejore o agregue algo en el futuro como (sonidos, red, matchmaking, assets) abre un issue o envíame una lista de cambios deseados.

Licencia
-------
Incluye tu licencia preferida aquí (por ejemplo MIT) o deja este apartado vacío si no quieres publicarlo.

Créditos
-------
- Motor: Pygame
- Desarrollador: jesus espinoza collazo ( Universidad Politecnica de Santa Rosa Jauregui ) 

Gracias por jugar y por construir este proyecto si es que lo quieres modificar , buena suerte !.