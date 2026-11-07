
import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from logger import obtener_logger

HOST = '127.0.0.1'
PORT = 5000

# Pool de 5 workers para procesar las tareas
pool = ThreadPoolExecutor(max_workers=5)

logger = obtener_logger()


def procesar_tarea(tarea):
    """
    Procesa mensajes de texto y operaciones matemáticas.
    Esta función se ejecuta en uno de los workers del pool.
    """

    try:
        operacion = tarea.get('operacion')

        # Operaciones matemáticas
        if operacion in ('sumar', 'restar', 'multiplicar', 'dividir'):

            numero1 = float(tarea.get('numero1'))
            numero2 = float(tarea.get('numero2'))

            if operacion == 'sumar':
                resultado = numero1 + numero2

            elif operacion == 'restar':
                resultado = numero1 - numero2

            elif operacion == 'multiplicar':
                resultado = numero1 * numero2

            elif operacion == 'dividir':
                if numero2 == 0:
                    raise ValueError('No se puede dividir por cero')

                resultado = numero1 / numero2

            logger.info(
                f'Operacion: {operacion} | '
                f'{numero1} y {numero2} | Resultado: {resultado}'
            )

            return {
                'estado': 'OK',
                'resultado': resultado
            }

        # Mensaje de texto
        mensaje = tarea.get('mensaje')

        if mensaje is not None:
            if not isinstance(mensaje, str) or not mensaje.strip():
                raise ValueError('El mensaje no puede estar vacio')

            logger.info(f'Mensaje recibido: {mensaje}')

            return {
                'estado': 'OK',
                'resultado': f'Tarea procesada correctamente: {mensaje}'
            }

        raise ValueError('La tarea no contiene una operacion valida')

    except (ValueError, TypeError) as error:
        logger.error(f'Error al procesar tarea: {error}')

        return {
            'estado': 'ERROR',
            'resultado': str(error)
        }

    except Exception as error:
        logger.exception(f'Error inesperado: {error}')

        return {
            'estado': 'ERROR',
            'resultado': 'Error interno al procesar la tarea'
        }


def recibir_mensaje(cliente, buffer):
    """
    Recibe datos hasta encontrar un salto de linea.
    """

    while b'\n' not in buffer:
        datos = cliente.recv(1024)

        if not datos:
            return None, buffer

        buffer += datos

    mensaje, buffer = buffer.split(b'\n', 1)

    return mensaje, buffer


def manejar_cliente(cliente, direccion):
    """
    Atiende las solicitudes de un cliente.
    """

    logger.info(f'Cliente conectado: {direccion}')

    buffer = b''

    try:
        while True:

            datos, buffer = recibir_mensaje(cliente, buffer)

            if datos is None:
                break

            try:
                tarea = json.loads(datos.decode('utf-8'))

                # Enviar la tarea al pool de workers
                futuro = pool.submit(procesar_tarea, tarea)

                # Esperar el resultado del worker
                respuesta = futuro.result()

            except json.JSONDecodeError:
                respuesta = {
                    'estado': 'ERROR',
                    'resultado': 'Formato JSON invalido'
                }

                logger.error('Se recibio un JSON invalido')

            except Exception as error:
                respuesta = {
                    'estado': 'ERROR',
                    'resultado': str(error)
                }

                logger.error(f'Error de comunicacion: {error}')

            # Enviar respuesta al cliente
            respuesta_json = json.dumps(respuesta) + '\n'

            cliente.sendall(respuesta_json.encode('utf-8'))

    except (ConnectionError, OSError) as error:
        logger.error(f'Error de conexion con {direccion}: {error}')

    finally:
        cliente.close()
        logger.info(f'Cliente desconectado: {direccion}')


def iniciar_servidor():

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORT))
    servidor.listen()

    logger.info(f'Servidor escuchando en {HOST}:{PORT}')

    try:
        while True:

            cliente, direccion = servidor.accept()

            hilo = threading.Thread(
                target=manejar_cliente,
                args=(cliente, direccion)
            )

            hilo.start()

    except KeyboardInterrupt:
        logger.info('Servidor detenido por el usuario')

    finally:
        servidor.close()
        pool.shutdown(wait=True)


if __name__ == '__main__':
    iniciar_servidor()
