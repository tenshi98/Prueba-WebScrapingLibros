# 📚 Web Scraping - Books to Scrape (Standalone)

Proyecto completo de web scraping en Python para extraer información de libros desde [books.toscrape.com](https://books.toscrape.com) utilizando **Selenium con Chromium**, diseñado para **ejecución standalone** sin necesidad de instalar dependencias vía pip.

## 🎯 Características

- ✅ **Ejecución standalone**: Usa dependencias del sistema (no requiere `pip install`)
- ✅ **Chromium**: Usa chromedriver del sistema
- ✅ **Extracción inteligente**:
  - Info básica de **3 páginas** del catálogo
  - Detalles completos de **5 libros** (descripción, UPC, categoría)
- ✅ Almacenamiento en base de datos SQLite
- ✅ Detección automática de duplicados por UPC y por Titulo
- ✅ Rate limiting para no sobrecargar el servidor
- ✅ Sistema de logging completo (INFO, WARNING, ERROR)
- ✅ Manejo robusto de errores y reintentos
- ✅ Código modular y bien documentado

## 📋 Requisitos del Sistema

### Obligatorios

- **Python 3.10 o superior**
- **Chromium** (navegador)
- **ChromeDriver** (driver de Selenium para Chromium)
- **Selenium** (librería Python)

### Instalación de Dependencias del Sistema

#### Ubuntu/Debian

```bash
# Instalar Chromium y ChromeDriver
sudo apt update
sudo apt install chromium-browser chromium-chromedriver

# Instalar Selenium a nivel de sistema
sudo apt install python3-selenium
```

#### Fedora/RHEL

```bash
# Instalar Chromium y ChromeDriver
sudo dnf install chromium chromedriver

# Instalar Selenium
sudo dnf install python3-selenium
```

#### Arch Linux

```bash
# Instalar Chromium y ChromeDriver
sudo pacman -S chromium chromedriver

# Instalar Selenium
sudo pacman -S python-selenium
```

#### Verificar Instalación

```bash
# Verificar Chromium
chromium-browser --version

# Verificar ChromeDriver
chromedriver --version

# Verificar Selenium
python3 -c "import selenium; print(selenium.__version__)"
```

## 🚀 Instalación del Proyecto

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tenshi98/Prueba-WebScrapingLibros.git
```

### 2. Verificar estructura

```bash
ls -la
```

Deberías ver:
```
Prueba-WebScrapingLibros/
├── database/
├── scraper/
├── utils/
├── logs/
├── data/
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

### 3. (Opcional) Instalar Selenium vía pip

Si no tienes Selenium a nivel de sistema, puedes instalarlo localmente:

```bash
pip3 install --user selenium
```

## ⚙️ Configuración

El archivo `config.py` contiene todas las configuraciones:

| Parámetro | Valor por defecto | Descripción |
|-----------|-------------------|-------------|
| `MAX_PAGES` | 3 | Número de páginas a extraer |
| `DETAIL_BOOKS_LIMIT` | 5 | Libros con detalles completos |
| `REQUEST_DELAY` | 2 segundos | Delay entre requests |
| `CHROMIUM_DRIVER_PATH` | `/usr/bin/chromedriver` | Path al chromedriver |
| `HEADLESS_MODE` | True | Ejecutar sin interfaz gráfica |

### Ajustar Path de ChromeDriver

Si tu chromedriver está en otra ubicación, edita `config.py`:

```python
# Ubicaciones comunes:
CHROMIUM_DRIVER_PATH = '/usr/bin/chromedriver'           # Ubuntu/Debian
CHROMIUM_DRIVER_PATH = '/usr/local/bin/chromedriver'     # macOS/Fedora
CHROMIUM_DRIVER_PATH = 'chromedriver'                    # Si está en PATH
```

## 🎮 Uso

### Ejecución Básica (Standalone)

```bash
python3 main.py
```

**No requiere activar entorno virtual ni instalar dependencias vía pip** (si ya tienes Selenium en el sistema).

### Salida Esperada

```
================================================================================
Iniciando proceso de web scraping - Books to Scrape (Standalone)
================================================================================
2025-11-21 13:15:00 - books_scraper - INFO - Inicializando base de datos...
2025-11-21 13:15:00 - books_scraper - INFO - Libros en base de datos antes del scraping: 0
2025-11-21 13:15:00 - books_scraper - INFO - Inicializando scraper con Chromium...
2025-11-21 13:15:01 - books_scraper - INFO - Usando chromedriver en: /usr/bin/chromedriver
2025-11-21 13:15:02 - books_scraper - INFO - WebDriver de Chromium inicializado correctamente
2025-11-21 13:15:02 - books_scraper - INFO - Estrategia: Info básica de 3 páginas + detalles completos de 5 libros
2025-11-21 13:15:02 - books_scraper - INFO - Procesando página 1/3
...
================================================================================
Proceso de scraping completado
================================================================================
Libros extraídos: 60
Libros insertados: 60
Libros con detalles completos: 5
Duplicados: 0
Errores: 0
Total en base de datos: 60
================================================================================
```

## 📁 Estructura del Proyecto

```
Prueba-WebScrapingLibros/
├── database/
│   ├── __init__.py
│   └── db_manager.py          # Gestión de base de datos SQLite
├── scraper/
│   ├── __init__.py
│   └── book_scraper.py        # Scraper con Selenium + Chromium
├── utils/
│   ├── __init__.py
│   └── logger.py              # Configuración de logging
├── logs/
│   └── scraper.log            # Archivo de logs (generado automáticamente)
├── data/
│   └── libros.db              # Base de datos SQLite (generado automáticamente)
├── config.py                  # Configuración centralizada
├── main.py                    # Script principal de ejecución
├── requirements.txt           # Dependencias (solo selenium)
└── README.md                  # Este archivo
```

## 🗄️ Esquema de Base de Datos

```sql
CREATE TABLE libros (
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
```

### Datos Extraídos

#### De todas las páginas (info básica):
- ✅ Título del libro
- ✅ Precio
- ✅ Disponibilidad (In stock/Out of stock)
- ✅ Rating (cantidad de estrellas 1-5)
- ✅ URL de la imagen de portada

#### Solo de los primeros 5 libros (detalles completos):
- ✅ Descripción del producto
- ✅ UPC (código único)
- ✅ Categoría

### Consultar Datos

```bash
# Ver total de libros
sqlite3 data/libros.db "SELECT COUNT(*) FROM libros;"

# Ver libros con detalles completos
sqlite3 data/libros.db "SELECT titulo, descripcion IS NOT NULL as tiene_desc, upc FROM libros LIMIT 10;"

# Ver los 5 libros con detalles completos
sqlite3 data/libros.db "SELECT titulo, categoria, upc FROM libros WHERE descripcion IS NOT NULL;"

# Ver libros por categoría
sqlite3 data/libros.db "SELECT categoria, COUNT(*) FROM libros WHERE categoria IS NOT NULL GROUP BY categoria;"
```

## 📦 Módulos

### `config.py`
Configuración centralizada con:
- Rutas de archivos y directorios
- URLs del sitio web
- **Path a chromedriver de Chromium**
- **Límite de libros con detalles completos (5)**
- Parámetros de scraping (delays, timeouts)
- Configuración de Selenium

### `database/db_manager.py`
Gestión de SQLite:
- `create_table()`: Crea la tabla si no existe
- `book_exists(upc)`: Verifica duplicados por UPC
- `insert_book(book_data)`: Inserta libro evitando duplicados
- `get_book_count()`: Obtiene total de libros

### `scraper/book_scraper.py`
Scraper standalone con Chromium:
- `setup_driver()`: Configura Chromium WebDriver del sistema
- `extract_books_from_page()`: Extrae info básica o completa según parámetros
- `extract_book_details()`: Navega a página de detalle y extrae descripción, UPC, categoría
- `scrape_books()`: Ejecuta extracción completa con lógica de límite de detalles

### `utils/logger.py`
Sistema de logging:
- Logs en archivo (`logs/scraper.log`) y consola
- Niveles: INFO, WARNING, ERROR

### `main.py`
Script principal:
- Orquesta scraper y base de datos
- Muestra estadísticas detalladas
- Maneja errores y cierre graceful

## 🔍 Funcionalidades Implementadas

### ✅ Extracción Inteligente

El scraper usa una estrategia optimizada:

1. **Páginas 1-3**: Extrae info básica de todos los libros (~60 libros)
2. **Primeros 5 libros**: Navega a página de detalle y extrae descripción, UPC, categoría
3. **Resto de libros**: Solo info básica (sin navegar a detalles)

Esto reduce el tiempo de ejecución mientras cumple con el requisito de extraer detalles de al menos 5 libros.

### ✅ Detección de Duplicados

El sistema implementa una **validación inteligente de duplicados** con dos niveles:

1. **Prioridad: Validación por UPC**
   - Si el libro tiene UPC, se verifica por este código único
   - Más confiable y preciso

2. **Fallback: Validación por Título**
   - Si el libro NO tiene UPC, se valida por el título
   - Evita duplicados incluso cuando falta información de UPC

**Ejemplo:**
```python
# Libro con UPC: valida por UPC
libro1 = {'titulo': 'Python Basics', 'upc': 'ABC123', ...}
libro2 = {'titulo': 'Python Basics (Edición 2)', 'upc': 'ABC123', ...}
# ❌ Duplicado detectado por UPC (aunque títulos sean diferentes)

# Libro sin UPC: valida por título
libro3 = {'titulo': 'JavaScript Guide', 'upc': None, ...}
libro4 = {'titulo': 'JavaScript Guide', 'upc': None, ...}
# ❌ Duplicado detectado por título
```

### ✅ Rate Limiting
- 2 segundos de delay entre requests
- Evita sobrecargar el servidor
- Configurable en `config.py`

### ✅ Manejo de Errores
- Reintentos automáticos (3 intentos por página)
- Logging detallado de errores
- Continuación del proceso ante errores individuales

### ✅ Logging Completo
- **INFO**: Operaciones normales y progreso
- **WARNING**: Situaciones anómalas no críticas
- **ERROR**: Errores que requieren atención

## 🐛 Troubleshooting

### Error: "chromedriver not found"

```bash
# Verificar si está instalado
which chromedriver

# Si no está, instalar:
sudo apt install chromium-chromedriver  # Ubuntu/Debian
```

### Error: "No module named 'selenium'"

```bash
# Instalar a nivel de sistema
sudo apt install python3-selenium

# O instalar para el usuario
pip3 install --user selenium
```

### Error: "Chrome binary not found"

```bash
# Instalar Chromium
sudo apt install chromium-browser
```

### Chromium en modo visible (no headless)

Edita `config.py`:
```python
HEADLESS_MODE = False
```

### Cambiar número de libros con detalles

Edita `config.py`:
```python
DETAIL_BOOKS_LIMIT = 10  # Extraer detalles de 10 libros
```

## 📊 Ejemplos de Uso

### Ver estadísticas

```bash
# Total de libros
sqlite3 data/libros.db "SELECT COUNT(*) FROM libros;"

# Libros con detalles completos
sqlite3 data/libros.db "SELECT COUNT(*) FROM libros WHERE descripcion IS NOT NULL;"

# Precio promedio
sqlite3 data/libros.db "SELECT AVG(precio) FROM libros;"

# Distribución de ratings
sqlite3 data/libros.db "SELECT rating, COUNT(*) FROM libros GROUP BY rating;"
```

### Exportar a CSV

```bash
sqlite3 -header -csv data/libros.db "SELECT * FROM libros;" > libros.csv
```

### Ver logs

```bash
cat logs/scraper.log
```

## 📝 Notas Importantes

> [!IMPORTANT]
> **Ejecución Standalone**: Este proyecto está diseñado para ejecutarse sin `pip install` usando dependencias del sistema. Asegúrate de tener Chromium, chromedriver y python3-selenium instalados a nivel de sistema.

> [!NOTE]
> **Extracción Selectiva**: Solo los primeros 5 libros tendrán descripción, UPC y categoría completos. El resto solo tendrá información básica (título, precio, rating, disponibilidad, imagen).

> [!TIP]
> Si quieres extraer detalles de más libros, modifica `DETAIL_BOOKS_LIMIT` en `config.py`.

## ⚠️ Disclaimer

Este proyecto es solo para fines educativos. Asegúrate de revisar y respetar los términos de servicio del sitio web que estás scrapeando.

---

**Desarrollado con Python 3.10+ y Selenium + Chromium** 🐍✨
