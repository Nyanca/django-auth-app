from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User

def index(request):
    '''return index.html file'''
    return render(request, 'index.html')

@login_required
def logout(request):
    ''' log user out '''
    auth.logout(request)
    messages.success(request, "You've been logged out.")
    return redirect(reverse('index'))

def login(request):
    ''' log user in '''
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username = request.POST['username'],
                                     password = request.POST['password'])
                                     
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in.")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Invalid username or password")
                
    else:
        login_form = UserLoginForm()
        
    return render(request, 'login.html', {"login_form": login_form})
    
def registration(request):
    ''' allows new clients to register an account '''
    
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, 'Account created successfully')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Unable to create your account at this time')
    
    else:
        registration_form = UserRegistrationForm()
       
    return render(request, "registration.html",{
        "registration_form": registration_form})

def profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile":user})