from django.shortcuts import render, redirect
from django.contrib.auth import login as l_in, logout as l_out, authenticate
from models import RegisterForm


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
                return HttpResponse("Your account was inactive.")
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
            form.save()
            return redirect('people:register')

    else:
        form = RegisterForm()

    return render(request, 'people/register.html', {'form': form})
