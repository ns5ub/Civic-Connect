from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from CivicConnect.models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

## interests for users to choose from ##
interests = [(1, "Cybersecurity"), (2, "Police Brutality")]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    required_css_class = 'bootstrap4-req'
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserForm'
        self.helper.layout = Layout (
            Row (
                Column ('first_name', css_class='form-group col-md-6 mb-0'),
                Column ('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email'
        )
        self.helper.form_tag = False


class ProfileForm(forms.ModelForm):
    #user_interests = forms.MultipleChoiceField(choices=interests, required=True)
    class Meta:
        model = Profile
        fields = ('bio', 'address', 'interests')
    required_css_class = 'bootstrap4-req'
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-ProfileForm'
        self.helper.layout = Layout (
            'bio',
            'address',
            'interests'
        )
        self.helper.form_tag = False


class CreateProfile(UserCreationForm):

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
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'user_interests',
        )

    required_css_class = "bootstrap4-req"


class RepresentativeToSendForm(forms.Form):
    address = forms.CharField(max_length=200, required=False)
    city = forms.CharField(max_length=200, required=False)
    state = forms.CharField(max_length=200, required=False)
    zip = forms.CharField(max_length=200, required=False)
    phone = forms.CharField(max_length=200, required=False)
    url = forms.CharField(max_length=200, required=False)
    email = forms.CharField(max_length=200, required=False)