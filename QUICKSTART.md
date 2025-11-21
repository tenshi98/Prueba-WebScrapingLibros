# 🚀 Inicio Rápido - Books Scraper Standalone

## ⚡ Instalación y Ejecución en 3 Pasos

### 1️⃣ Instalar dependencias del sistema

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install chromium-browser chromium-chromedriver python3-selenium
```

**Fedora:**
```bash
sudo dnf install chromium chromedriver python3-selenium
```

### 2️⃣ Verificar instalación

```bash
chromium-browser --version
chromedriver --version
python3 -c "import selenium; print('Selenium OK')"
```

### 3️⃣ Ejecutar el scraper

```bash
cd /home/tenshi98/.gemini/antigravity/scratch/books_scraper_standalone
python3 main.py
```

---

## 📊 Estrategia de Extracción

- **3 páginas**: Info básica de ~60 libros (título, precio, rating, disponibilidad, imagen)
- **5 libros**: Detalles completos (+ descripción, UPC, categoría)

---

## 📋 Comandos Útiles

### Ver datos extraídos
```bash
# Total de libros
sqlite3 data/libros.db "SELECT COUNT(*) FROM libros;"

# Libros con detalles completos
sqlite3 data/libros.db "SELECT titulo, categoria FROM libros WHERE descripcion IS NOT NULL;"

# Ver logs
cat logs/scraper.log
```

### Exportar a CSV
```bash
sqlite3 -header -csv data/libros.db "SELECT * FROM libros;" > libros.csv
```

---

## ⚙️ Configuración Rápida

Edita `config.py`:

```python
MAX_PAGES = 3                    # Páginas a extraer
DETAIL_BOOKS_LIMIT = 5           # Libros con detalles completos
REQUEST_DELAY = 2                # Segundos entre requests
HEADLESS_MODE = True             # False para ver el navegador
CHROMIUM_DRIVER_PATH = '/usr/bin/chromedriver'  # Ajustar si es necesario
```

---

## 🐛 Troubleshooting

### ChromeDriver no encontrado
```bash
# Verificar ubicación
which chromedriver

# Si está en otro lugar, editar config.py:
CHROMIUM_DRIVER_PATH = '/ruta/a/chromedriver'
```

### Selenium no encontrado
```bash
# Instalar a nivel de sistema
sudo apt install python3-selenium

# O para el usuario
pip3 install --user selenium
```

---

## 📚 Más Información

Ver **README.md** para documentación completa.
