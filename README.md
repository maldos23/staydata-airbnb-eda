# StayData Lab — Análisis exploratorio de *Airbnb price prediction*

Actividad 2 del reto: carga, revisión estructural, consultas, estadísticas
descriptivas, detección de anomalías y visualizaciones sobre la base
**Airbnb price prediction** (74,080 anuncios · 29 columnas · 6 ciudades de EE. UU.).

Esta etapa **describe** la base; **no** la limpia ni la modela. La limpieza formal
corresponde a la Actividad 3.

---

## Cómo ejecutar

### Opción A — Docker (recomendada)

```bash
# 1. Coloca el archivo original en data/raw/ con este nombre exacto:
#    data/raw/airbnb_price_prediction.xlsx

# 2. Análisis completo: imprime el resumen y escribe las gráficas en reports/figures/
docker compose run --rm eda

# 3. Notebook interactivo en http://localhost:8888 (sin token)
docker compose up lab

# 4. Pruebas unitarias
docker compose run --rm tests
```

La primera corrida reconstruye el workbook (~1 minuto) y guarda una copia en
Parquet dentro de `data/interim/`; las siguientes tardan segundos. Para forzar la
relectura del archivo original: `docker compose run --rm eda python -m staydata_eda.main --no-cache`.

### Opción B — entorno local

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export PYTHONPATH=src            # Windows PowerShell: $env:PYTHONPATH="src"
python -m staydata_eda.main      # CLI
jupyter lab notebooks/01_exploratory_analysis.ipynb   # notebook
pytest tests -q                  # pruebas
```

### Sitio web (dashboard)

`--site` vuelca todo lo que imprime la ejecución en `site/data.js` (un único
`window.DATA`) y copia las figuras a `site/figures/`. El sitio es HTML estático
sin build: lee esas variables y las pinta.

```bash
python -m staydata_eda.main --site        # regenera site/data.js + site/figures/
python -m http.server -d site 8000        # verlo en http://localhost:8000
```

Despliegue en Vercel: importar el repositorio y dejar *Framework Preset* en
`Other`; `vercel.json` ya fija `outputDirectory: site`. La integración Git de
Vercel redespliega en cada commit a `main`, así que no hace falta un workflow de
GitHub Actions. Los números del sitio cambian cuando se vuelve a correr el
análisis en local (el `.xlsx` no está versionado) y se commitea `site/data.js`.

---

### Dónde va la base

El archivo `.xlsx` **no está versionado** (pesa 37 MB y está ignorado en
`.gitignore`). Descárgalo de la plataforma del curso y colócalo en:

```
data/raw/airbnb_price_prediction.xlsx
```

Si prefieres otra ruta o nombre, expórtalo como variable de entorno:

```bash
export RAW_DATA_PATH=/ruta/a/tu/archivo.xlsx
```

> **Nota sobre el archivo original:** el workbook trae todo el CSV dentro de una
> sola columna, y los registros que rebasan el límite de 32,767 caracteres por
> celda de Excel se derraman en columnas adicionales. El repositorio de datos
> reconstruye cada registro antes de entregar la tabla; el archivo original nunca
> se modifica.

---

## Estructura del proyecto

```
staydata-airbnb-eda/
├── src/staydata_eda/
│   ├── domain/              # Capa de dominio: sin dependencias externas
│   │   ├── entities.py      #   value objects inmutables
│   │   ├── ports.py         #   interfaces (ListingRepository, AnomalyRule, ChartStrategy)
│   │   └── schema.py        #   nombres de columna: única fuente de verdad
│   ├── application/         # Casos de uso y lógica de análisis
│   │   ├── profiling.py     #   perfilado estructural y estadísticas
│   │   ├── anomalies.py     #   reglas de calidad de datos
│   │   └── use_cases.py     #   RunExploratoryAnalysis
│   ├── infrastructure/      # Adaptadores concretos
│   │   ├── repositories.py  #   lectura del Excel, caché en Parquet, CSV
│   │   ├── plotting.py      #   estrategias de gráficas + renderer matplotlib
│   │   └── config.py        #   settings desde variables de entorno
│   ├── container.py         # Composition root (inyección de dependencias)
│   └── main.py              # Entrada por CLI
├── notebooks/01_exploratory_analysis.ipynb
├── tools/build_notebook.py  # genera el notebook desde código
├── tests/test_analysis.py
├── reports/figures/         # PNG generados
├── Dockerfile · docker-compose.yml · requirements.txt
```

## Decisiones de diseño

**Clean architecture.** Las dependencias apuntan hacia adentro: `infrastructure`
conoce a `application`, `application` conoce a `domain`, y `domain` no conoce a
nadie. El `container.py` es el único módulo que ve todas las clases concretas.

**Patrones aplicados**

| Patrón | Dónde | Para qué |
|---|---|---|
| Repository | `ListingRepository` + `ExcelListingRepository` | aislar el origen de los datos |
| Decorator | `ParquetCachedRepository` | añadir caché sin tocar el lector |
| Strategy | `AnomalyRule`, `ChartStrategy` | agregar reglas o gráficas sin modificar código existente |
| Factory Method | `AnomalyDetector.with_default_rules()` | construir el conjunto de reglas del reto |
| Composition Root | `container.py` | inyección de dependencias en un solo lugar |

**SOLID**

- **S** — cada módulo tiene una razón de cambio: el repositorio parsea, el
  profiler describe, las reglas detectan, el renderer dibuja.
- **O** — una gráfica o una regla nueva se agrega registrando una clase; ningún
  archivo existente se edita.
- **L** — `FakeRepository` en las pruebas sustituye al lector de Excel sin que el
  caso de uso lo note.
- **I** — los puertos son mínimos: `ListingRepository` solo expone `load()` y
  `source_description`.
- **D** — la capa de aplicación depende de interfaces, nunca de `openpyxl` ni de
  `matplotlib`.

**DRY** — los nombres de columna viven solo en `domain/schema.py`; el estilo de
las gráficas en un único diccionario; `to_frame()` convierte cualquier conjunto de
dataclasses en tabla.

**Comentarios y docstrings en inglés**, según el criterio de evaluación.

## Salidas generadas

| Archivo | Contenido |
|---|---|
| `reports/figures/fig1_price_distribution.png` | distribución del precio y de `log_price` |
| `reports/figures/fig2_price_by_room_type.png` | precio por tipo de espacio |
| `reports/figures/fig3_price_vs_accommodates.png` | precio mediano por capacidad y tipo de espacio |
| `reports/figures/fig4_price_by_city.png` | precio mediano por ciudad |
| `reports/figures/fig5_missing_values.png` | porcentaje de faltantes por variable |

## Convención de commits

El historial sigue [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `build:`, `refactor:`.
