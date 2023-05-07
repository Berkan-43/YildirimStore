from django import forms
from home.models import *
from django.forms import TextInput, FileInput, Select, EmailInput, PasswordInput, Textarea

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = (
            'name' ,
            'email',
            'subject',
            'message'
        )

        widgets = {
            'name'   : TextInput(attrs={'class':'form-control', 'placeholder':'İsim', 'id':'name', 'name': 'name'}),
            'email'   : EmailInput(attrs={'class':'form-control', 'placeholder':'E-posta', 'id':'email', 'name': 'email'}),
            'subject'   : TextInput(attrs={'class':'form-control', 'placeholder':'Konu', 'id':'subject', 'name': 'subject'}),
            'message'   : Textarea(attrs={'class':'form-control', 'placeholder':'Mesajınız..', 'id':'message', 'name': 'message'}),
        }