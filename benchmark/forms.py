from django import forms
from django.contrib.auth.models import User

from benchmark.models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'dataset',
            'name',
            'description',
            'authors',
            'code_link',
            'paper_link',
            'result',
            'public'
        ]

class UserRegistrationForm(forms.Form):
    required_css_class = 'form-group'
    attribute = {
        'class': 'form-control',
        'placeholder': 'Enter Email'}
    email = forms.EmailField(
        required = True,
        max_length = 32,
        widget = forms.TextInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter Username'
    username = forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.TextInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter Password'
    password = forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.PasswordInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Confirm your password'
    confirm_password =forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.PasswordInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter First name'
    first_name = forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.TextInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter Last name'
    last_name = forms.CharField(
        required = True,
        max_length = 32,
        widget = forms.TextInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter Affiliation Name (if applicable)'
    affiliation_name = forms.CharField(
        required = False,
        max_length = 64,
        widget = forms.TextInput(attrs=attribute)
    )
    attribute['placeholder'] = 'Enter the DOB'
    attribute['class'] = 'form-control datepicker'
    dob = forms.DateField(
        required = False,
        label = 'Birth date (mm/dd/YYYY)',
        widget = forms.DateInput(attrs=attribute)
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already Exists. Please login')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already Exists. Choose different username')
        return username

    def clean_password(self):
        """
        TODO:
        Password should be atleast 6 character and no spaces.
        """
        return self.cleaned_data['password']

    def clean_confirm_password(self):
        p = self.cleaned_data['password']
        cp = self.cleaned_data['confirm_password']
        if p != cp:
            raise forms.ValidationError('Passwords do not match')
        return cp

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name = first_name.strip().split(' ')
        if len(first_name) > 1:
            raise forms.ValidationError('First Name should not have any spaces')
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name = last_name.strip().split(' ')
        if len(last_name) > 1:
            raise forms.ValidationError('Last Name should not have any spaces')
        return self.cleaned_data['last_name']

    def clean_affiliation_name(self):
        """
        This clean method sets the default value for affiliation to ''
        """
        return self.cleaned_data['affiliation_name'] or ''

    def clean_dob(self):
        return self.cleaned_data['dob']
