from django import forms
from posts import models

class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message",)
        model = models.Post
