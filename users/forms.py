from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group
import re
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(StyledFormMixin ,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass

"""
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    profile_bio = forms.CharField(required=False, widget=forms.Textarea, label='Profile Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        # Todo: Handle Error

        if self.userprofile:
            self.fields['profile_bio'].initial = self.userprofile.profile_bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save userProfile jodi thake
        if self.userprofile:
            self.userprofile.profile_bio = self.cleaned_data.get('profile_bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')

            if commit:
                self.userprofile.save()

        if commit:
            user.save()

        return user
"""

class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'profile_bio']
