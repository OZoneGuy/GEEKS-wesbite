import uuid
from datetime import date
from io import BytesIO
from tempfile import NamedTemporaryFile, TemporaryFile

import qrcode
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as l_in
from django.contrib.auth import logout as l_out
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User as U
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from fpdf import FPDF

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


@permission_required('people.make_member', raise_exception=True)
def memberships(request):
    if ('member' in request.GET):
        acc = get_object_or_404(Account, pk=request.GET['member'])
        if (acc.make_member):
            return HttpResponse('Given membership successfully.')
        else:
            return HttpResponse('Failed to give membership.'
                                ' Please contact admin.')
    else:
        context = {'members':
                   Account.objects.filter(pending_member__exact=True)}
        return render(request, 'people/memberships.html', context=context)


@permission_required('people.see_members', raise_exception=True)
def members(request):
    if (request.POST):
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        is_member = request.POST['is_member']
        context = {"members": Account.objects.filter(
            user__first_name__icontains=f_name,
            user__last_name__icontains=l_name,
            is_member=is_member == "yes")}
        pass
    else:
        context = {"members": Account.objects.all()}
        pass
    return render(request, 'people/members.html', context=context)


def change_pass(request):
    if (not request.user.is_authenticated):
        return redirect('people:login')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'misc/forms.html', {
        'form': form,
        'target': "people:password",
        'submit': "Change Password",
        'title': "Change Password"
    })


def card(request):
    if (not request.user.is_authenticated):
        return redirect('people:login')
    account = request.user.account
    pdf = FPDF('L', 'mm', (51, 89))

    pdf.add_page()
    pdf.image('/usr/static/img/people/front.png', x=0, y=0, w=89, h=51,
              type='PNG')

    # backside
    pdf.add_page()
    pdf.image('/usr/static/img/people/back.png', x=0, y=0, w=89, h=51,
              type='PNG')

    # first name
    pdf.set_font('arial', size=14.2)
    pdf.text(x=14, y=20.5, txt=account.user.first_name)

    # last name
    pdf.set_font('arial', size=14.2)
    pdf.text(x=14, y=29, txt=account.user.last_name)

    # code
    pdf.set_font('arial', size=6)
    if (account.is_member):
        pdf.text(x=14, y=42.5, txt=account.member_code.urn[9:])
    else:
        pdf.text(x=14, y=42.5, txt='c61cb43a-00ed-4f8b-bb2c-4cb4438822ec')

    if (request.user.account.is_member):
        img = qrcode.make(account.member_code)
    else:
        img = qrcode.make('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    imgBytes = BytesIO()
    img.save(imgBytes)
    with NamedTemporaryFile() as qr:

        qr.write(imgBytes.getvalue())
        # qr code
        qr.seek(0)
        pdf.image(qr.name, x=60, y=18, w=27, type='PNG')

        b = bytes(pdf.output(dest='S'), 'latin')
        with TemporaryFile() as card:
            card.write(b)
            card.seek(0)
            return HttpResponse(card, content_type='application/pdf')


def QRcode(request):
    if (not request.user.is_authenticated):
        return redirect('people:login')
    if (request.user.account.is_member):
        img = qrcode.make(request.user.account.member_code)
    else:
        img = qrcode.make('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    imgBytes = BytesIO()
    img.save(imgBytes)
    with TemporaryFile() as qr:

        qr.write(imgBytes.getvalue())
        qr.seek(0)
        return HttpResponse(qr, content_type='image/png')
