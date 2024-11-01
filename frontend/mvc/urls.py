# accounts/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),  # Logout sayfası
    path('create-piece/', create_piece_view, name='create_piece'),  # Yeni parça üretme sayfası
    path('pieces/', list_pieces_view, name='list_pieces'), 
    path('airplane/create/', create_airplane_view, name='create_airplane'),
    path('airplane/attach-piece/', attach_piece_view, name='attach_piece'),
    path('airplanes/', list_airplanes_view, name='airplane_plan'),
    path('manage-airplanes/', manage_airplanes_view, name='manage_airplanes'),
]
