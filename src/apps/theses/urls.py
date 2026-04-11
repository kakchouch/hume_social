from django.urls import path
from . import views

app_name = 'theses'

urlpatterns = [
    path('', views.thesis_list, name='list'),
    path('<int:pk>/', views.thesis_detail, name='detail'),
    path('<int:pk>/review/', views.thesis_review, name='review'),
    path('create/', views.thesis_create, name='create'),
    path('<int:parent_pk>/follow-up/', views.thesis_create, name='follow_up'),
    path('<int:pk>/edit/', views.thesis_edit, name='edit'),
]
