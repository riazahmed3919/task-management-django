from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the <strong>task management</strong> system!")

def contact(request):
    return HttpResponse("This is <span style='color: red'><strong>contact</strong></span> page!")

def show_task(request):
    return HttpResponse("This is our <span style='color: red'>task</span> page!")