from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Measurement

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        labels = {
            'username': 'Nom d\'utilisateur',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
            'email': 'Adresse e-mail',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Measurement

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['name', 'habit', 'pant_size', 'phone_number']
        labels = {
            'name': 'Nom du client',
            'habit': "Mesure de l'habit",
            'pant_size': 'Mesure du pantalon',
            'phone_number': 'Numéro de téléphone',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'habit': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'pant_size': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
