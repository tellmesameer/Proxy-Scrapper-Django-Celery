# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev curl

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Copy the .env file (make sure it exists at the root)
COPY .env /app/

# **Create the logs directory before collectstatic**
RUN mkdir -p logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (Gunicorn will serve on 8000)
EXPOSE 8000

# Start Gunicorn (production server)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
