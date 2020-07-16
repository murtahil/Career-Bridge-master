# accounts.forms.py
from django import forms
from .models import Bidding
from project.models import Milestones, Project
from .models import University
from accounts.models import User

class SignMouForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('university_mou', 'university_remarks')
        widgets = {
            'university_mou': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'university_remarks': forms.Textarea(attrs={'class': 'form-control', 'cols': 3, 'rows': 5}),
        }

class ChangeLogoForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ('logo',)
        widgets = {
            'logo': forms.FileInput(attrs={'id': 'wizard-picture'})
        }
    # def clean(self):
    #     cleaned_data = super(ChangeLogoForm, self).clean()
    #     file = cleaned_data.get('logo')
    #     if file:
    #         filename = file.name
    #         if not filename.endswith('.jpg') or not filename.endswith('.png'):
    #             raise forms.ValidationError("File is not valid. Please upload jpg or png file.")
    #     return file
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
        model = University
        fields = ('address',)
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            

        }


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class AddMilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestones
        fields = ('name','description', 'start_date', 'end_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter...', 'cols': 3, 'rows': 5}),
            # 'start_date': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'start_date': DateTimeInput(),
            'end_date': DateTimeInput(),
            # 'end_date': forms.DateTimeInput(attrs={'class': 'form-control date_time_picker', 'type': 'datetime-local'}),
        }

    