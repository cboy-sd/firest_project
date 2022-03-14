from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientimageForm
from .models import Recipe, RecipeIngredient
from django.forms.models import modelformset_factory
from django.http import Http404






@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    print(qs)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        "object": obj
    }
    return render(request, "recipes/detail.html", context)


@login_required
def recipe_delete_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        success_url = reverse('recipes:list')
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)


def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form,

    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    form_2 = RecipeIngredientForm(request.POST or None)

    context = {

        "form": form,
        "form_2": form_2,
        "object": obj
    }

    if all([form.is_valid(), form_2.is_valid()]):
        form.save(commit=False)
        form_2.save(commit=False)
        context['message'] = 'data saved'
    return render(request, "recipes/create-update.html", context)


def recipe_ingredient_img_upload_view(request, parent_id=None):
    print(request.FILES)
    try:
        perant_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_id = None
    if parent_id is None:
        raise Http404
    form = RecipeIngredientimageForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = perant_obj
        obj.save()
    return render(request, "recipes/image-form.html", {"form": form})
