from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('available/', AvailableView.as_view(), name='available'),
    path('info/<int:pk>/', DetailView, name='info'),
    path('apply/<int:pk>/', ApplicationView, name='apply'),
    path('register/', RegisterView, name='register'),
    path('application/<int:pk>/', StatusView, name='status'),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'), 
    path('application/edit/<int:pk>/', EditView, name='edit'), 
    path('send/<int:pk>/', apply_mail, name='send_mail')
]
