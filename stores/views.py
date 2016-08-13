from django.shortcuts import render, get_object_or_404

# Create your views here.
from stores.models import Category


def index(request):
    categories = Category.objects.filter(parent=None).order_by('weight')
    return render(request=request, template_name="stores/index.html",
                  context={categories: categories})


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    return render(request=request, template_name="stores/category.html", context={category: cat})