from django.views.generic import TemplateView
from datetime import date


class TestPage(TemplateView):
    template_name = "test.html"


class ThanksPage(TemplateView):
    template_name = "thanks.html"


class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from appointments.models import Appointment
        from services.models import Service
        from django.contrib.auth import get_user_model
        User = get_user_model()

        sessions_completed = Appointment.objects.filter(
            status='completed'
        ).count()

        happy_clients = User.objects.filter(
            appointments__status='completed'
        ).distinct().count()

        programs_available = Service.objects.count()

        founding_year = 2014
        years_experience = date.today().year - founding_year

        context.update({
            'sessions_completed': sessions_completed,
            'happy_clients':      happy_clients,
            'programs_available': programs_available,
            'years_experience':   years_experience,
        })

        return context
