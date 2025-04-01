from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your Message'}),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return message
