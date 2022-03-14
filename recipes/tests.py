from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from django.core.exceptions import ValidationError
from .models import Recipe, RecipeIngredient
from django.urls import include

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user_cbo = User.objects.create_user('cbo', password='cbodola17573')
        # self.recipe.objects.create()

    def test_user_pw(self):
        Checked = self.user_cbo.check_password("cbodola17573")
        self.assertTrue(Checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_cbo = User.objects.create_user('cbo', password='cbodola17573')
        self.recipe_a = Recipe.objects.create(
            name='Grilled chicken',
            user=self.user_cbo
        )
        self.recipe_b = Recipe.objects.create(
            name='beef cooked',
            user=self.user_cbo
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='chicken',
            quantity='1/4',
            unit='pounds'
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='chicken',
            quantity='grdnjdj4',
            unit='pounds'
        )

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_cbo
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_cbo
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_cbo
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_reverse(self):
        user = self.user_cbo
        recipeingredient_ids = list(user.recipe_set.all().values('recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        print(qs)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_cbo
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    def test_unit_validation(self):
        invalid_unit = ''
        with self.assertRaises(ValidationError):
            ingredient = RecipeIngredient(
                name='new',
                quantity=10,
                recipe=self.recipe_a,
                unit=invalid_unit,
            )
            ingredient.full_clean()

    def test_unit_validation_error(self):
        invalid_units = ['ndnda', 'gram', 'loyg']
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient(
                    name='new',
                    quantity=10,
                    recipe=self.recipe_a,
                    unit=unit,
                )
                ingredient.full_clean()

    def test_quantity_as_flaot(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
