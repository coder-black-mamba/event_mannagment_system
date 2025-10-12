from django import forms
from users.models import CustomUser
from django.forms import widgets
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm

import re
DEFAULT_CLASSES="block px-4 py-2 border border-gray-300 rounded w-full"



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':DEFAULT_CLASSES,
        'placeholder':'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':DEFAULT_CLASSES,
        'placeholder':'Confirm password'
    }))
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password','confirm_password','phone_number','profile_picture']
        widgets = {
            'username': widgets.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter username'
            }),
            'first_name': widgets.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter first name'
            }),
            'last_name': widgets.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter last name'
            }),
            'email': widgets.EmailInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter email'
            }),
            'password': widgets.PasswordInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter password'
            }),
            'confirm_password': widgets.PasswordInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Confirm password'
            }),
            'phone_number': widgets.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter phone number'
            }),
            'profile_picture': widgets.FileInput(attrs={
                'class': DEFAULT_CLASSES
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or len(first_name) < 2:
            raise forms.ValidationError("First name is required")
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or len(last_name) < 2:
            raise forms.ValidationError("Last name is required")
        return last_name


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password or len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        errors = []

        if len(confirm_password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', confirm_password):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', confirm_password):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', confirm_password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', confirm_password):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return confirm_password
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_regex = re.compile(r'^(\+8801|8801|01)[3-9]\d{8}$')
        if not phone_regex.match(phone_number):
            raise forms.ValidationError("Phone number must be In Correct Bangladeshi Format")
        
        return phone_number
    def clean_profile_picture(self):
        # profile_picture = self.cleaned_data.get('profile_picture')
        # if not profile_picture:
        #     raise forms.ValidationError("Profile picture is required")
        return self.cleaned_data.get('profile_picture')

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        return cleaned_data
   

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': DEFAULT_CLASSES,
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': DEFAULT_CLASSES,
            'placeholder': 'Enter password'
        })
    )

    
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not username or len(username) < 2:
    #         raise forms.ValidationError("Username is required")
    #     return username
    
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if not password or len(password) < 8:
    #         raise forms.ValidationError("Password must be at least 8 characters long")
    #     return password

    # def clean(self):
    #     cleaned_data = super(UserLoginForm, self).clean()
    #     return cleaned_data

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={
            'class': DEFAULT_CLASSES
        })
    )
    
class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'my-2'
        }),
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter group name'
            })
        }


# edit profile form
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': DEFAULT_CLASSES,
                'placeholder': 'Enter phone number'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': DEFAULT_CLASSES
            })
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or len(first_name) < 2:
            raise forms.ValidationError("First name is required")
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or len(last_name) < 2:
            raise forms.ValidationError("Last name is required")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_regex = re.compile(r'^(\+8801|8801|01)[3-9]\d{8}$')
        if not phone_regex.match(phone_number):
            raise forms.ValidationError("Phone number must be In Correct Bangladeshi Format")
        return phone_number



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # common style for every field
        for f in self.fields.values():
            f.widget.attrs.update({'class': DEFAULT_CLASSES})

        # field-specific placeholders
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter old password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'

class CustomPasswordResetForm( PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # common style for every field
        for f in self.fields.values():
            f.widget.attrs.update({'class': DEFAULT_CLASSES})

        # field-specific placeholders
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'

class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # common style for every field
        for f in self.fields.values():
            f.widget.attrs.update({'class': DEFAULT_CLASSES})

        # field-specific placeholders
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'