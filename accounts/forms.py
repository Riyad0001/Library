from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['username', 'email', 'first_name','last_name']

class DepositeMoneiForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
