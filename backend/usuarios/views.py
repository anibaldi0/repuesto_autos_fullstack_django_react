from django.contrib.auth.forms import UserCreationForm  # Asegúrate de incluir esta importación
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib import messages
from .form import RegistroUsuarioForm

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')  # Redirigir a la página de login o donde sea necesario
    else:
        return render(request, 'usuarios/activation_invalid.html')  # O mostrar un mensaje de error
    
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el nuevo usuario
            return redirect('login')  # Redirigir a la página de login después del registro
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/register.html', {'form': form})


