#files.py
import re
from django import forms
#from django.contrib.auth.models import User
#from login.models import Registration
from django.utils.translation import ugettext_lazy as _
 
class ProfileForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, readonly = True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    firstname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("First Name"))
    lastname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("Last Name"))
    apt = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=10, render_value=True)), label=_("Apartment"))
    street = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100, render_value=True)), label=_("Street"))
    city = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("City"))
    state = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=50, render_value=True)), label=_("State"))
    zip = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=5, render_value=True)), label=_("Zip"))

    def clean_username(self):
        try:
            registration = Registration.objects.get(email__iexact=self.cleaned_data['email'])
        except Registration.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The email already exists. Please try another one."))
 
    def clean_zip(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class LoginForm(forms.Form):
 
    #username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
