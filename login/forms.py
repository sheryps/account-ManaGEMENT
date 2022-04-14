from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    #DO form cleanig here
    def clean_username(self):
        username = self.cleaned_data['username']
        if username in [entry.username for entry in User.objects.all()]:
            raise ValidationError('Username is not available')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email in [entry.email for entry in User.objects.all()]:
            raise ValidationError("Email not available for use")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        #check password length
        if len(password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        #check for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")

        return password


class AddUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(max_length = 30)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        #check password length
        if len(new_password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        #check for number and letters is password
        if new_password.isalpha() or new_password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")

        return new_password   
class ResetForms(forms.Form):
    email = forms.EmailField()
            
class NewPasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        #check password length
        if len(password) < 8:
            raise ValidationError("Password can't be less than 8 characters")
        #check for number and letters is password
        if password.isalpha() or password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")

        return password