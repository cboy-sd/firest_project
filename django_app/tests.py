from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django_app.models import Article
from django.utils.text import slugify
from .utils import slugify_instance_tittle


class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 500
        for i in range(0, self.number_of_articles):
            Article.objects.create(tittle='Hello world',
                                   content='something  amaxing write here ')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        tittle = obj.tittle
        slug = obj.slug
        slugified_tittle = slugify(tittle)
        self.assertEqual(slug, slugified_tittle)

    def test_slugify_instance_tittle(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(0, 25):
            instance = slugify_instance_tittle(obj, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_instance_tittle_redux(self):
        slugs_list = Article.objects.all().values_list('slug', flat=True)
        unique_slugs_list = list(set(slugs_list))
        print(unique_slugs_list)
        self.assertEqual(len(slugs_list), len(unique_slugs_list))

    def test_article_search_manager(self):
        qs = Article.objects.search(query='hello mr cboy')
        self.assertEqual(qs.count(), self.number_of_articles)
        qs = Article.objects.search(query='learning ')
        self.assertEqual(qs.count(), self.number_of_articles)
