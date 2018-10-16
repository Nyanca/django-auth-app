from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    ''' form to login users '''
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.Form):
    
    username = forms.CharField(label='Enter Username', 
        min_length=4, max_length=150)
    email = forms.CharField(label='Enter email')
    password =  forms.CharField(
        label='Password', 
        widget=forms.PasswordInput)
    passwordConf = forms.CharField(
        label='Password Confirmation', 
        widget=forms.PasswordInput)
        
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r  = User.objects.filter(email=email)
        if r.count():
            raise ValidationError('This email already exists')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('This username already exists. Choose a unique username')
        return username
    
    def clean_passwordConf(self):
        password = self.cleaned_data.get('password')
        passwordConf = self.cleaned_data.get('passwordConf')
        
        if not password and not passwordConf:
            raise ValidationError('Please confirm your password')
        
        if password and passwordConf and password != passwordConf:
            raise ValidationError("Passwords don\'t match")
        return passwordConf
            
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
            )
        return user
        
    
        