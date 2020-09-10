from django.db import models
from django import forms


# Blog class
# A class responsible for storing blogs/newsletters
class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    last_edit_date = models.DateField(auto_now=True)
    author = models.CharField(max_length=50)
    last_editor = models.CharField(max_length=50)


class NewBlogForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label="Title")
    body = forms.CharField(widget=forms.TextArea,
                           label="Body")


class EditBlogForm(forms.Form):
    title = forms.CharField(max_length=100,
                            label="Title", initial='title')
    body = forms.CharField(widget=forms.TextArea,
                           label="Body", initial='body')
