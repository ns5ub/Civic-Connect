from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from CivicConnect.models import Profile

## interests for users to choose from ##
interests = [(1, "Cybersecurity"), (2, "Police Brutality")]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    user_interests = forms.MultipleChoiceField(choices=interests, required=True)
    class Meta:
        model = Profile
        fields = ('bio', 'address')

'''
## interests for users to choose from ##
interests = [(1, "Cybersecurity"), (2, "Police Brutality")]

class CreateProfile(UserCreationForm) :

    #username = forms.CharField(max_length=25)

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

    required_css_class = "bootstrap4-req"
'''