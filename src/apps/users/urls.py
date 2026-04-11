from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='list'),
    path('contacts/requests/', views.contact_requests, name='contact_requests'),
    path('contacts/requests/<int:pk>/', views.contact_request_decision, name='contact_request_decision'),
    path('<int:pk>/contact-request/', views.send_contact_request, name='send_contact_request'),
    path('sponsorship/requests/', views.sponsorship_requests, name='sponsorship_requests'),
    path('sponsorship/requests/<int:pk>/', views.sponsorship_decision, name='sponsorship_decision'),
    path('<int:pk>/', views.user_detail, name='detail'),
]
