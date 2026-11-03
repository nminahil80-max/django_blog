from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),

            'subject': forms.TextInput(attrs={
                'placeholder': 'Enter subject'
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message...',
                'rows': 5
            }),
        }