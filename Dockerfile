# Reproducible environment for the StayData Lab exploratory analysis.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PROJECT_ROOT=/app \
    MPLBACKEND=Agg

WORKDIR /app

# Dependencies first so the layer is cached across code changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tools/ ./tools/
COPY notebooks/ ./notebooks/
COPY tests/ ./tests/

# data/ and reports/ are bind-mounted at run time (see docker-compose.yml).
VOLUME ["/app/data", "/app/reports"]

EXPOSE 8888

# Default: run the full exploratory pass and write the figures.
CMD ["python", "-m", "staydata_eda.main"]
