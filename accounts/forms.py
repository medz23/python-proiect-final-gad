from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, Profile
from django import forms
from taggit.managers import TaggableManager


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','content','image']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    camps = TaggableManager(verbose_name=u'Pasta')
    class Meta:
        model = Profile
        fields = ['image','name','description']
