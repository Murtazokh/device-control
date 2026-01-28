from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list_view, name='device_list'),
    path('<int:pk>/', views.device_detail_view, name='device_detail'),
]