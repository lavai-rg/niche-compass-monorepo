# Gunakan base image Python
FROM python:3.11-slim-buster

# Set working directory di dalam kontainer
WORKDIR /app

# Copy requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY . .

# Expose port yang digunakan Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "src/main.py"]


