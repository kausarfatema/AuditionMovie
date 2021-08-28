from django import forms
from .models import User,Photographer,Talent,Category,District,Sector,Province, Recruter,Photographerwork,Feedback, RecruterApp
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	first_name=forms.CharField(max_length=100)
	last_name=forms.CharField(max_length=100)	
	class Meta:
	 	model= User
	 	fields=['username','email','first_name','last_name','password1','password2','province','district','sector','gender']
	 	widget={
			'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
		}
	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['district'].queryset=District.objects.none()
		self.fields['sector'].queryset=Sector.objects.none()

		if 'province' in self.data and 'district' in self.data:
			try:
				province_id=int(self.data.get('province'))
				self.fields['district'].queryset=District.objects.filter(province_id=province_id)
				district_id=int(self.data.get('district'))
				self.fields['sector'].queryset=Sector.objects.filter(district_id=district_id)
			except (ValueError,TypeError):
				pass


class PhotographerForm(forms.ModelForm):
	appid = forms.IntegerField()
	class Meta:
		model=Photographer
		fields=['is_employed']

class PhotographerUpdateForm(forms.ModelForm):
	appid = forms.IntegerField()
	class Meta:
		model=Photographer
		fields=['img']



class TalentForm(forms.ModelForm):
	#category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
	class Meta:
		model=Talent
		exclude=['user','category']



class RecruterForm(forms.ModelForm):
	appid = forms.IntegerField()
	class Meta:
		model= Recruter
		exclude=['user','rec_application']


class VideoForm(forms.Form):
	video=forms.FileField()

class UploadWork(forms.ModelForm):
	class Meta:
		model =  Photographerwork
		exclude = ['photographer']

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['description']

class RecruterappForm(forms.ModelForm):
	class Meta:
		model = RecruterApp
		exclude = ['is_rejected','is_employed']

	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['district'].queryset=District.objects.none()
		self.fields['sector'].queryset=Sector.objects.none()

		if 'province' in self.data and 'district' in self.data:
			try:
				province_id=int(self.data.get('province'))
				self.fields['district'].queryset=District.objects.filter(province_id=province_id)
				district_id=int(self.data.get('district'))
				self.fields['sector'].queryset=Sector.objects.filter(district_id=district_id)
			except (ValueError,TypeError):
				pass

		
		


		
			