from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Article
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article
from django.http import Http404

def article_search_view(request):
    query = request.GET.get('q')
    # qs = Article.objects.all()
    # if query is not None:
        # lookups = Q(tittle__icontains=query) | Q(content__icontains=query)
    qs = Article.objects.search(query=query)
    context= {
            "object_list":qs
    }
    return render(request, "search.html", context=context)



def details_view(request, slug=None, *args, **kwargs):
    obj = None
    if slug is not None:
        try:
            obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
           return  render(request,'https://www.mantralabsglobal.com/404')
        except Article.MultipleObjectsReturned:
            obj = Article.objects.filter(slug=slug).first()
        except:
          raise Http404
    context = {
    "object": obj
             }
    return render(request, "detail.html",context)


def articles_show_view(request):

        article_obj = Article.objects.all()
        context = {
        "object": article_obj
           }
        return render(request, "home.html", context=context)


@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
      article_object = form.save()
      context['form'] = ArticleForm()
    # if request.method == "POST":
#     tittle = form.cleaned_data.get("tittle")
#     content = form.cleaned_data.get("content")
# article_object = Article.objects.create(tittle=tittle, content=content)
#  context['object'] = article_object
#  context['created'] = True
    return render(request, "create.html", context=context)

def home(request):
    return render(request, "home.html")
