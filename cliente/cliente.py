
import socket
import json

HOST = '127.0.0.1'
PORT = 5000


def recibir_respuesta(cliente, buffer):
    """
    Recibe la respuesta del servidor hasta encontrar un salto de linea.
    """

    while b'\n' not in buffer:
        datos = cliente.recv(1024)

        if not datos:
            raise ConnectionError('El servidor cerro la conexion')

        buffer += datos

    respuesta, buffer = buffer.split(b'\n', 1)

    return respuesta, buffer


def enviar_tarea(cliente, buffer, tarea):
    """
    Envia una tarea al servidor y recibe su resultado.
    """

    mensaje = json.dumps(tarea) + '\n'

    cliente.sendall(mensaje.encode('utf-8'))

    datos, buffer = recibir_respuesta(cliente, buffer)

    respuesta = json.loads(datos.decode('utf-8'))

    print('\nResultado:', respuesta.get('resultado'))

    return buffer


def iniciar_cliente():

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    buffer = b''

    try:
        cliente.connect((HOST, PORT))

        print('Conectado al servidor')

        while True:

            print('\n========== MENU ==========')
            print('1 - Sumar')
            print('2 - Restar')
            print('3 - Multiplicar')
            print('4 - Dividir')
            print('5 - Enviar mensaje de texto')
            print('0 - Salir')
            print('==========================')

            opcion = input('Seleccione una opcion: ').strip()

            if opcion == '0':
                print('Desconectando cliente...')
                break

            # Operaciones matematicas
            operaciones = {
                '1': 'sumar',
                '2': 'restar',
                '3': 'multiplicar',
                '4': 'dividir'
            }

            if opcion in operaciones:

                try:
                    numero1 = float(input('Ingrese el primer numero: '))
                    numero2 = float(input('Ingrese el segundo numero: '))

                except ValueError:
                    print('Error: debe ingresar valores numericos')
                    continue

                tarea = {
                    'operacion': operaciones[opcion],
                    'numero1': numero1,
                    'numero2': numero2
                }

            # Mensaje de texto
            elif opcion == '5':

                mensaje = input('Ingrese el mensaje: ')

                tarea = {
                    'mensaje': mensaje
                }

            else:
                print('Opcion incorrecta')
                continue

            buffer = enviar_tarea(cliente, buffer, tarea)

    except ConnectionRefusedError:
        print('No se pudo conectar. Verifique que el servidor este iniciado')

    except (ConnectionError, OSError) as error:
        print(f'Error de comunicacion: {error}')

    finally:
        cliente.close()


if __name__ == '__main__':
    iniciar_cliente()
