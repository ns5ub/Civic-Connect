from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
from CivicConnect.forms import UserForm, ProfileForm
from CivicConnect.models import Profile


def home(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()
    return render(request, 'CivicConnect/home.html')

def index(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()
    return render(request, 'CivicConnect/index.html')

def logout_request(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("CivicConnect:home")

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
    return render(request, 'CivicConnect/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })