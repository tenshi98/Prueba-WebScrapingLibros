"""
Configuración del proyecto de web scraping standalone.
Define constantes y parámetros para el scraper, base de datos y logging.
"""

import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
DB_PATH = os.path.join(DATA_DIR, 'libros.db')

# Configuración del scraper
BASE_URL = 'https://books.toscrape.com'
CATALOGUE_URL = f'{BASE_URL}/catalogue'
MAX_PAGES = 3  # Solo extraer las primeras 3 páginas
DETAIL_BOOKS_LIMIT = 5  # Solo extraer detalles completos de los primeros 5 libros

# Configuración de Chromium (standalone - usar driver del sistema)
CHROMIUM_DRIVER_PATH = '/usr/bin/chromedriver'  # Path típico en Linux
# Alternativas comunes:
# - Ubuntu/Debian: /usr/bin/chromedriver
# - Fedora: /usr/local/bin/chromedriver
# - macOS: /usr/local/bin/chromedriver
# Si está en PATH, puede dejarse como 'chromedriver'

# Configuración de delays y rate limiting
REQUEST_DELAY = 2  # Segundos entre requests
PAGE_LOAD_TIMEOUT = 10  # Timeout para carga de páginas
IMPLICIT_WAIT = 5  # Espera implícita para elementos

# Configuración de Selenium
HEADLESS_MODE = True  # Ejecutar navegador en modo headless
WINDOW_SIZE = "1920,1080"

# Configuración de logging
LOG_FILE = os.path.join(LOGS_DIR, 'scraper.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Mapeo de ratings
RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

# Crear directorios si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
