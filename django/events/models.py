from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime


class Event(models.Model):
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=500)
    long_desc = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    banner = models.ImageField(upload_to="events/%Y/%m")


class NewEventForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label='Event Title')
    short_desc = forms.CharField(max_length=500,
                                 widget=forms.Textarea,
                                 help_text='A short description of the event.'
                                 ' No details needed here.',
                                 label='Short Description')
    long_desc = forms.CharField(max_length=500,
                                widget=forms.Textarea,
                                help_text='This should contain all the'
                                ' events details, plus description.  '
                                ""
                                "You can use [Markdown]"
                                """(https://www.markdownguide.org/basic-syntax).

Examples:

- `*text*` → *text*
- `**text**` → **text**
- `***text***` → ***text***""",
                                label='Long Description')
    start_time = forms.DateTimeField(label='Event start time',
                                     help_text='Format: YYYY-MM-DD HH:mm.'
                                     ' 24-hr format.')
    end_time = forms.DateTimeField(label='Event end time',
                                   help_text='Format: YYYY-MM-DD HH:mm.'
                                   ' 24-hr format.')
    banner = forms.FileField(label='Event banner')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time is None or end_time is None:
            return
        if start_time > end_time:
            self.add_error('end_time',
                           ValidationError("End time is before start time."))

        if start_time.replace(tzinfo=None) < datetime.now():
            self.add_error('start_time',
                           ValidationError(
                               "Start time must be in the future."))


class EditEventForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label='Event Title',
                            initial='title')
    short_desc = forms.CharField(max_length=500,
                                 widget=forms.Textarea,
                                 help_text='A short description of the event.'
                                 ' No details needed here.',
                                 label='Short Description',
                                 initial='short_desc')
    long_desc = forms.CharField(max_length=500,
                                widget=forms.Textarea,
                                help_text='This should contain all the'
                                ' events details, plus description.  '
                                ""
                                "You can use [Markdown]"
                                """(https://www.markdownguide.org/basic-syntax).

Examples:

- `*text*` → *text*
- `**text**` → **text**
- `***text***` → ***text***""",
                                label='Long Description',
                                initial='long_desc')
    start_time = forms.DateTimeField(label='Event start time',
                                     initial='start_time')
    end_time = forms.DateTimeField(label='Event end time',
                                   initial='end_time')
    banner = forms.ImageField(label='Event banner',
                              initial='banner',
                              required=False,)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time > end_time:
            self.add_error('end_time',
                           ValidationError("End time is before start time."))

        if start_time.replace(tzinfo=None) < datetime.now():
            self.add_error('start_time',
                           ValidationError(
                               "Start time must be in the future."))
