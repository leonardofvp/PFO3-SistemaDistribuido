
import socket
import json
import threading

from concurrent.futures import ThreadPoolExecutor
from logger import obtener_logger


HOST = '127.0.0.1'
PORT = 5000
MAX_WORKERS = 5
MAX_MENSAJE = 65536

logger = obtener_logger()


def procesar_tarea(tarea):

    mensaje = tarea.get('mensaje')

    if not isinstance(mensaje, str) or not mensaje.strip():
        return {
            'estado': 'ERROR',
            'resultado': 'El mensaje no puede estar vacío.'
        }

    mensaje = mensaje.strip()

    logger.info(
        f'Worker {threading.current_thread().name} '
        f'procesando tarea: {mensaje}'
    )

    return {
        'estado': 'OK',
        'resultado': f'Tarea procesada correctamente: {mensaje}'
    }


def recibir_mensaje(cliente, buffer):

    while b'\n' not in buffer:

        datos = cliente.recv(1024)

        if not datos:
            return None, buffer

        buffer += datos

        if len(buffer) > MAX_MENSAJE:
            raise ValueError('Mensaje demasiado grande.')

    mensaje_bytes, buffer = buffer.split(b'\n', 1)

    if not mensaje_bytes.strip():
        raise ValueError('Mensaje vacío.')

    solicitud = json.loads(mensaje_bytes.decode('utf-8'))

    return solicitud, buffer


def manejar_cliente(cliente, direccion, pool):

    logger.info(f'Cliente conectado: {direccion}')

    buffer = b''

    try:

        while True:

            solicitud, buffer = recibir_mensaje(cliente, buffer)

            if solicitud is None:
                break

            if not isinstance(solicitud, dict):
                raise ValueError('La solicitud debe ser un objeto JSON.')

            logger.info(f'Solicitud recibida: {direccion}')

            try:

                futuro = pool.submit(procesar_tarea, solicitud)
                resultado = futuro.result()

            except Exception as error:

                logger.exception(f'Error procesando tarea: {error}')

                resultado = {
                    'estado': 'ERROR',
                    'resultado': 'Error al procesar la tarea.'
                }

            respuesta = json.dumps(
                resultado,
                ensure_ascii=False
            ) + '\n'

            cliente.sendall(respuesta.encode('utf-8'))

            logger.info(f'Respuesta enviada: {direccion}')

    except json.JSONDecodeError as error:

        logger.exception(f'JSON inválido: {error}')

    except ValueError as error:

        logger.exception(f'Error de solicitud: {error}')

    except ConnectionError as error:

        logger.info(f'Conexión finalizada: {direccion} - {error}')

    except OSError as error:

        logger.exception(f'Error de socket: {error}')

    except Exception as error:

        logger.exception(f'Error inesperado: {error}')

    finally:

        cliente.close()
        logger.info(f'Conexión cerrada: {direccion}')


def iniciar_servidor():

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:

        servidor.bind((HOST, PORT))
        servidor.listen(10)

        logger.info(f'Servidor escuchando en {HOST}:{PORT}')
        logger.info(f'Pool de workers configurado: {MAX_WORKERS}')

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:

            while True:

                cliente, direccion = servidor.accept()

                hilo = threading.Thread(
                    target=manejar_cliente,
                    args=(cliente, direccion, pool),
                    daemon=True
                )

                hilo.start()

    except KeyboardInterrupt:

        logger.info('Servidor detenido por el usuario.')

    except OSError as error:

        logger.exception(f'Error en el servidor: {error}')

    finally:

        servidor.close()
        logger.info('Socket del servidor cerrado.')


if __name__ == '__main__':
    iniciar_servidor()
