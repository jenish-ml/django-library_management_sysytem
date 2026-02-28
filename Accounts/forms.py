from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MemberRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']