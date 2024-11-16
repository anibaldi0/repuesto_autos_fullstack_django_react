# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Otras rutas...
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Ruta para el login
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registro/', views.registro, name='registro'),  # URL para la vista de registro
]



