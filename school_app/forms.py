from . models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Here is the Signup or Registration form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Here is the Profile form of the user
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["profile_pic", "username", "email","status", "email","contact", "address"]


# Here is the Group form
class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = "__all__"
        exclude = ["created_by"]

# Here is the Group Member form
class StudentGroupMemberForm(forms.ModelForm):
    class Meta:
        model = StudentGroupMember
        fields = ["group"]
