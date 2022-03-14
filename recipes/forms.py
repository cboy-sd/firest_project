from django import forms

from .models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeForm(forms.ModelForm):
    errors_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                         "place_holder": "Recipe name"}))
    # descriptions = forms.CharField(widget=forms.Textarea(attrs={"row": 0}))

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']
#
# def __init__(self, *args, **kwargs):
#         super.__init__(*args, **kwargs)
#         for field in self.fields:
#             new_data = {
#                 "placeholder": f'Recipe{str(field)}',
#                 "class": 'form-control'
#             }
#         self.fields[str(field)].widget.atrrs.update(
#             new_data
#         )


class RecipeIngredientimageForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredientImage
        fields = ['img']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']
