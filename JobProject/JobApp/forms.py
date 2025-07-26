from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserRole,Job,Application

class UserRegistrationForm(UserCreationForm):

    role = forms.ChoiceField(choices=UserRole.Role.choices)
    class Meta:
        model = User
        fields = ['username','email','role']
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','company_name','location','description']        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume','cover_letter']       