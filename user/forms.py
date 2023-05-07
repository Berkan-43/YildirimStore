from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.models import User
from user.models import UserProfile
from django.forms import TextInput, FileInput, Select, EmailInput, PasswordInput, CheckboxInput
from django.contrib.auth import get_user_model
from user.models import AddressModel
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from allauth.account.forms import LoginForm, AddEmailForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm, SetPasswordForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'password1', 'password2'
        ]
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            self.fields["username"].widget = forms.TextInput(
                attrs={"placeholder": "Kullanıcı Adı Giriniz", "class": "form-control form-control-lg"})
            self.fields["email"].widget = forms.EmailInput(
                attrs={"placeholder": "Email Adresi Giriniz", "class": "form-control form-control-lg ",'id':'register-email'})
            self.fields["password1"].widget = forms.PasswordInput(
                attrs={"placeholder": "Parola Giriniz", "class": "form-control form-control-lg password-box", 'id':'password'})
            self.fields["password2"].widget = forms.PasswordInput(
                attrs={"placeholder": "Parolayı Tekrar Giriniz", "class": "form-control form-control-lg password-box", 'id':'password2'})
            

class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control mb-2 form-control-lg', 'placeholder': 'Kullanıcı Adı veya E-posta Adresinizi Giriniz', 'id':'singin-email'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2 form-control-lg input','placeholder': 'Parolanızı Giriniz','id': 'singin-password',})
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'custom-control-input', 'id': 'signin-remember'})


class EmailAddForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(EmailAddForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget = forms.EmailInput(
                attrs={"placeholder": "Email Adresi Giriniz", "class": "form-control",})
        

class PasswordChange(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChange, self).__init__(*args, **kwargs)

        self.fields["oldpassword"].widget = forms.PasswordInput(
                attrs={"placeholder": "Mevcut Parolanızı Giriniz", "class": "form-control form-control-lg password-box", 'id':'passwordField'})
        self.fields["password1"].widget = forms.PasswordInput(
                attrs={"placeholder": "Yeni Parolanızı Giriniz", "class": "form-control form-control-lg password-box", 'id':'passwordField1'})
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Parolayı Tekrar Giriniz", "class": "form-control form-control-lg password-box", 'id':'passwordField2'})
        

class PasswordCReset(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordCReset, self).__init__(*args, **kwargs)

        self.fields["email"].widget = forms.EmailInput(
                attrs={"placeholder": "Email Adresi Giriniz", "class": "form-control form-control-lg",})


class PasswordResetKey(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetKey, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Yeni Parola', 'id':'password4'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Yeni Parola Tekrarı', 'id':'password5'}
        )


class PasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Yeni Parola', 'id':'password5'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Yeni Parola Tekrarı', 'id':'password6'}
        )

    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            for fieldname in ['username']:
                self.fields[fieldname].help_text = None
        
            self.fields["username"].widget = forms.TextInput(
                attrs={"placeholder": "Kullanıcı Adı Giriniz", "class": "form-control"})
            self.fields["email"].widget = forms.EmailInput(
                attrs={"placeholder": "Email Adresi Giriniz", "class": "form-control"})
            self.fields["first_name"].widget = forms.TextInput(
                attrs={"placeholder": "İsim Giriniz", "class": "form-control"})
            self.fields["last_name"].widget = forms.TextInput(
                attrs={"placeholder": "Soyisim Giriniz", "class": "form-control"})
            


#  Yalnızca telefon ve profil resmi güncellenir.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'phone',
            'profile_image'
        )
        widgets = {
            'phone'   : TextInput(attrs={"class": "form-control"}),
            'profile_image'   : FileInput(attrs={'class':'form-control', 'placeholder':'Profil resmi seçin'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ["addressCountry", "addressCity",  "addressTitle",  "addressText"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        self.fields["addressCountry"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ülke Giriniz", "rows": 4,
                   "style": "max-height: 150px;" "width: 100%;"})
        self.fields["addressCity"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Şehir Giriniz", "rows": 4,
                   "style": "max-height: 150px;" "width: 100%;"})
        self.fields["addressTitle"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Bölge Giriniz", "rows": 4,
                   "style": "max-height: 150px;" "width: 100%;"})
        self.fields["addressText"].widget = forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Adres İçeriğini Giriniz", "rows": 4,
                   "style": "max-height: 150px;" "width: 100%;"})
        
        


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = (
#             'phone',
#             'address',
#             'city',
#             'country',
#             'image'
#         )

#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for name, field in self.fields.items():
        
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),
#             field.widget.attrs.update({'class': 'form-control col-12'}),