# Multi-stage Docker build for QKD BB84 Protocol Application
# Optimized for production deployment

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 qkd_user

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/qkd_user/.local

# Copy application code
COPY --chown=qkd_user:qkd_user . .

# Set environment variables
ENV PATH=/home/qkd_user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

# Switch to non-root user
USER qkd_user

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')"

# Run with Gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--worker-class", "gthread", "--timeout", "60", "app:app"]
