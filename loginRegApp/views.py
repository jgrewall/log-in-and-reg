from django.shortcuts import render, HttpResponse, redirect, render
from .models import *
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages

def index(request):
    if ('userID' in request.session):
        return redirect('/dashboard')
    return render(request, "loginPage.html")
def displaydashboard(request):
    if (('userID' not in request.session)):
        return redirect('/')
    context={
        'thisUser':User.objects.get(id=request.session['userID'])
    }
    return render(request, "dashboard.html", context)

def newUser(request):
    if (request.method != "POST"):
        return redirect('/')
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        newUser = User.objects.create(firstName=request.POST['fName'],lastName=request.POST['lName'],email=request.POST['email'], password=pw_hash)

        request.session['userID']=newUser.id
        return redirect('/dashboard')

def login(request):
    if (request.method != "POST"):
        return redirect('/')
    errors=User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    #get user wrapped in array if filter(), if get() its not in
    user = User.objects.filter(email=request.POST['email'])
    #get that user in that array
    logged_user= user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['userID']=logged_user.id
        return redirect('/dashboard')
    else:
        messages.error(request, 'email or password invalid')
        return redirect('/')

#clear the session and redirect to logout
def logout(request):
    request.session.clear()
    return redirect('/')