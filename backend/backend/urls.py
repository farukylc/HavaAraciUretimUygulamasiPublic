from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name="get-token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/person/register/",CreatePersonView.as_view(), name="register"),
    path("api/departman/create", CreateDepartmanView.as_view(), name="departmen-create"),
    path("api/person/person-list", PersonListView.as_view(), name="person-list"),
    path('api/ihapiece/create/', IHAPieceCreateView.as_view(), name='ihapiece-create'),
    path('api/airplane/create/', AirplaneCreateView.as_view(), name='airplane-create'),
    path('api/airplane-piece/create/', AirplanePieceCreateView.as_view(), name='airplanepiece-create'),
    path('api/airplane/airplane-list', AirplaneListView.as_view(), name='airplane-list'),
    path('api/ihapiece/piece-list/', IHAPieceListView.as_view(), name='ihapiece-list'),
    path('api/department/department-list',DepartmanListView.as_view(), name = 'department-list'),
    path('api/ihapiece/delete/<int:pk>',DeleteIHAPieceView.as_view(), name='ihapiece-delete'),
    path('api/ihapiece/type/<str:piece_type>/', PieceByTypeView.as_view(), name='piece_by_type'),





]
