# Multi-stage build for production
FROM python:3.13-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy dependency files
COPY pyproject.toml ./

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies (production only, no dev dependencies)
RUN poetry install --no-dev --no-interaction --no-ansi

# Production stage
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENV=production

# Create non-root user for security
RUN useradd -m -u 1000 monagent && \
    mkdir -p /app && \
    chown -R monagent:monagent /app

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=monagent:monagent src/ ./src/
COPY --chown=monagent:monagent pyproject.toml ./

# Switch to non-root user
USER monagent

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "monagent.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
