from .models import Article
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittle', 'content', 'slug', 'updated', 'timestamp', ]
    search_fields = ['updated', 'tittle']


admin.site.register(Article, ArticleAdmin)



