# Gunakan base image Python
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file.py ke direktori /app di dalam container
COPY predict.py /app/

# Salin requirements.txt ke direktori /app di dalam container
COPY requirements.txt /app/

# Install dependensi Python menggunakan pip
RUN pip install -r requirements.txt

COPY . .

# Expose port yang digunakan oleh Streamlit
EXPOSE 8501

# Jalankan Streamlit ketika container dijalankan
CMD ["streamlit", "run", "predict.py","--server.port=8501", "--server.address="]
