from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    names = ['Rahim', 'Karim', 'Jabbar', 'Sattar', 'Mr. Alu']
    count = 0
    for name in names:
        count += 1
    context = {
        'names': names,
        'age': [10, 20, 30, 40, 50],
        'count': count
    }
    return render(request, "test.html", context)