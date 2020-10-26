from datetime import datetime

from django.shortcuts import render

from blogs.models import Blog
from events.models import Event


# Create your views here.
def index(request):
    context = {
        'events': Event.objects.filter(start_time__gt=datetime.now()
                                       ).order_by('start_time')[:5].reverse(),
        'blogs': Blog.objects.all().order_by('last_edit_date')[:5].reverse(),
    }

    return render(request, "home/index.html", context=context)


def about_us(request):
    return render(request, "home/about_us.html")


def weeklies(request):
    return render(request, "home/weeklies.html")
