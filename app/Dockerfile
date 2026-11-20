# Baseline Dockerfile for Task (a): Standard containerization
FROM python:3.11

WORKDIR /app

# Copy dependency requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose web application port
EXPOSE 5000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Run with Gunicorn WSGI for production readiness
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
