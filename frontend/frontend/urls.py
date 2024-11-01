# frontend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),  # Proje ilk açıldığında login sayfasına yönlendir
    path('', include('mvc.urls')),           # accounts uygulamasındaki diğer URL'ler
]
