
# ==================================================
# IMPORTACIONES
# ==================================================

# Librería para administrar los registros del sistema.
import logging

# Permite trabajar con directorios y rutas de archivos.
from pathlib import Path


# ==================================================
# CONFIGURACIÓN DE RUTAS
# ==================================================

# Obtenemos la carpeta principal del proyecto PFO3.
BASE_DIR = Path(__file__).resolve().parent.parent

# Definimos la carpeta donde se guardarán los registros.
LOG_DIR = BASE_DIR / "logs"

# Creamos la carpeta logs si todavía no existe.
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Definimos el archivo donde se almacenarán los eventos.
LOG_FILE = LOG_DIR / "servidor.log"


# ==================================================
# FUNCIÓN PARA CONFIGURAR EL LOGGER
# ==================================================

def obtener_logger():

    # Obtenemos o creamos el logger de nuestra aplicación.
    logger = logging.getLogger("PFO3")

    # Establecemos el nivel mínimo de registro.
    logger.setLevel(logging.INFO)

    # Evitamos configurar varias veces los mismos manejadores.
    if not logger.handlers:

        # Definimos el formato de los mensajes.
        formato = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # Configuramos el registro en el archivo servidor.log.
        archivo = logging.FileHandler(
            LOG_FILE,
            encoding='utf-8'
        )

        archivo.setFormatter(formato)

        # Configuramos el registro en la consola.
        consola = logging.StreamHandler()

        consola.setFormatter(formato)

        # Asociamos los manejadores al logger.
        logger.addHandler(archivo)
        logger.addHandler(consola)

    # Devolvemos el logger configurado.
    return logger
