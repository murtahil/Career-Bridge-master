# accounts.forms.py
from django import forms
from .models import Company
from accounts.models import User

class ChangeLogoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('logo',)
        widgets = {
            'logo': forms.FileInput(attrs={'id': 'wizard-picture'})
        }    

class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'phone', 'website')
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'})

        }

class EditUniversityInfoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('address',)
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            

        }