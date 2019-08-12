from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from .models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.urls import reverse
from usrhome.models import Notice,Rent


def index(request):
        return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user= auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            # msg = Notice.objects.filter(user=request.user, delete=False)
            # due = Rent.objects.filter(user=request.user, paid=False)
            # pay = Rent.objects.filter(user=request.user, paid=True)
            # return render(request, 'profile.html', {'dues': due, 'notification': msg, 'pastpay': pay})
            return render(request, 'index.html')
        else:
            messages.info(request, 'invalid credentials')
            return HttpResponseRedirect('#login')
    else:
        return render(request, 'index.html')




def register(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['uname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        apmnt = request.POST['apmntname']
        phone = request.POST['phone']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken')
                return HttpResponseRedirect('#signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return HttpResponseRedirect('#signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=firstname,
                                                last_name=lastname, apmnt_name=apmnt, phone=phone)
                user.save()
                messages.info(request, 'Account Created')
                return HttpResponseRedirect('#login')
        else:
            messages.info(request, 'passwords not matching')
            return HttpResponseRedirect('#signup')
        # messages.info(request,'user created')
        print('user created')
        return HttpResponseRedirect('#signup')
    else:
        return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')



