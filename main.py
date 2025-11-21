"""
Script principal de ejecución del web scraper standalone.
Orquesta el proceso de scraping y almacenamiento en base de datos.
"""

import sys
from database.db_manager import DatabaseManager
from scraper.book_scraper import BookScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Función principal que ejecuta el proceso de scraping."""
    logger.info("=" * 80)
    logger.info("Iniciando proceso de web scraping - Books to Scrape (Standalone)")
    logger.info("=" * 80)
    
    scraper = None
    db_manager = None
    
    try:
        # Inicializar base de datos
        logger.info("Inicializando base de datos...")
        db_manager = DatabaseManager()
        initial_count = db_manager.get_book_count()
        logger.info(f"Libros en base de datos antes del scraping: {initial_count}")
        
        # Inicializar scraper
        logger.info("Inicializando scraper con Chromium...")
        scraper = BookScraper()
        
        # Ejecutar scraping
        logger.info("Iniciando extracción de libros...")
        logger.info("Estrategia: Info básica de 3 páginas + detalles completos de 5 libros")
        books = scraper.scrape_books()
        
        # Guardar en base de datos
        logger.info(f"Guardando {len(books)} libros en la base de datos...")
        inserted_count = 0
        duplicate_count = 0
        error_count = 0
        books_with_details = 0
        
        for book in books:
            try:
                if db_manager.insert_book(book):
                    inserted_count += 1
                    if book.get('descripcion') and book.get('upc') and book.get('categoria'):
                        books_with_details += 1
                else:
                    duplicate_count += 1
            except Exception as e:
                logger.error(f"Error al insertar libro '{book.get('titulo')}': {e}")
                error_count += 1
        
        # Estadísticas finales
        final_count = db_manager.get_book_count()
        logger.info("=" * 80)
        logger.info("Proceso de scraping completado")
        logger.info("=" * 80)
        logger.info(f"Libros extraídos: {len(books)}")
        logger.info(f"Libros insertados: {inserted_count}")
        logger.info(f"Libros con detalles completos: {books_with_details}")
        logger.info(f"Libros duplicados: {duplicate_count}")
        logger.info(f"Errores: {error_count}")
        logger.info(f"Total en base de datos: {final_count}")
        logger.info("=" * 80)
        
    except KeyboardInterrupt:
        logger.warning("Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error crítico en el proceso de scraping: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cerrar recursos
        if scraper:
            logger.info("Cerrando scraper...")
            scraper.close()
        logger.info("Proceso finalizado")


if __name__ == "__main__":
    main()
