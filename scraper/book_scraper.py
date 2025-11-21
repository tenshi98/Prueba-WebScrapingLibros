"""
Módulo de web scraping con Selenium (Standalone - Chromium).
Extrae información de libros desde books.toscrape.com usando Chromium del sistema.
"""

import time
import os
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config import (
    BASE_URL, 
    CATALOGUE_URL,
    MAX_PAGES, 
    DETAIL_BOOKS_LIMIT,
    REQUEST_DELAY, 
    PAGE_LOAD_TIMEOUT,
    IMPLICIT_WAIT,
    HEADLESS_MODE,
    WINDOW_SIZE,
    RATING_MAP,
    CHROMIUM_DRIVER_PATH
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BookScraper:
    """Scraper de libros usando Selenium WebDriver con Chromium standalone."""
    
    def __init__(self):
        """Inicializa el scraper y configura el WebDriver."""
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self) -> None:
        """Configura y inicializa el WebDriver de Chromium."""
        try:
            chrome_options = Options()
            
            if HEADLESS_MODE:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            
            chrome_options.add_argument(f'--window-size={WINDOW_SIZE}')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Usar Chromium driver del sistema (standalone)
            if os.path.exists(CHROMIUM_DRIVER_PATH):
                service = Service(CHROMIUM_DRIVER_PATH)
                logger.info(f"Usando chromedriver en: {CHROMIUM_DRIVER_PATH}")
            else:
                # Intentar usar chromedriver desde PATH
                service = Service('chromedriver')
                logger.info("Usando chromedriver desde PATH del sistema")
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            
            logger.info("WebDriver de Chromium inicializado correctamente")
        except WebDriverException as e:
            logger.error(f"Error al inicializar WebDriver: {e}")
            logger.error("Asegúrate de tener Chromium y chromedriver instalados:")
            logger.error("  Ubuntu/Debian: sudo apt install chromium-browser chromium-chromedriver")
            logger.error("  Fedora: sudo dnf install chromium chromedriver")
            raise
    
    def close(self) -> None:
        """Cierra el WebDriver y libera recursos."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver cerrado correctamente")
            except Exception as e:
                logger.error(f"Error al cerrar WebDriver: {e}")
    
    def wait_between_requests(self) -> None:
        """Aplica delay entre requests para evitar sobrecargar el servidor."""
        time.sleep(REQUEST_DELAY)
        logger.debug(f"Esperando {REQUEST_DELAY} segundos entre requests")
    
    def get_page(self, url: str, retries: int = 3) -> bool:
        """
        Navega a una URL con reintentos en caso de error.
        
        Args:
            url: URL a la que navegar
            retries: Número de reintentos en caso de error
        
        Returns:
            True si la navegación fue exitosa, False en caso contrario
        """
        for attempt in range(retries):
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                logger.info(f"Página cargada exitosamente: {url}")
                return True
            except TimeoutException:
                logger.warning(f"Timeout al cargar página (intento {attempt + 1}/{retries}): {url}")
            except WebDriverException as e:
                logger.error(f"Error al cargar página (intento {attempt + 1}/{retries}): {e}")
            
            if attempt < retries - 1:
                time.sleep(2)
        
        logger.error(f"No se pudo cargar la página después de {retries} intentos: {url}")
        return False
    
    def extract_rating(self, book_element) -> Optional[int]:
        """
        Extrae el rating de un libro.
        
        Args:
            book_element: Elemento Selenium del libro
        
        Returns:
            Rating numérico (1-5) o None si no se encuentra
        """
        try:
            rating_element = book_element.find_element(By.CSS_SELECTOR, 'p.star-rating')
            rating_class = rating_element.get_attribute('class')
            
            for rating_text, rating_value in RATING_MAP.items():
                if rating_text in rating_class:
                    return rating_value
            
            logger.warning("Rating no reconocido en las clases CSS")
            return None
        except NoSuchElementException:
            logger.warning("Elemento de rating no encontrado")
            return None
    
    def extract_book_details(self, book_url: str) -> Dict:
        """
        Extrae detalles completos de un libro desde su página individual.
        
        Args:
            book_url: URL de la página del libro
        
        Returns:
            Diccionario con los detalles del libro (descripcion, upc, categoria)
        """
        details = {
            'descripcion': None,
            'upc': None,
            'categoria': None
        }
        
        if not self.get_page(book_url):
            return details
        
        try:
            # Extraer descripción
            try:
                description_element = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'article.product_page > p'
                )
                details['descripcion'] = description_element.text.strip()
            except NoSuchElementException:
                logger.warning(f"Descripción no encontrada para: {book_url}")
            
            # Extraer UPC de la tabla de información del producto
            try:
                table_rows = self.driver.find_elements(By.CSS_SELECTOR, 'table.table tr')
                for row in table_rows:
                    header = row.find_element(By.TAG_NAME, 'th').text
                    if header == 'UPC':
                        details['upc'] = row.find_element(By.TAG_NAME, 'td').text.strip()
                        break
            except NoSuchElementException:
                logger.warning(f"UPC no encontrado para: {book_url}")
            
            # Extraer categoría del breadcrumb
            try:
                breadcrumb = self.driver.find_elements(By.CSS_SELECTOR, 'ul.breadcrumb li')
                if len(breadcrumb) >= 3:
                    details['categoria'] = breadcrumb[2].text.strip()
            except (NoSuchElementException, IndexError):
                logger.warning(f"Categoría no encontrada para: {book_url}")
        
        except Exception as e:
            logger.error(f"Error al extraer detalles del libro: {e}")
        
        return details
    
    def extract_books_from_page(self, extract_details: bool = False, detail_limit: int = 0) -> List[Dict]:
        """
        Extrae información de todos los libros en la página actual.
        
        Args:
            extract_details: Si True, extrae detalles completos navegando a cada libro
            detail_limit: Límite de libros para extraer detalles (0 = todos)
        
        Returns:
            Lista de diccionarios con información de cada libro
        """
        books = []
        
        try:
            book_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')
            logger.info(f"Encontrados {len(book_elements)} libros en la página")
            
            for idx, book_element in enumerate(book_elements, 1):
                try:
                    # Extraer información básica
                    title_element = book_element.find_element(By.CSS_SELECTOR, 'h3 a')
                    titulo = title_element.get_attribute('title')
                    book_relative_url = title_element.get_attribute('href')
                    
                    # Construir URL completa del libro
                    if book_relative_url.startswith('catalogue/'):
                        book_url = f"{BASE_URL}/{book_relative_url}"
                    elif book_relative_url.startswith('../../../'):
                        book_url = f"{CATALOGUE_URL}/{book_relative_url.replace('../../../', '')}"
                    else:
                        book_url = book_relative_url
                    
                    # Precio
                    price_element = book_element.find_element(By.CSS_SELECTOR, 'p.price_color')
                    precio_text = price_element.text.strip().replace('£', '')
                    precio = float(precio_text) if precio_text else None
                    
                    # Disponibilidad
                    availability_element = book_element.find_element(By.CSS_SELECTOR, 'p.availability')
                    disponibilidad = availability_element.text.strip()
                    
                    # Rating
                    rating = self.extract_rating(book_element)
                    
                    # URL de imagen
                    img_element = book_element.find_element(By.CSS_SELECTOR, 'img')
                    img_relative_url = img_element.get_attribute('src')
                    url_imagen = f"{BASE_URL}/{img_relative_url.replace('../', '')}"
                    
                    # Inicializar datos del libro con info básica
                    book_data = {
                        'titulo': titulo,
                        'precio': precio,
                        'disponibilidad': disponibilidad,
                        'rating': rating,
                        'url_imagen': url_imagen,
                        'descripcion': None,
                        'upc': None,
                        'categoria': None
                    }
                    
                    # Extraer detalles solo si está habilitado y no se ha alcanzado el límite
                    if extract_details and (detail_limit == 0 or len(books) < detail_limit):
                        logger.info(f"Extrayendo detalles del libro {len(books) + 1}: {titulo}")
                        self.wait_between_requests()
                        details = self.extract_book_details(book_url)
                        book_data.update(details)
                        
                        # Volver a la página de listado
                        self.driver.back()
                        time.sleep(1)
                    
                    books.append(book_data)
                    logger.info(f"Libro extraído: {titulo} (detalles: {extract_details and len(books) <= detail_limit})")
                
                except Exception as e:
                    logger.error(f"Error al extraer libro {idx}: {e}")
                    continue
        
        except NoSuchElementException:
            logger.error("No se encontraron libros en la página")
        except Exception as e:
            logger.error(f"Error al extraer libros de la página: {e}")
        
        return books
    
    def scrape_books(self, max_pages: int = MAX_PAGES, detail_limit: int = DETAIL_BOOKS_LIMIT) -> List[Dict]:
        """
        Extrae libros de múltiples páginas del catálogo.
        Extrae info básica de todas las páginas, pero detalles completos solo de los primeros N libros.
        
        Args:
            max_pages: Número máximo de páginas a extraer
            detail_limit: Número de libros para extraer detalles completos
        
        Returns:
            Lista de todos los libros extraídos
        """
        all_books = []
        books_with_details = 0
        
        for page_num in range(1, max_pages + 1):
            try:
                url = f"{CATALOGUE_URL}/page-{page_num}.html"
                
                logger.info(f"Procesando página {page_num}/{max_pages}: {url}")
                
                if not self.get_page(url):
                    logger.error(f"No se pudo cargar la página {page_num}, continuando...")
                    continue
                
                # Determinar si extraer detalles en esta página
                remaining_details = detail_limit - books_with_details
                extract_details = remaining_details > 0
                
                # Extraer libros de la página actual
                books = self.extract_books_from_page(
                    extract_details=extract_details,
                    detail_limit=remaining_details
                )
                
                # Contar cuántos libros tienen detalles completos
                for book in books:
                    if book.get('upc') is not None:
                        books_with_details += 1
                
                all_books.extend(books)
                
                logger.info(f"Página {page_num} completada. Libros: {len(books)}, Con detalles: {books_with_details}/{detail_limit}")
                
                # Si ya tenemos suficientes libros con detalles, solo extraer info básica
                if books_with_details >= detail_limit:
                    logger.info(f"Alcanzado límite de {detail_limit} libros con detalles completos")
                
                # Esperar antes de la siguiente página
                if page_num < max_pages:
                    self.wait_between_requests()
            
            except Exception as e:
                logger.error(f"Error al procesar página {page_num}: {e}")
                continue
        
        logger.info(f"Scraping completado. Total: {len(all_books)} libros, Con detalles: {books_with_details}")
        return all_books
