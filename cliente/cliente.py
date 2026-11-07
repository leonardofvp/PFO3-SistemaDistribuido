
# ==================================================
# IMPORTACIONES
# ==================================================

# Librería para establecer comunicaciones TCP/IP.
import socket


# ==================================================
# CONFIGURACIÓN DEL CLIENTE
# ==================================================

# Dirección IP del servidor.
HOST = '127.0.0.1'

# Puerto donde escucha el servidor.
PORT = 5000


# ==================================================
# CONEXIÓN CON EL SERVIDOR
# ==================================================

def conectar_servidor():

    # Creamos el socket del cliente utilizando IPv4 y TCP.
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        # Establecemos la conexión con el servidor.
        cliente.connect((HOST, PORT))

        print("Conectado al servidor correctamente.")

        # Solicitamos un mensaje al usuario.
        mensaje = input("Ingrese un mensaje: ")

        # Convertimos el mensaje a bytes y lo enviamos.
        cliente.sendall(mensaje.encode('utf-8'))

        # Esperamos recibir la respuesta del servidor.
        respuesta = cliente.recv(1024)

        # Mostramos la respuesta recibida.
        print("Respuesta del servidor:", respuesta.decode('utf-8'))

    except ConnectionRefusedError:

        # Se ejecuta cuando el servidor no está disponible.
        print("No se pudo conectar con el servidor.")

    except Exception as e:

        # Capturamos otros errores de comunicación.
        print(f"Error de comunicación: {e}")

    finally:

        # Cerramos el socket del cliente.
        cliente.close()

        print("Conexión del cliente cerrada.")


# ==================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==================================================

if __name__ == "__main__":

    # Iniciamos la conexión con el servidor.
    conectar_servidor()
