import uuid
from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth import login as l_in
from django.contrib.auth import logout as l_out
from django.contrib.auth.models import User as U
from django.shortcuts import redirect, render

from .models import Account, LoginForm, RegisterForm


# Create your views here.
def index(request):
    if (not request.user.is_authenticated):
        return redirect('people:login')
    context = {'member': request.user.account}
    return render(request, 'people/index.html', context=context)


def login(request):
    if (request.user.is_authenticated):
        return redirect('people:account')
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    l_in(request, user)
                    return redirect('people:account')
                else:
                    form.add_error('username',
                                   "Account is inactive."
                                   " Contact Admin for activation.")
            else:
                form.add_error('password', "Wrong Username or Password")
    else:
        form = LoginForm()
    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'people:login',
                                               'submit': 'Login',
                                               'title': 'Login'})


def logout(request):
    if (request.user.is_authenticated):
        l_out(request)
    return redirect('home:index')


def register(request):

    if (request.user.is_authenticated):
        return redirect('people:account')

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = U.objects.create_user(
                username=data.get('username'),
                first_name=data.get('f_name'),
                last_name=data.get('l_name'),
                email=data.get('email'),
                password=data.get('password'),
                is_staff=False,
                is_superuser=False,
                is_active=True,)

            user.save()

            is_member: bool
            mem_uuid: uuid
            if date.today() < date(year=2020, month=10, day=1):
                is_member = True
                mem_uuid = uuid.uuid4()

                account = Account(user=user,
                                  is_member=is_member,
                                  member_code=mem_uuid)
            else:
                account = Account(user=user)

            account.save()
            l_in(request, user)
            return redirect('people:register')

    else:
        form = RegisterForm()

    return render(request, 'misc/forms.html', {'form': form,
                                               'target': 'people:register',
                                               'submit': 'Register',
                                               'title': 'Register'})
