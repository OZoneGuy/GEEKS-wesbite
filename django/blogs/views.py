from django.shortcuts import render, get_object_or_404
from .models import Blog


# Create your views here.
def index(request):
    context = {
        'blog': Blog.objects.all()
    }
    return render(request, "blogs/index.html", context=context)


def details(request, blog_id):
    context = {
        'blog': get_object_or_404(Blog, pk=blog_id)
    }
    return render(request, "blogs/details.html", context=context)
