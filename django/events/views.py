from django.shortcuts import render
from .models import Event


# Create your views here.
def index(request):
    context = {
        'event': Event.objects.all()
    }
    return render(request, "events/index.html", context=context)


def details(request, id):
    context = {
        'event': Event.objects.get(pk=id)
    }
    return render(request, "events/details.html", context=context)
