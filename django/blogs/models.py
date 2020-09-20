from django.db import models
from django import forms


# Blog class
# A class responsible for storing blogs/newsletters
class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50)


class NewBlogForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label="Title")
    body = forms.CharField(widget=forms.Textarea,
                           label="Body",
                           help_text="You can use [Markdown]"
                           """(https://www.markdownguide.org/basic-syntax).

Examples:

- `*text*` → *text*
- `**text**` → **text**
- `***text***` → ***text***""")


class EditBlogForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label="Title", initial='title')
    body = forms.CharField(widget=forms.Textarea,
                           label="Body", initial='body',
                           help_text="You can use [Markdown]"
                           """(https://www.markdownguide.org/basic-syntax).

Examples:

- `*text*` → *text*
- `**text**` → **text**
- `***text***` → ***text***""")
