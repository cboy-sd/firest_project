from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
       class Meta:
           model = Article
           fields =['tittle','content']
       def clean(self):
           data = self.cleaned_data
           tittle = data.get("tittle")
           qs= Article.objects.filter(tittle=tittle)
           if qs.exists():
            self.add_error("tittle",f"\"{tittle}\" is already in use ")
           return data

class ArticleFormOld(forms.Form):
     tittle = forms.CharField()
     content = forms.CharField()

     # def clean_title(self):
     #       cleaned_data = self.cleaned_data
     #       print("cleaned data", cleaned_data)
     #       tittle = cleaned_data.get('tittle')
     #       if tittle.lower().strip() == "hi mr mohamed":
     #              raise forms.validationError("the title is hass been taken ")
     #       print("tittle",tittle)
     #       return  tittle