from django import forms
from .models  import CriteriaQuestions
from ads.models import Ad

class QuestionForm(forms.ModelForm):
    

    def __init__(self,*args,**kwargs):
        recruter = kwargs.pop("recruter")
        super(QuestionForm, self).__init__(*args,**kwargs)
        self.fields['ad'] = forms.ChoiceField(label="ad", choices=[(ad.id, ad.name) for ad in Ad.objects.filter(recruter=recruter)])


    class Meta:
        model=CriteriaQuestions
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }



class QuestForm(forms.ModelForm):
    class Meta:
        model=CriteriaQuestions
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
