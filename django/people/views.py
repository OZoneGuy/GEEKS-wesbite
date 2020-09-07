from django.contrib.auth import authenticate
from django.contrib.auth import login as l_in
from django.contrib.auth import logout as l_out
from django.contrib.auth.models import User as U
from django.http import HttpResponse
from django.shortcuts import redirect, render

from models import RegisterForm, User


# Create your views here.
def index(request):
    if (not request.user.is_authenticated):
        return redirect('people:login')
    context = {'user': request.user}
    return render(request, 'people/index.html', context=context)


def login(request):
    if (request.user.is_authenticated):
        return redirect('people:index')
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                l_in(request, user)
                return redirect('home:index')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid Username/Password.")
    if (request.method == 'GET'):
        return render(request, 'people/login.html')


def logout(request):
    if (request.user.is_authenticated):
        l_out(request.user)
    return redirect('home:index')


def register(request):

    if (request.user.is_authenticated):
        return redirect('people:index')

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User(user=U.objects.create_user(
                username=data.get('username'),
                first_name=data.get('f_name'),
                last_name=data.get('l_name'),
                email=data.get('email'),
                password=data.get('password'),
                is_staff=False,
                is_superuser=False,
                is_active=False,))
            l_in(request, user.user)
            return redirect('people:register')

    else:
        form = RegisterForm()

    return render(request, 'people/register.html', {'form': form})
