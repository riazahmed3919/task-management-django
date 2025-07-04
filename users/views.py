from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomResgistrationForm


# Create your views here.
def sign_up(request):
    form = CustomResgistrationForm()

    if request.method == 'POST':
        form = CustomResgistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed successfully!")
    
    return render(request, "registration/register.html", {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if username is not None:
            login(request, user)
            return redirect('home')

    return render(request, "registration/sign_in.html")

def sign_out(request):
    if request.method == 'POST':
        logout(request)

        return redirect('sign-in')