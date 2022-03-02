from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name','middle_name','last_name','Profile_Pic','Cover_pic','Gender','BIO','Contact_Number','Country','Address')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text','img')

