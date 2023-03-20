from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import datetime

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ApplicationForm(forms.ModelForm):
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Application
        fields = ['full_name', 'email', 'date_of_birth', 'matric_no', 'school', 'level', 'department', 'cgpa', 'picture', 'admission_letter', 'result', 'national_identification', 'id_card']
