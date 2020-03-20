from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, "login.html")

def register(request):
    if request.method != "POST":
        # Get requests should not be accepted at this endpoint
        return redirect("/")
    
    errors = User.objects.validate(request.POST)
    if errors:         # if we have any errors returned in the errors object
        for key, err in errors.items():
            messages.error(request, err)
        return redirect("/")

    # no errors foudn in the login data and so we should register them!
    new_user = User.objects.register(request.POST)

    #   save the user ID to the session so we can prove that they have authenticated
    #   and so we can use it easily to pull info
    request.session['id'] = new_user.id 

    return redirect("/successful_login")


def login(request):
    if request.method != "POST":
        # Get requests should not be accepted at this endpoint
        return redirect("/")

    if not User.objects.authenticate(request.POST['login_email'], request.POST['login_password']):
        messages.error(request, "Invalid login credentials")
        return redirect("/")
    
    # we have successfully logged in / verified credentials
    #   save the user ID to the session so we can prove that they have authenticated
    #   and so we can use it easily to pull info
    user = User.objects.get(email = request.POST['login_email'])
    request.session['id'] = user.id 
    return redirect("/successful_login")

def success(request):
    # verify that the user is actually authenticated
    if not 'id' in request.session:
        return redirect("/")

    # successful login or registration will redirect to where we want it
    return redirect('/wishes/')

def logout(request):
    del request.session['id']
    return redirect("/")
