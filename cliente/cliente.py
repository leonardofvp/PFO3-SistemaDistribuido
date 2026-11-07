import socket

HOST = '127.0.0.1'
PORT = 5000


def conectar_servidor():

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))

        print("Conectado al servidor correctamente")

        mensaje = input("Ingrese un mensaje: ")

        cliente.sendall(mensaje.encode('utf-8'))

        respuesta = cliente.recv(1024)

        print("Respuesta del servidor:", respuesta.decode('utf-8'))

    except ConnectionRefusedError:
        print("No se pudo conectar con el servidor")

    finally:
        cliente.close()


if __name__ == "__main__":
    conectar_servidor()