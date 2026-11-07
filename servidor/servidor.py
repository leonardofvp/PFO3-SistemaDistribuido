
# ==================================================
# IMPORTACIONES
# ==================================================

# Permite establecer comunicaciones mediante TCP/IP.
import socket

# Administra un conjunto de hilos reutilizables.
from concurrent.futures import ThreadPoolExecutor

# Importamos la función para registrar eventos.
from logger import obtener_logger


# ==================================================
# CONFIGURACIÓN DEL SERVIDOR
# ==================================================

# Dirección IP donde escuchará el servidor.
HOST = '127.0.0.1'

# Puerto TCP utilizado para recibir conexiones.
PORT = 5000

# Cantidad máxima de hilos que atenderán clientes simultáneamente.
MAX_WORKERS = 5

# Tiempo máximo de espera para recibir datos de un cliente.
# Si pasan 30 segundos sin recibir información, se cierra la conexión.
TIMEOUT_CLIENTE = 30

# Inicializamos el sistema de logs.
logger = obtener_logger()


# ==================================================
# ATENCIÓN DE CLIENTES
# ==================================================

def manejar_cliente(cliente, direccion):
    """
    Atiende las solicitudes de un cliente.

    cliente: socket de comunicación con el cliente.
    direccion: dirección IP y puerto del cliente.

    Esta función se ejecuta dentro de un worker del Thread Pool.
    """

    logger.info(f"Nueva conexión desde: {direccion}")

    try:

        # Establecemos el tiempo máximo de espera del socket.
        cliente.settimeout(TIMEOUT_CLIENTE)

        # Esperamos recibir información del cliente.
        datos = cliente.recv(1024)

        # Verificamos que se hayan recibido datos.
        if datos:

            # Convertimos los bytes recibidos a texto.
            mensaje = datos.decode('utf-8')

            # Registramos el mensaje recibido.
            logger.info(f"Mensaje recibido: {mensaje}")

            # Generamos una respuesta para el cliente.
            respuesta = "Mensaje procesado por un worker"

            # Enviamos la respuesta mediante el socket.
            cliente.sendall(respuesta.encode('utf-8'))

        else:

            # El cliente cerró la conexión sin enviar información.
            logger.info(f"El cliente {direccion} cerró la conexión.")

    except socket.timeout:

        # Se ejecuta cuando el cliente supera el tiempo de espera.
        logger.warning(
            f"Timeout: cliente {direccion} inactivo durante "
            f"{TIMEOUT_CLIENTE} segundos."
        )

    except Exception as e:

        # Registramos cualquier otro error de comunicación.
        logger.error(f"Error con el cliente {direccion}: {e}")

    finally:

        # Cerramos la conexión para liberar recursos.
        cliente.close()

        # Registramos el cierre de la conexión.
        logger.info(f"Conexión cerrada: {direccion}")


# ==================================================
# INICIO DEL SERVIDOR
# ==================================================

def iniciar_servidor():

    # Creamos un socket IPv4 utilizando TCP.
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permitimos reutilizar el puerto después de detener el servidor.
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:

        # Asociamos el socket a la dirección IP y al puerto.
        servidor.bind((HOST, PORT))

        # Colocamos el servidor en modo escucha.
        servidor.listen(10)

        logger.info(f"Servidor escuchando en {HOST}:{PORT}")
        logger.info(f"Thread Pool configurado con {MAX_WORKERS} workers")
        logger.info(f"Timeout de clientes: {TIMEOUT_CLIENTE} segundos")

        # Creamos el Thread Pool.
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:

            try:

                # El servidor permanece esperando conexiones.
                while True:

                    # Esperamos la conexión de un cliente.
                    cliente, direccion = servidor.accept()

                    # Delegamos la atención al Thread Pool.
                    pool.submit(manejar_cliente, cliente, direccion)

            except KeyboardInterrupt:

                # Capturamos la interrupción mediante Ctrl + C.
                logger.info("Solicitud de detención recibida (Ctrl + C).")

            finally:

                # Cerramos el socket principal.
                servidor.close()
                logger.info("Socket del servidor cerrado.")

        # Esperamos que finalicen los workers activos.
        logger.info("Todos los workers finalizaron.")
        logger.info("Servidor detenido correctamente.")

    except OSError as e:

        # Registramos errores relacionados con el socket.
        logger.error(f"Error al iniciar o ejecutar el servidor: {e}")

        # Cerramos el socket.
        servidor.close()


# ==================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==================================================

if __name__ == "__main__":

    # Iniciamos el servidor.
    iniciar_servidor()
