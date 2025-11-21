"""
Módulo de gestión de base de datos SQLite.
Maneja la creación del schema, inserción de datos y detección de duplicados.
"""

import sqlite3
from typing import Dict, Optional
from contextlib import contextmanager
from config import DB_PATH
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Gestor de base de datos SQLite para almacenar información de libros."""
    
    def __init__(self, db_path: str = DB_PATH):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.create_table()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para manejar conexiones a la base de datos.
        
        Yields:
            Conexión a la base de datos SQLite
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error en la conexión a la base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def create_table(self) -> None:
        """Crea la tabla de libros si no existe."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            precio DECIMAL(10,2),
            disponibilidad TEXT,
            rating INTEGER,
            url_imagen TEXT,
            descripcion TEXT,
            upc TEXT UNIQUE,
            categoria TEXT,
            fecha_extraccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                logger.info("Tabla 'libros' verificada/creada exitosamente")
        except sqlite3.Error as e:
            logger.error(f"Error al crear la tabla: {e}")
            raise
    
    def book_exists(self, upc: Optional[str] = None, titulo: Optional[str] = None) -> bool:
        """
        Verifica si un libro ya existe en la base de datos.
        Prioriza validación por UPC, pero usa título como fallback si UPC no está disponible.
        
        Args:
            upc: Código UPC del libro (opcional)
            titulo: Título del libro (opcional)
        
        Returns:
            True si el libro existe, False en caso contrario
        """
        if not upc and not titulo:
            logger.warning("No se proporcionó UPC ni título para verificar duplicados")
            return False
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Priorizar validación por UPC si está disponible
                if upc:
                    cursor.execute("SELECT 1 FROM libros WHERE upc = ? LIMIT 1", (upc,))
                    exists = cursor.fetchone() is not None
                    if exists:
                        logger.debug(f"Libro encontrado por UPC: {upc}")
                    return exists
                
                # Fallback: validar por título si no hay UPC
                if titulo:
                    cursor.execute("SELECT 1 FROM libros WHERE titulo = ? LIMIT 1", (titulo,))
                    exists = cursor.fetchone() is not None
                    if exists:
                        logger.debug(f"Libro encontrado por título: {titulo}")
                    return exists
                
                return False
        except sqlite3.Error as e:
            logger.error(f"Error al verificar duplicado (UPC: {upc}, Título: {titulo}): {e}")
            return False
    
    def insert_book(self, book_data: Dict) -> bool:
        """
        Inserta un libro en la base de datos si no existe.
        Valida duplicados por UPC si está disponible, o por título como fallback.
        
        Args:
            book_data: Diccionario con los datos del libro
        
        Returns:
            True si se insertó correctamente, False si ya existía o hubo error
        """
        upc = book_data.get('upc')
        titulo = book_data.get('titulo')
        
        # Validar que al menos tengamos título
        if not titulo:
            logger.error("No se puede insertar libro sin título")
            return False
        
        # Verificar si ya existe (por UPC o por título)
        if self.book_exists(upc=upc, titulo=titulo):
            if upc:
                logger.info(f"Libro duplicado (UPC: {upc}), omitiendo: {titulo}")
            else:
                logger.info(f"Libro duplicado (por título), omitiendo: {titulo}")
            return False
        
        insert_sql = """
        INSERT INTO libros (titulo, precio, disponibilidad, rating, url_imagen, descripcion, upc, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_sql, (
                    book_data.get('titulo'),
                    book_data.get('precio'),
                    book_data.get('disponibilidad'),
                    book_data.get('rating'),
                    book_data.get('url_imagen'),
                    book_data.get('descripcion'),
                    book_data.get('upc'),
                    book_data.get('categoria')
                ))
                logger.info(f"Libro insertado exitosamente: {book_data.get('titulo')}")
                return True
        except sqlite3.IntegrityError as e:
            logger.warning(f"Error de integridad al insertar libro (UPC: {upc}): {e}")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error al insertar libro en la base de datos: {e}")
            return False
    
    def get_book_count(self) -> int:
        """
        Obtiene el número total de libros en la base de datos.
        
        Returns:
            Número de libros almacenados
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM libros")
                count = cursor.fetchone()[0]
                return count
        except sqlite3.Error as e:
            logger.error(f"Error al obtener conteo de libros: {e}")
            return 0
