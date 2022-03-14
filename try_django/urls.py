"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    login_view,
    logout_view,
    register_view,

)
from django_app.views import home, articles_show_view, article_create_view, article_search_view
from django_app.views import details_view

urlpatterns = [
    path('pantry/recipes/', include('recipes.urls')),
    path('articles/search/', article_search_view),
    path('articles/details/<slug:slug>', details_view, name="article_search"),
    path('details/login/', login_view),
    path('articles/', articles_show_view),
    path('', home),
    path('admin/', admin.site.urls),
    path('create/', article_create_view),
    path('logout/', logout_view),
    path('create/search', article_search_view),
    path('register/', register_view),
    path('register/login/', login_view),
    path('register/logout/', logout_view),
]
