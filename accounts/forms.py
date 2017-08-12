__author__ = 'OllyD'

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username2 = forms.CharField(label='Username')
    class Meta:
        model = User
        fields = ['username2', 'password']

    def clean_username2(self):
        username = self.cleaned_data.get('username2')
        if User.objects.filter(username__iexact=username).exists():
            return username
        else:
            raise forms.ValidationError(u'Username Does Not Exist')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username2')
        # formuser = User.objects.get(username__iexact=username)
        # username = formuser.username
        try:
            user = User.objects.get(username__iexact=username)
           # username = user.username
        except User.DoesNotExist:
            return password
        if password != user.password:
            raise forms.ValidationError(u'Invalid Password')
        return password




class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        lower_username = str(username).lower()
        try:
            user = User.objects.get(username=username)
            print("Try suceed")
        except User.DoesNotExist:
            if User.objects.filter(username__icontains=username).exists():
                raise forms.ValidationError("This username is taken")
            if lower_username in non_usernames:
                raise forms.ValidationError("This is not allowed to be a username")
            if " " in username:
                raise forms.ValidationError("No Spaces Allowed")
            return username
        if str(username).lower() == str(user.username).lower():
            return username
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("This username is taken")
        if lower_username in non_usernames:
            raise forms.ValidationError("This is not allowed to be a username")
        if " " in username:
            raise forms.ValidationError("No Spaces Allowed")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        try:
            user  = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return email
        if str(email).lower() == str(user.email).lower():
            return email
        if User.objects.filter(email__icontains=email).exclude().exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password', 'password2']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        isupper = False
        if len(password) < 8:
            print("too short")
            raise forms.ValidationError("Password must be atleast 8 characters")
        for letter in password:
            if letter.isupper():
                isupper = True
                break
        if not isupper:
            raise forms.ValidationError("Password must contain atleast one capital")
        return password


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password must match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        lower_username = str(username).lower()
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("This username is taken")
        if lower_username in non_usernames:
            raise forms.ValidationError("This is not allowed to be a username")
        if " " in username:
            raise forms.ValidationError("No Spaces Allowed")
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        email = str(email).lower()
        email2 = str(email2).lower()
        if email != email2:
            raise forms.ValidationError("Emails must match")
        return email2

non_usernames = ['fuck', 'bitch', 'about', 'sex', 'dick', 'pussy', 'crafters', 'faggots', 'shit', 'playlist', 'videos', 'accounts']