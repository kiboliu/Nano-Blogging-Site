from django import forms

from django.contrib.auth.models import User
from socialnetwork.models import *

MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput())
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            'user',
            'date',
        )

class EditProfileForm(forms.Form):
    class Meta:
        model = Profile
        exclude = (
            'user',
            'content_type',
        )
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        # if not picture:
        #     raise forms.ValidationError("You must upload a picture")
        # if not picture.content_type or not picture.content_type.startswith('image'):
        #     raise forms.ValidationError("File type is not image")
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError("File too big (max size is {0} bytes)".format(MAX_UPLOAD_SIZE))
        return picture