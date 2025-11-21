"""
Script de prueba para verificar la validación de duplicados.
Prueba la lógica de validación por UPC y por título.
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_duplicate_validation():
    """Prueba la validación de duplicados por UPC y título."""
    
    print("=" * 80)
    print("PRUEBA DE VALIDACIÓN DE DUPLICADOS")
    print("=" * 80)
    
    # Crear instancia del gestor de BD
    db_manager = DatabaseManager()
    
    # Limpiar tabla para pruebas
    print("\n🗑️  Limpiando tabla de pruebas...")
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros")
    print("✅ Tabla limpiada")
    
    # Test 1: Insertar libro con UPC
    print("\n" + "-" * 80)
    print("TEST 1: Insertar libro con UPC")
    print("-" * 80)
    
    libro1 = {
        'titulo': 'Libro de Prueba 1',
        'precio': 19.99,
        'disponibilidad': 'In stock',
        'rating': 5,
        'url_imagen': 'http://example.com/img1.jpg',
        'descripcion': 'Descripción del libro 1',
        'upc': 'ABC123456789',
        'categoria': 'Fiction'
    }
    
    result = db_manager.insert_book(libro1)
    print(f"Resultado inserción: {'✅ Insertado' if result else '❌ No insertado'}")
    
    # Test 2: Intentar insertar duplicado por UPC
    print("\n" + "-" * 80)
    print("TEST 2: Intentar insertar duplicado por UPC")
    print("-" * 80)
    
    libro2 = {
        'titulo': 'Libro de Prueba 1 (Título diferente)',
        'precio': 29.99,
        'disponibilidad': 'In stock',
        'rating': 4,
        'url_imagen': 'http://example.com/img2.jpg',
        'descripcion': 'Descripción diferente',
        'upc': 'ABC123456789',  # Mismo UPC
        'categoria': 'Non-Fiction'
    }
    
    result = db_manager.insert_book(libro2)
    print(f"Resultado inserción: {'❌ Insertado (ERROR!)' if result else '✅ Duplicado detectado correctamente'}")
    
    # Test 3: Insertar libro SIN UPC (solo con título)
    print("\n" + "-" * 80)
    print("TEST 3: Insertar libro SIN UPC (validación por título)")
    print("-" * 80)
    
    libro3 = {
        'titulo': 'Libro Sin UPC',
        'precio': 15.99,
        'disponibilidad': 'In stock',
        'rating': 3,
        'url_imagen': 'http://example.com/img3.jpg',
        'descripcion': None,
        'upc': None,  # Sin UPC
        'categoria': None
    }
    
    result = db_manager.insert_book(libro3)
    print(f"Resultado inserción: {'✅ Insertado' if result else '❌ No insertado'}")
    
    # Test 4: Intentar insertar duplicado por título (sin UPC)
    print("\n" + "-" * 80)
    print("TEST 4: Intentar insertar duplicado por TÍTULO (sin UPC)")
    print("-" * 80)
    
    libro4 = {
        'titulo': 'Libro Sin UPC',  # Mismo título
        'precio': 25.99,
        'disponibilidad': 'Out of stock',
        'rating': 5,
        'url_imagen': 'http://example.com/img4.jpg',
        'descripcion': None,
        'upc': None,  # Sin UPC
        'categoria': None
    }
    
    result = db_manager.insert_book(libro4)
    print(f"Resultado inserción: {'❌ Insertado (ERROR!)' if result else '✅ Duplicado detectado correctamente por título'}")
    
    # Test 5: Insertar libro con título diferente pero sin UPC
    print("\n" + "-" * 80)
    print("TEST 5: Insertar libro con título diferente (sin UPC)")
    print("-" * 80)
    
    libro5 = {
        'titulo': 'Otro Libro Sin UPC',  # Título diferente
        'precio': 12.99,
        'disponibilidad': 'In stock',
        'rating': 4,
        'url_imagen': 'http://example.com/img5.jpg',
        'descripcion': None,
        'upc': None,
        'categoria': None
    }
    
    result = db_manager.insert_book(libro5)
    print(f"Resultado inserción: {'✅ Insertado' if result else '❌ No insertado'}")
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE PRUEBAS")
    print("=" * 80)
    
    count = db_manager.get_book_count()
    print(f"\n📊 Total de libros en BD: {count}")
    print(f"   Esperado: 3 libros (libro1, libro3, libro5)")
    
    if count == 3:
        print("\n✅ TODAS LAS PRUEBAS PASARON")
        print("   - Validación por UPC: ✅")
        print("   - Validación por título (fallback): ✅")
        print("   - Detección de duplicados: ✅")
    else:
        print(f"\n❌ ERROR: Se esperaban 3 libros, pero hay {count}")
    
    print("\n" + "=" * 80)
    
    # Mostrar libros insertados
    print("\n📚 Libros en la base de datos:")
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, upc FROM libros")
        for idx, row in enumerate(cursor.fetchall(), 1):
            upc_str = row[1] if row[1] else "(sin UPC)"
            print(f"   {idx}. {row[0]} - UPC: {upc_str}")
    
    print("\n" + "=" * 80)
    
    return count == 3


if __name__ == "__main__":
    try:
        success = test_duplicate_validation()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Error en las pruebas: {e}", exc_info=True)
        sys.exit(1)
