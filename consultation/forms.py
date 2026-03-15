from django import forms
from .models import ConsultationRequest

class ConsultationForm(forms.ModelForm):
    class Meta:
        model  = ConsultationRequest
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your Full Name'
            }),
            'email':   forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Email Address'
            }),
            'phone':   forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Phone Number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Brief message (optional)'
            }),
        }