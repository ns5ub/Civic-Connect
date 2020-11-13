import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy

from . import forms

# Create your views here.
from django.views.generic import CreateView

from CivicConnect.forms import UserForm, ProfileForm, RepresentativeToSendForm #, CreateProfile
from CivicConnect.models import Profile, TemplateSubmission, EmailTemplate

# For Emails
from django.core.mail import send_mail
from django.http import HttpResponse
# Emails

def home(request):
    return render(request, 'CivicConnect/home.html')


def index(request):
    return render(request, 'CivicConnect/index.html')


def profile(request):
    return render(request, 'CivicConnect/profile.html')


def logout_request(request):
    '''if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()'''
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("CivicConnect:home")


@login_required
def profile(request):
    return render(request, 'CivicConnect/profile.html')


@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'CivicConnect/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

'''
    def signup(request):
    if request.method == 'POST':
        form = CreateProfile(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('CivicConnect:home')
    else:
        form = CreateProfile()
    return render(request, 'CivicConnect/add_user.html', {'form': form})
'''


@login_required
def representatives(request):
    endpoint = 'https://www.googleapis.com/civicinfo/v2/representatives'
    querystring_country = {"key": settings.GOOGLE_CIVIC_API_KEY,  # API key I setup in the Google Developer's Console
                           "address": request.user.profile.address,
                           "includeOffices": "true",  # Includes offices in addition to officials, can set false
                           "levels": "Country",  # Sample level of government
                           }

    querystring_regional = {"key": settings.GOOGLE_CIVIC_API_KEY,  # API key I setup in the Google Developer's Console
                            "address": request.user.profile.address,
                            "includeOffices": "true",  # Includes offices in addition to officials, can set false
                            "levels": "regional",  # Sample level of government
                            }
    querystring_adminarea1 = {"key": settings.GOOGLE_CIVIC_API_KEY,  # API key I setup in the Google Developer's Console
                              "address": request.user.profile.address,
                              "includeOffices": "true",  # Includes offices in addition to officials, can set false
                              "levels": "administrativeArea1",  # Sample level of government
                              }

    country_reps = requests.request("GET", endpoint, params=querystring_country).json()
    regional_reps = requests.request("GET", endpoint, params=querystring_regional).json()
    adminarea_reps = requests.request("GET", endpoint, params=querystring_adminarea1).json()

    return render(request, 'CivicConnect/representatives.html', {'country_representatives': country_reps,
                                                                 'regional_representatives': regional_reps,
                                                                 'administrative_representatives': adminarea_reps})

def contactrepresentative(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        office = request.POST.get('office')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        url = request.POST.get('url')
        email = request.POST.get('email')
    return render(request, 'CivicConnect/contactrepresentative.html', {'name': name,
                                                                       'office': office,
                                                                       'address': address,
                                                                       'city': city,
                                                                       'state': state,
                                                                       'zip': zip,
                                                                       'phone': phone,
                                                                       'url': url,
                                                                       'email': email})


def templatesubmission(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        template = request.POST.get('template')
        submission_obj = TemplateSubmission(topic=topic, template=template)
        submission_obj.save()
    t = TemplateSubmission.objects.all()
    return render(request, 'CivicConnect/templatesubmission.html', {'template': t})


def templates(request):
       temps = TemplateSubmission.objects.all()
       return render(request, 'CivicConnect/templates.html', {'template': temps})



