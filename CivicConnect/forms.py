from django import forms
from django.contrib.auth.models import  User
from CivicConnect.models import Profile



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'address')

## interests for users to choose from ##
interests = ["Cybersecurity", "Police Brutality"]
class CreateProfile(forms.ModelForm) :

    """ Password creation and validation """
    password = forms.CharField(widget=forms.PasswordInput)  # ask for password, special widget for a bit more security
    validate_password = forms.CharField(widget=forms.PasswordInput)  # re-enter password for authentication

    """ Interest selection """
    user_interests = forms.MultipleChoiceField(choices=interests, required=True)

    """ Date of birth """
    dob = forms.DateField(required=False)

    """ Location """
    location = forms.CharField(max_length=200, required=False)

    """ Collect relevant user metadata """
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'user_interests',
        ]
