import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from . import forms

# Create your views here.
from django.views.generic import CreateView

from CivicConnect.forms import UserForm, ProfileForm, TemplateForm #RepresentativeToSendForm #, CreateProfile
from CivicConnect.models import Profile, TemplateSubmission


def home(request):
    return render(request, 'CivicConnect/home.html')


def index(request):
    return render(request, 'CivicConnect/index.html')

def about(request):
    return render(request, 'CivicConnect/about.html')


def logout_request(request):
    '''if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()'''
    logout(request)
    return redirect("CivicConnect:home")


@login_required
def profile(request):
    return render(request, 'CivicConnect/profile.html', {'interests': request.user.profile.interests.all(),
                                                         })


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
            return redirect('CivicConnect:profile')
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
                            "levels": "administrativeArea1",  # Sample level of government
                            }
    querystring_local = {"key": settings.GOOGLE_CIVIC_API_KEY,  # API key I setup in the Google Developer's Console
                              "address": request.user.profile.address,
                              "includeOffices": "true",  # Includes offices in addition to officials, can set false
                              "levels": "administrativeArea2",  # Sample level of government
                              }

    country_reps = requests.request("GET", endpoint, params=querystring_country).json()
    regional_reps = requests.request("GET", endpoint, params=querystring_regional).json()
    local_reps = requests.request("GET", endpoint, params=querystring_local).json()

    valid_address = True
    if ("error" in country_reps):
        valid_address = False

    return render(request, 'CivicConnect/representatives.html', {'country_representatives': country_reps,
                                                                 'regional_representatives': regional_reps,
                                                                 'local_representatives': local_reps,
                                                                 'valid_address': valid_address})


@login_required
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
        photo = request.POST.get('photo')
    return render(request, 'CivicConnect/contactrepresentative.html', {'name': name,
                                                                       'office': office,
                                                                       'address': address,
                                                                       'city': city,
                                                                       'state': state,
                                                                       'zip': zip,
                                                                       'phone': phone,
                                                                       'url': url,
                                                                       'email': email,
                                                                       'photo': photo})


@login_required
def templatesubmission(request):
    if request.method == 'POST':
        template_form = TemplateForm(request.POST, user=request.user.profile)
        if template_form.is_valid():
            template_form.save()
            return redirect('CivicConnect:templates')
    else:
        # Don't forget to add user argument
        template_form = TemplateForm(user=request.user.profile)
    return render(request, 'CivicConnect/templatesubmission.html', {
        'template_form': template_form,
    })


@login_required
def templates(request):
       #temps = TemplateSubmission.objects.all()
       temps = TemplateSubmission.objects.filter(approved=True).order_by('date_posted').reverse()
       search_text = "No Search Currently - All Displayed"
       if request.GET.get('search'):
           search_text = request.GET.get('search')
           temps = temps.filter(    Q(topic__icontains=search_text) |
                                    Q(template__icontains=search_text) |
                                    Q(associated_interests__description__icontains=search_text))

       return render(request, 'CivicConnect/templates.html', {'template': temps,
                                                              'search_text': search_text})

@login_required
def mytemplates(request):
    temps = TemplateSubmission.objects.filter(author=request.user.profile).order_by('date_posted').reverse()
    return render(request, 'CivicConnect/mytemplates.html', {'template': temps,
                                                             })
'''
@login_required
def update_template(request):
    if request.method == 'POST':
        template_to_edit_id = request.POST.get('template_to_edit')
        template_to_edit = TemplateSubmission.objects.get(pk=template_to_edit_id)
        template_form = TemplateForm(request.POST, user=request.user.profile, instance=template_to_edit)
        if template_form.is_valid():
            template_form.save()
            return redirect('CivicConnect:mytemplates')
    else:
        template_form = TemplateForm(user=request.user.profile)
    return render(request, 'CivicConnect/edit_template.html', {
        'template_form': template_form,
    })
'''
