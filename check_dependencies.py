"""
Script de verificación de dependencias del sistema para ejecución standalone.
"""

import sys
import os


def check_python_version():
    """Verifica la versión de Python."""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (se requiere 3.10+)")
        return False


def check_selenium():
    """Verifica que Selenium esté instalado."""
    print("\n📦 Verificando Selenium...")
    try:
        import selenium
        print(f"  ✅ Selenium {selenium.__version__}")
        return True
    except ImportError:
        print("  ❌ Selenium no encontrado")
        print("     Instalar: sudo apt install python3-selenium")
        print("     O: pip3 install --user selenium")
        return False


def check_chromedriver():
    """Verifica que chromedriver esté disponible."""
    print("\n🚗 Verificando ChromeDriver...")
    
    # Verificar paths comunes
    common_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver',
        'chromedriver'
    ]
    
    for path in common_paths:
        if path == 'chromedriver':
            # Verificar en PATH
            import shutil
            if shutil.which('chromedriver'):
                print(f"  ✅ chromedriver encontrado en PATH")
                return True
        elif os.path.exists(path):
            print(f"  ✅ chromedriver encontrado en: {path}")
            return True
    
    print("  ❌ chromedriver no encontrado")
    print("     Instalar: sudo apt install chromium-chromedriver")
    return False


def check_chromium():
    """Verifica que Chromium esté instalado."""
    print("\n🌐 Verificando Chromium...")
    
    import shutil
    chromium_names = ['chromium-browser', 'chromium', 'google-chrome']
    
    for name in chromium_names:
        if shutil.which(name):
            print(f"  ✅ {name} encontrado")
            return True
    
    print("  ❌ Chromium no encontrado")
    print("     Instalar: sudo apt install chromium-browser")
    return False


def check_project_structure():
    """Verifica la estructura del proyecto."""
    print("\n📁 Verificando estructura del proyecto...")
    
    required_files = [
        'config.py',
        'main.py',
        'requirements.txt',
        'README.md',
        'database/__init__.py',
        'database/db_manager.py',
        'scraper/__init__.py',
        'scraper/book_scraper.py',
        'utils/__init__.py',
        'utils/logger.py',
    ]
    
    required_dirs = [
        'database',
        'scraper',
        'utils',
        'logs',
        'data',
    ]
    
    all_ok = True
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - NO ENCONTRADO")
            all_ok = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - NO ENCONTRADO")
            all_ok = False
    
    return all_ok


def main():
    """Ejecuta todas las verificaciones."""
    print("=" * 80)
    print("VERIFICACIÓN DE DEPENDENCIAS - BOOKS SCRAPER STANDALONE")
    print("=" * 80)
    
    checks = [
        check_python_version(),
        check_selenium(),
        check_chromedriver(),
        check_chromium(),
        check_project_structure()
    ]
    
    print("\n" + "=" * 80)
    if all(checks):
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("El proyecto está listo para ejecutarse en modo standalone")
        print("\nEjecutar con: python3 main.py")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("Por favor, instala las dependencias faltantes antes de ejecutar")
    print("=" * 80)
    
    return all(checks)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
