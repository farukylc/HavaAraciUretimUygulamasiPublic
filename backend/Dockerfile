# Backend için base image
FROM python:3.9.17

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyasını backend klasöründen kopyala
COPY requirements.txt .

# Gereksinimleri yükle
RUN pip install -r requirements.txt

# Kodları kopyala
COPY . .

# Django için ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1

# Django development server'ı host dışından erişilebilir yapacak şekilde başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
