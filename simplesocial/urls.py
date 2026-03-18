"""final_social_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views
from django.views.generic import TemplateView
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "app": "Soul Voyage"})

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('health/', health_check, name='health'),
    path('test/', views.HomePage.as_view(), name='test'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    path('admin/', admin.site.urls),

    path('accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    path('accounts/', include("django.contrib.auth.urls")),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path('posts/', include(("posts.urls", "posts"), namespace="posts")),
    path('consultation/', include('consultation.urls', namespace='consultation')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('appointments/', include(('appointments.urls','appointments'), namespace='appointments')),
path('services/', include(('services.urls','services'), namespace='services')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
