# Use official Python image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for building packages
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Run migrations and seed data
RUN python manage.py migrate
RUN python manage.py seed_example

# Expose port 8000 to the outside world
EXPOSE 8000

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]