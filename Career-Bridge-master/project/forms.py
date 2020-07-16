# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Project

class SignMouForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('company_mou', 'company_remarks')
        widgets = {
            'company_mou': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'company_remarks': forms.Textarea(attrs={'class': 'form-control', 'cols': 3, 'rows': 5}),
        }
    
class RegisterProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'project_description', 'start_date', 'end_date', 'bidding_start', 'bidding_end')
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter...'}),  
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter...', 'cols': 3, 'rows': 5}),            
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker'}),
            'bidding_start': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker'}),
            'bidding_end': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker'}),
        }

    
    def save(self, commit=True):
        project = super(RegisterProject, self).save(commit=False)        
        return project