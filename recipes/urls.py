from django.urls import path

from .views import (

    recipe_list_view,
    recipe_detail_view,
    recipe_update_view,
    recipe_create_view,
    recipe_delete_view,
    recipe_ingredient_img_upload_view,

)

app_name = 'recipes'

urlpatterns = [

    path("", recipe_list_view, name="list"),
    path("create/", recipe_create_view, name='craete'),
    path("<int:id>", recipe_detail_view, name='detail'),
    path("<int:id>/edit/", recipe_update_view, name='update'),
    path("<int:id>/delete/", recipe_delete_view, name='delete'),
    path("<int:parent_id>/image-upload/", recipe_ingredient_img_upload_view, name="image-upload")

]
