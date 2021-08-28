from django import forms
from .models import Ad, Application



class Adform(forms.ModelForm):
	class Meta:
		model=Ad
		exclude=['talents','recruter']

class ApplicationForm(forms.ModelForm):
	class Meta:
		model=Application
		exclude=['ads','talent','application_status']

	