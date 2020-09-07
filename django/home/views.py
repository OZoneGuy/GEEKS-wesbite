from datetime import datetime

from django.shortcuts import render

from blogs.models import Blog
from events.models import Event


# Create your views here.
def index(request):
    context = {
        'events': Event.objects.filter(start_time__gt=datetime.now()),
        'blogs': Blog.objects.all(),
    }

    return render(request, "home/index.html", context=context)
