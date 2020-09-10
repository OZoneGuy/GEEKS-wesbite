from django.shortcuts import get_object_or_404, render, redirect

from .models import Event, NewEventForm, EditEventForm


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


def new(request):
    if (request.method == 'POST'):
        form = NewEventForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data
            event = Event(title=data.get('title'),
                          short_desc=data.get('short_desc'),
                          long_desc=data.get('long_desc'),
                          start_time=data.get('start_time'),
                          end_time=data.get('end_time'),
                          banner=data.get('banner'))
            event.save()
            return redirect('events:details', id=event.id)
    else:
        form = NewEventForm()
    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'events:new',
                                               'title': 'New Event'})
    pass


def edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if (request.method == 'POST'):
        form = EditEventForm(request.POST, request.FILE)
        if (form.is_valid()):
            data = form.cleaned_data

            event.title = data.get('title')
            event.short_desc = data.get('short_desc')
            event.longs_desc = data.get('longs_desc')
            event.start_time = data.get('start_time')
            event.end_time = data.get('end_time')
            event.banner = data.get('banner')

            event.save()
            return redirect('events:details', id=event.id)
    else:
        data = {
            'title': event.title,
            'short_desc': event.short_desc,
            'long_desc': event.long_desc,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'banner': event.banner,
        }
        form = NewEventForm(initial=data)
    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'events'
                                               ':edit ' + event_id,
                                               'title': 'New Event'})
    pass
