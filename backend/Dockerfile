FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY ../ ./

# Expose port
EXPOSE 8000

# Run
CMD ["python", "main.py"]
