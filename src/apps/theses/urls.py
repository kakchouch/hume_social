from django.urls import path
from . import views

app_name = 'theses'

urlpatterns = [
    path('', views.thesis_list, name='list'),
    path('<int:pk>/', views.thesis_detail, name='detail'),
    path('create/', views.thesis_create, name='create'),
    path('<int:pk>/edit/', views.thesis_edit, name='edit'),
]
