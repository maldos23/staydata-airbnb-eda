"""Generate the exploratory notebook from a declarative cell list.

Keeping the notebook generated from source avoids hand-edited JSON and keeps the
narrative and the code in one reviewable place.
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

MD = "markdown"
CODE = "code"

CELLS: list[tuple[str, str]] = [
    (MD, """# Actividad 2 — Análisis exploratorio inicial
**Reto StayData Lab · base *Airbnb price prediction***

Este notebook es deliberadamente delgado: toda la lógica vive en el paquete
`staydata_eda` (arquitectura por capas), y aquí solo se orquesta y se muestran
resultados. Así el mismo código corre desde el notebook, desde la CLI
(`python -m staydata_eda.main`) y dentro del contenedor Docker.

| Capa | Contenido |
|---|---|
| `domain` | entidades, puertos (interfaces) y el esquema de columnas |
| `application` | casos de uso, perfilado y reglas de calidad |
| `infrastructure` | lectura del archivo, configuración y gráficas |

**Importante:** esta actividad *no* limpia ni transforma la base. Solo describe.
La limpieza formal corresponde a la Actividad 3."""),

    (MD, "## 1. Configuración y wiring de dependencias"),
    (CODE, """import sys
from pathlib import Path

# Make the package importable when the notebook runs from the notebooks/ folder.
PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd

from staydata_eda.container import build_analysis, configure_logging
from staydata_eda.application.profiling import to_frame
from staydata_eda.domain import schema

configure_logging()
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 40)

# The composition root wires repository + rules + renderer together.
analysis = build_analysis()
print("Proyecto:", PROJECT_ROOT)"""),

    (MD, """## 2. Carga de datos

El archivo original **no se modifica**. El repositorio lo lee en modo lectura y
reconstruye la tabla: el workbook trae todo el CSV dentro de una sola columna y
los registros largos se derraman en columnas adicionales por el límite de 32,767
caracteres por celda de Excel."""),
    (CODE, """listings = analysis.load()
print(f"Filas: {listings.shape[0]:,}   Columnas: {listings.shape[1]}")
print("Registros descartados por comillas mal cerradas:", listings.attrs.get("malformed_records"))"""),

    (MD, "## 3. Estructura general: tipos, nombres y primeras observaciones"),
    (CODE, """listings.info(verbose=True, show_counts=True)"""),
    (CODE, """listings.head(3)"""),
    (CODE, """listings.tail(3)"""),
    (CODE, """from staydata_eda.application.profiling import profile_dataset

profile = profile_dataset(listings)
print(f"{profile.rows:,} filas x {profile.columns} columnas")
print(f"ids duplicados: {profile.duplicated_ids} | filas idénticas: {profile.duplicated_rows}")

structure = to_frame(profile.column_profiles)
structure[["name", "dtype", "non_null", "missing", "missing_pct", "unique"]]"""),

    (MD, """## 4. Consultas básicas

Nombres de columnas, valores únicos de las categóricas relevantes y un vistazo
a los grupos analíticos definidos en la Actividad 1."""),
    (CODE, """print("Columnas disponibles:")
print(list(listings.columns))"""),
    (CODE, """for column in (schema.CITY, schema.ROOM_TYPE, schema.BED_TYPE, schema.CANCELLATION_POLICY):
    print(f"{column} ({listings[column].nunique()} valores únicos):")
    print(listings[column].value_counts().to_string(), "\\n")"""),
    (CODE, """# Cuántos anuncios hay por ciudad y tipo de espacio (consulta cruzada básica).
pd.crosstab(listings[schema.CITY], listings[schema.ROOM_TYPE], margins=True)"""),

    (MD, """## 5. Estadísticas descriptivas de variables numéricas

`log_price` es la variable objetivo. Se agrega `price_usd` (exponencial de
`log_price`) únicamente como columna derivada de lectura, para poder interpretar
los números en dólares."""),
    (CODE, """from staydata_eda.application.profiling import summarise_numeric

to_frame(summarise_numeric(listings))"""),
    (CODE, """listings[[schema.PRICE_USD]].describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.95, 0.99]).round(2)"""),
    (CODE, """# Correlación de Spearman contra la variable objetivo (monotónica, robusta a la asimetría).
numeric_columns = [
    schema.ACCOMMODATES, schema.BEDROOMS, schema.BEDS, schema.BATHROOMS,
    schema.NUMBER_OF_REVIEWS, schema.REVIEW_SCORES_RATING, schema.TARGET,
]
listings[numeric_columns].corr(method="spearman")[schema.TARGET].round(3).sort_values(ascending=False)"""),

    (MD, "## 6. Exploración de variables categóricas"),
    (CODE, """from staydata_eda.application.profiling import summarise_categorical

to_frame(summarise_categorical(listings))"""),
    (CODE, """# Precio mediano por categoría: comparaciones descriptivas, todavía no conclusiones.
for column in (schema.ROOM_TYPE, schema.CITY, schema.CANCELLATION_POLICY, schema.INSTANT_BOOKABLE):
    grouped = listings.groupby(column)[schema.PRICE_USD].agg(["median", "size"]).sort_values("median")
    print(f"--- {column} ---")
    print(grouped.to_string(), "\\n")"""),

    (MD, """## 7. Detección de anomalías

Cada regla es una estrategia independiente. **No se elimina ni se transforma
nada**: solo se documenta el problema y el tratamiento propuesto para después."""),
    (CODE, """from staydata_eda.application.anomalies import AnomalyDetector

findings = AnomalyDetector.with_default_rules().detect(listings)
to_frame(findings)[["code", "title", "severity", "observed", "proposed_treatment"]]"""),

    (MD, """## 8. Visualizaciones exploratorias

Cinco figuras se guardan en `reports/figures/`. La interpretación de cada una
está en el reporte escrito que acompaña a esta entrega."""),
    (CODE, """report = analysis.execute(listings)
for path in report.figures:
    print(path)"""),
    (CODE, """from IPython.display import Image, display

for path in report.figures:
    display(Image(filename=path))"""),

    (MD, """## 9. Cierre

- La base queda descrita, no modificada.
- Los hallazgos y la interpretación de cada figura se desarrollan en el reporte
  `Actividad2_Reporte_EDA.docx`.
- La limpieza (imputación, normalización de formatos, codificación de
  categóricas y tratamiento de atípicos) corresponde a la Actividad 3."""),
]


def build() -> Path:
    """Write the notebook to disk and return its path."""
    notebook = nbf.v4.new_notebook()
    notebook.cells = [
        nbf.v4.new_markdown_cell(source) if kind == MD else nbf.v4.new_code_cell(source)
        for kind, source in CELLS
    ]
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }
    target = Path(__file__).resolve().parents[1] / "notebooks" / "01_exploratory_analysis.ipynb"
    target.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, target)
    return target


if __name__ == "__main__":
    print(build())
