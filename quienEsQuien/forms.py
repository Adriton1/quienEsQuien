from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserResgisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label = 'Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput)
    pruebaRealizada = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'pruebaRealizada']
        help_texts = {k:"" for k in fields}