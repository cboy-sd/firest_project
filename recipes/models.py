import pathlib
import uuid

from django.db import models
from django.conf import settings
from .validaters import validate_unit_of_measure
from .utils import number_str_to_float
from django.urls import reverse
import pint


# Create your models here.
# def recipe_ingredient_image_upload_handeler(filename):
#     fpath = pathlib.Path(filename)
#     new_name = str(uuid.uuid1())
#     return f"recipes/ingredient/{new_name}{fpath.suffix}"


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("recipes:delete", kwargs={"id": self.id})

    def get_ingredients_childern(self):
        return self.recipeingredient_set.all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)  #
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])  # gram ,pound
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute()

    def get_edit_url(self):
        return self.recipeingredient_set.all()

    def get_ingredients_childern(self):
        return self.recipeingredient_set.all()

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement  # .to_base_unit()

    def as_mks(self):
        measurement = self.convert_to_system(system='mks')
        return measurement

    def as_imperial(self):
        measurement = self.convert_to_system(system='imperial')
        return measurement

    def to_ounces(self):
        m = self.convert_to_system()
        return m.to('ounces')

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)


class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="recipes/upload/imges")
