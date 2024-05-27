from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Message, UserEmail
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

def academic_email_validator(value):
    """
    Validator to ensure the email address belongs to an academic domain.
    """
    allowed_domains = ['edu.umi.ac.ma', 'umi.ac.ma']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError('Only academic email addresses are allowed.')

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        academic_email_validator(email)  # Applying the custom validator
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
#         labels = {
#             'last_name': 'Nom',
#             'first_name': 'Prenom',
#         }

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})



            
# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['name', 'email', 'subject', 'body']

#     def __init__(self, *args, **kwargs):
#         super(MessageForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})


# Code for register form
# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
    
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match')
#         return cd['password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# Code for login form
class LoginForm(forms.Form):  # Use forms.Form since this is not a model form
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Custom validations
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nom', 'prenom', 'sexe', 'CNI', 'phonenumber', 'departement', 'filiere', 'profile_image',
                  'CNE', 'semestre']
        widgets = {
            'sexe': forms.Select(choices=[('male', 'Male'), ('female', 'Female')])
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class ContactForm(forms.Form):
    name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    details=forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        send_mail("some random subject","message body",settings.EMAIL_HOST_USER,[self.cleaned_data['email']],
        fail_silently=False)


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['email']
        

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     cin = forms.CharField(label='CIN', max_length=20)  # Adjust max length as needed
#     phonenumber = forms.CharField(label='Phone Number', max_length=20)  # Adjust max length as needed
#     gender = forms.CharField(label='Gender',  max_length=20)  # Assuming you have GENDER_CHOICES in your Profile model

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match')
#         return cd['password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# # Code for login form
# class LoginForm(forms.Form):  # Use forms.Form since this is not a model form
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     # Custom validations
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         return username

#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         return password
    


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['profile_image']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'email', 'username', 'password1', 'password2']
#         labels = {
#             'first_name': 'Name',
#         }

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'email', 'username',
#                   'CNI', 'departement', 'filiere', 'profile_image',
#                   'CNE', 'semestre', 'sexe']

#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})


# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['name', 'email', 'subject', 'body']

#     def __init__(self, *args, **kwargs):
#         super(MessageForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})

# # # Code for register form
# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     cin = forms.CharField(label='CIN', max_length=20)  # Adjust max length as needed
#     phonenumber = forms.CharField(label='Phone Number', max_length=20)  # Adjust max length as needed
#     gender = forms.CharField(label='Gender',  max_length=20)  # Assuming you have GENDER_CHOICES in your Profile model

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match')
#         return cd['password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# # Code for login form
# class LoginForm(forms.Form):  # Use forms.Form since this is not a model form
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     # Custom validations
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         return username

    
#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         return password


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['profile_picture']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']


