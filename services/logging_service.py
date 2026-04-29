import logging
from pathlib import Path


# Ruta del archivo donde se guardarán los logs
LOG_FILE = Path("logs/app.log")


def setup_logger() -> logging.Logger:
    """
    Configura y devuelve el logger principal de la aplicación.

    Returns:
        logging.Logger: logger configurado
    """

    # Creamos la carpeta logs/ si no existe
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Creamos o recuperamos un logger con nombre "climapp"
    logger = logging.getLogger("climapp")

    # Nivel mínimo de mensajes que se van a guardar
    # INFO guarda INFO, WARNING, ERROR y CRITICAL
    logger.setLevel(logging.INFO)

    # Esto evita que, si llamamos varias veces a setup_logger(),
    # se añadan manejadores duplicados y se escriba el mismo log dos veces.
    if not logger.handlers:
        # FileHandler escribe los logs en un archivo
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

        # Formato del log
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Aplicamos el formato al archivo
        file_handler.setFormatter(formatter)

        # Añadimos el manejador al logger
        logger.addHandler(file_handler)

    return logger


def log_info(message: str) -> None:
    """
    Guarda un mensaje informativo.
    """
    logger = setup_logger()
    logger.info(message)


def log_warning(message: str) -> None:
    """
    Guarda un mensaje de advertencia.
    """
    logger = setup_logger()
    logger.warning(message)


def log_error(message: str) -> None:
    """
    Guarda un mensaje de error.
    """
    logger = setup_logger()
    logger.error(message)


def log_critical(message: str) -> None:
    """
    Guarda un mensaje crítico.
    """
    logger = setup_logger()
    logger.critical(message)