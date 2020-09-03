from django.shortcuts import render, get_object_or_404
from .models import Event


# Create your views here.
def index(request):
    context = {
        'event': Event.objects.all()
    }
    return render(request, "events/index.html", context=context)


def details(request, event_id):
    context = {
        'event': get_object_or_404(Event, pk=event_id)
    }
    return render(request, "events/details.html", context=context)
