"""
Módulo de configuración de logging.
Configura el sistema de logs con handlers para archivo y consola.
"""

import logging
import sys
from config import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Configura y retorna un logger con handlers para archivo y consola.
    
    Args:
        name: Nombre del logger (por defecto usa el nombre del módulo)
    
    Returns:
        Logger configurado con handlers de archivo y consola
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers si ya existen
    if logger.handlers:
        return logger
    
    # Formatter común para todos los handlers
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # Handler para archivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Logger por defecto para el módulo
logger = setup_logger('books_scraper')
