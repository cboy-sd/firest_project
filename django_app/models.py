from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
import time

User = settings.AUTH_USER_MODEL


# Create your models here.

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(tittle__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    tittle = models.CharField(max_length=120)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    content = models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ArticleManager()
    # updated = models.DateTimeField(auto_now=True)
    # publish = models.DateField(auto_now_add=False , auto_now=False,null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     #obj = Article.objects.get(id=1)
    #     #obj.save()
    #     self.slug = slugify(self.tittle )
    #     super().save(*args, **kwargs)


def get_absolute_url(self):
    return reverse("article_search ")


def slugify_instance_tittle(instance, save=False):
    if instance.slug is None:
        slug = slugify(instance.tittle)
        instance.slug = slug
        instance.save()
        return instance


def article_pre_save(*args, instance, sender, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slug = slugify(instance.tittle) + f"-{time.time()}"
        # qs = Article.objects.filter(slug=slug)
        # print("Article Slug: ", qs.count())
        instance.slug = slug
        # instance.save()


pre_save.connect(article_pre_save, sender=Article)

# def article_post_save(sender, instance, created, *args, **kwargs):
#     # print('post_save')
#     print(args, kwargs)
#     if created:
#         slugify_instance_tittle(instance, save=True)
#
#
# post_save.connect(article_post_save, sender=Article)
