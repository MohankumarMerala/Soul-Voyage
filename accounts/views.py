from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from . import forms
from .models import Profile
from .forms import ProfileUpdateForm


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class ProfileView(LoginRequiredMixin, DetailView):

    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Safely create profile if missing
        profile, created = Profile.objects.get_or_create(user=self.object)

        context["profile"] = profile

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile",
            kwargs={"username": self.request.user.username}
        )

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile