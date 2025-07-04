from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from tasks.forms import StyledFormMixin

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldName in ['username', 'password1', 'password2']:
            self.fields[fieldName].help_text = None


class CustomResgistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists.")
        
        return email

    def clean_password(self):           # field error
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        if not re.search(r'[A-Z]', password):
            errors.append("Password must include at least one UPPERCASE letter (A-Z).")

        if not re.search(r'[a-z]', password):
            errors.append("Password must include at least one lowercase letter (a-z).")

        if not re.search(r'[0-9]', password):
            errors.append("Password must include at least one number (0-9).")

        if not re.search(r'[@#$%&_]', password):
            errors.append("Password must include at least one special character (@#$%&_).")

        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    def clean(self):            # non-field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password not matched.")
        
        return cleaned_data