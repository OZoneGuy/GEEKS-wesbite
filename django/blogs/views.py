from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Blog, EditBlogForm, NewBlogForm


# Create your views here.
def index(request):
    context = {
        'blogs': Blog.objects.all()
    }
    return render(request, "blogs/index.html", context=context)


def details(request, blog_id):
    context = {
        'blog': get_object_or_404(Blog, pk=blog_id)
    }
    return render(request, "blogs/details.html", context=context)


@permission_required('blogs.add_blog', raise_exception=True)
def new(request):
    if (request.method == 'POST'):
        form = NewBlogForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data
            blog = Blog(title=data.get('title'),
                        body=data.get('body'),
                        author=request.user.first_name + " "
                        "" + request.user.last_name)
            blog.save()
            return redirect('blogs:details', blog_id=blog.id)
    else:
        form = NewBlogForm()
    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'blogs:new',
                                               'submit': 'Create Blog',
                                               'title': 'New Blog'})
    pass


@permission_required('blogs.change_blog', raise_exception=True)
def edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if (request.method == 'POST'):
        form = EditBlogForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data

            blog.title = data.get('title')
            blog.body = data.get('body')

            blog.save()
            return redirect('blogs:details', blog_id=blog.id)
    else:
        data = {
            'title': blog.title,
            'body': blog.body,
        }
        form = NewBlogForm(initial=data)
    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'blogs:edit',
                                               'argument': blog_id,
                                               'submit': 'Update Blog',
                                               'title': 'Edit Blog'})
    pass
