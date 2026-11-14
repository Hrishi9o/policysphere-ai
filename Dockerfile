# -------------------------------------------------------------
# Dell PolicySphere™ - Production Container Image
# Multi-stage lightweight deployment container
# -------------------------------------------------------------

FROM python:3.11-slim as base

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install OS dependencies for healthcheck & security
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source & assets
COPY src/ ./src/
COPY data/ ./data/
COPY results/ ./results/
COPY frontend/ ./frontend/
COPY api.py .
COPY benchmark.py .
COPY .env.example .

# Create non-root user for enterprise container security compliance
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME
USER appuser

# Expose HTTP API & UI Port
EXPOSE 8000

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Launch production ASGI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

