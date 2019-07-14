from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import UserProfile
import re


#Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix',}))
    password = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if len(username) < 1:
            raise forms.ValidationError("Enter Username!")
        else:
            if len(password) < 8:
                raise forms.ValidationError("Password is too short!")
            else:
                user = authenticate(username=username, password=password)
                if not user or not user.is_active:
                    raise forms.ValidationError("Username or Password not matched!")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user



#Registration Form
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix'}))
    email = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'email'}))
    password1 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))
    password2 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(username) < 1:
            raise forms.ValidationError("Enter username!")
        else:
            user_exist = User.objects.filter(username__iexact=username).exists()
            if user_exist:
                raise forms.ValidationError("Username already taken!")
            else:
                if len(email) < 1:
                    raise forms.ValidationError("Enter email address!")
                else:
                    email_correction = re.match('[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})', email)
                    if email_correction == None:
                        raise forms.ValidationError("Email not correct!")
                    else:
                        email_exist = User.objects.filter(email__iexact=email).exists()
                        if email_exist:
                            raise forms.ValidationError("Email already exist!")
                        else:
                            if len(password1) < 8:
                                raise forms.ValidationError("Password is too short!")
                            else:
                                if password1 != password2:
                                    raise forms.ValidationError("Password not matched!")

    def registration(self, request):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')

        user = User.objects.create_user(username=username, email=email)

        user.set_password(password1)
        return user




class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
        ]


class ChangeBasicInfo(forms.ModelForm):

    phone = forms.CharField(max_length=18, required=False)
    age = forms.IntegerField(required=False)
    permanent_address = forms.CharField(max_length=100, required=False)
    present_addres = forms.CharField(max_length=100, required=False)
    image = forms.ImageField(required=False)


    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'age',
            'permanent_address',
            'present_address',
            'image'
        ]





class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', max_length=20, required=False, widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', max_length=20, required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm Password', max_length=20, required=False, widget=forms.PasswordInput)

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
