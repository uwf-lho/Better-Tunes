# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container to /app
WORKDIR /app

# Copy the entire server directory into /app (keeping the structure)
COPY ./ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to ensure proper module resolution
ENV PYTHONPATH=/app

# Expose the port Flask is running on
EXPOSE 8080

# Run the Flask application
CMD ["python", "main.py"]
