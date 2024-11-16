# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # El usuario no estará activo hasta validar su correo electrónico
        if commit:
            user.save()

            # Generar token para activación de correo
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

            # Enviar correo de validación
            current_site = 'localhost:8000'  # Asegúrate de usar el dominio correcto
            mail_subject = 'Activa tu cuenta'
            message = render_to_string('usuarios/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'noreply@tudominio.com', [user.email])

        return user


