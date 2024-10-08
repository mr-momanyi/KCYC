from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile, CommentBlog, CommentArticle


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class UserEditForm(forms.ModelForm):
        class Meta:
            model = get_user_model()
            fields = ['first_name', 'last_name', 'email']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']


# sharing posts via email
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# MANAGING COMMENTS
class CommentBlogForm(forms.ModelForm):
    class Meta:
        model = CommentBlog
        fields = ['name', 'email', 'body']

class CommentArticleForm(forms.ModelForm):
    class Meta:
        model = CommentArticle
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()




    