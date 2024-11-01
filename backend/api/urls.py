from django.urls import path
from . import views

urlpatterns = [
    path("person/register", views.CreatePersonView.as_view(), name="create-person"),
    path("departmen/create",views.CreateDepartmanView.as_view(), name="create-departmen"),
    path("person/person-list", views.PersonListView.as_view(), name="person-list"),
    path("piece/create",views.CreateIHAPieceView.as_view(), name="create-piece"),
    path("piece/count",views.PartCountView.as_view(), name="piece-count"),
    path('ihapiece/create/', views.IHAPieceCreateView.as_view(), name='ihapiece-create'),
    path('ihapiece/piece-list/', views.IHAPieceListView.as_view(), name='ihapiece-list'),
    path('airplane/create/', views.AirplaneCreateView.as_view(), name='airplane-create'),
    path('airplane-piece/create/', views.AirplanePieceCreateView.as_view(), name='airplanepiece-create'),
    path('airplane/airplane-list', views.AirplaneListView.as_view(), name='airplane-list'),
    path('department/department-list',views.DepartmanListView.as_view(), name = 'department-list'),
    path('ihapiece/delete/<int:pk>',views.DeleteIHAPieceView.as_view(), name='ihapiece-delete'),
    path('ihapiece/type/<str:piece_type>/', views.PieceByTypeView.as_view(), name='piece_by_type'),

]
