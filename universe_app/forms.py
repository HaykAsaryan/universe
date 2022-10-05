from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from universe_app.models import Profile, Post

class CreateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    username = forms.CharField(required=True, max_length=30) 
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1','password2']

    def username_clean(self):
        username = self.cleaned_data['username']  
        new = User.objects.filter(username = username)  
        if new.count():
            raise ValidationError("User With Given Username Already Exists")

