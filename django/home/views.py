from django.shortcuts import render
from events.models import Event
from blogs.models import Blog
from datetime import datetime


# Create your views here.
def index(request):
    context = {
        'events': Event.objects.filter(start_time__gt=datetime.now()),
        'blogs': Blog.objects.all(),
    }

    return render(request, "home/index.html", context=context)
