#files.py
import re
from django import forms
from profileapp.models import UserProfile
from django.contrib.auth.models import User
#from login.models import Registration
from django.utils.translation import ugettext_lazy as _
from django.db.models.lookups import IsNull
from django.http.response import HttpResponse
import os
 
class ProfileForm(forms.ModelForm):

#     username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, readonly = True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
#     email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    use_map = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=dict()), label=_("Use Map"))



    class Meta:
        model = UserProfile
#         exclude = ('user',)
        fields = ('firstname', 'lastname', 'profle', 'photopath', 'apt', 'street', 'city', 'state', 'zip', 'loc')
        
    
#     self.fields.keyOrder = ['username', 'email', 'firstname', 'lastname', 'apt', 'street', 'city', 'state','zip', 'profle']

    def __init__(self,  *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields.keyOrder = [ 'firstname', 'lastname', 'photopath', 'profle', 'use_map','apt', 'street', 'city', 'state', 'zip', 'loc']
#         self.fields['street'].queryset = User.objects.all()
#         self.fields['street'].widget.attrs['style'] = 'display:none'
#         self.fields['street'].widget.attrs['id'] = 'user_choice'
        self.fields['use_map'].widget.attrs['onclick'] = "javascript:cntrlFields(this);"
#         self.fields['use_map'].widget.attrs['value'] = 'False'

#     def getAddrs(self):
# #         if 'loc' in self.cleaned_data and 'apt' in self.cleaned_data and 'street' in self.cleaned_data and 'city' in self.cleaned_data and 'state' in self.cleaned_data and 'zip' in self.cleaned_data:
# #             if self.cleaned_data['use_map'] == 'on':
#         self.cleaned_data['apt'] = 'AA'
#         return self.cleaned_data['apt']

#     def clean_street(self):
#         if 'street' in self.cleaned_data:
#             if self.cleaned_data['street'] == "Street":
#                 raise forms.ValidationError(_("Please enter valid street"))
#         return self.cleaned_data['street']
#     
#     def clean_city(self):
#         if 'city' in self.cleaned_data:
#             if self.cleaned_data['city'] == "City":
#                 raise forms.ValidationError(_("Please enter valid city"))
#         return self.cleaned_data['city']
#     
#     def clean_state(self):
#         if 'state' in self.cleaned_data:
#             if self.cleaned_data['state'] == "State":
#                 raise forms.ValidationError(_("Please enter valid state"))
#         return self.cleaned_data['state']
#     
#     def clean_zip(self):
#         if 'zip' in self.cleaned_data:
#             if self.cleaned_data['zip'] == "Zip" or len(self.cleaned_data['zip']) != 5:
#                 raise forms.ValidationError(_("Please enter valid zip"))
#         return self.cleaned_data['zip']
 
    def clean_photopath(self):
        photopath = self.cleaned_data.get('photopath', False)
        
#                 fileType = photopath.content_type
        if self.cleaned_data['photopath']:
            ext = os.path.splitext(self.cleaned_data['photopath'].name)[1]
            if ext not in ['.jpeg', '.jpg', '.png']: #png and jpeg
                raise forms.ValidationError(_("FileType not supported: only upload jpegs and pngs."))
        return self.cleaned_data['photopath']

class UserForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.HiddenInput(attrs=dict(required=True, readOnly = True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))

#     class Meta:
#         model = User
#         fields = ('username','email')

    def save(self):
        u = User.objects.get(username=self.cleaned_data['username'])
        u.email = self.cleaned_data['email']
        u.save()
        return u

#     self.fields.keyOrder = ['username', 'email', 'firstname', 'lastname', 'apt', 'street', 'city', 'state','zip', 'profle']

#     def clean_street(self):
#         if 'street' in self.cleaned_data:
#             if self.cleaned_data['street'] == "Street":
#                 raise forms.ValidationError(_("Please enter valid street"))
#         return self.cleaned_data['street']

# class LoginForm(forms.Form):
#  
#     #username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
#     email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
#     password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
