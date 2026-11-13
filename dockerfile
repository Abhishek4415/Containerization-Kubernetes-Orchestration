
# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Application port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]
