from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def home(request):
    return render(request, 'CivicConnect/home.html')

def index(request):
    return render(request, 'CivicConnect/index.html')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("CivicConnect:home")

