from django import forms
from .models import PhotographerApplication

class AppForm(forms.ModelForm):
    class Meta:
        model= PhotographerApplication
        exclude=['is_rejected','is_employed']