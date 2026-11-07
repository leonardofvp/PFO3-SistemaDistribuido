import logging
from pathlib import Path

# Directorio principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio de logs
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "servidor.log"


def obtener_logger():

    logger = logging.getLogger("PFO3")
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formato = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # Registro en archivo
        archivo = logging.FileHandler(
            LOG_FILE,
            encoding='utf-8'
        )
        archivo.setFormatter(formato)

        # Registro en consola
        consola = logging.StreamHandler()
        consola.setFormatter(formato)

        logger.addHandler(archivo)
        logger.addHandler(consola)

    return logger