from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.urls import reverse

from .models import Appointment, Therapist, TimeSlot, SessionPrice
from .forms import AppointmentForm


class GetSessionPriceView(View):
    """Return session price via AJAX"""

    def get(self, request):

        session_type = request.GET.get("session_type")

        try:
            sp = SessionPrice.objects.get(
                session_type=session_type,
                is_active=True
            )

            return JsonResponse({
                "price": str(sp.price),
                "found": True
            })

        except SessionPrice.DoesNotExist:

            return JsonResponse({
                "price": "2500.00",
                "found": False
            })


class TherapistListView(ListView):

    model = Therapist
    template_name = "appointments/therapist_list.html"
    context_object_name = "therapists"

    def get_queryset(self):
        return Therapist.objects.filter(is_active=True)


class BookAppointmentView(LoginRequiredMixin, View):

    template_name = "appointments/book.html"

    def get_price_map(self):

        price_map = {}

        for sp in SessionPrice.objects.filter(is_active=True):
            price_map[sp.session_type] = str(sp.price)

        return price_map

    def get(self, request):

        form = AppointmentForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "price_map": self.get_price_map(),
            }
        )

    def post(self, request):

        form = AppointmentForm(request.POST)

        if not form.is_valid():

            print("FORM ERRORS:", form.errors)

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "price_map": self.get_price_map(),
                }
            )

        try:

            with transaction.atomic():

                appt = form.save(commit=False)

                appt.user = request.user

                # Lock slot row to avoid double booking
                slot = TimeSlot.objects.select_for_update().get(
                    pk=form.cleaned_data["slot"].pk
                )

                # Check if already booked
                if slot.is_booked:

                    form.add_error(
                        "slot",
                        "This slot was just booked by someone else. Please choose another."
                    )

                    return render(
                        request,
                        self.template_name,
                        {
                            "form": form,
                            "price_map": self.get_price_map(),
                        }
                    )

                # Assign slot
                appt.slot = slot

                # Fetch price
                try:

                    price = SessionPrice.objects.get(
                        session_type=appt.session_type,
                        is_active=True
                    )

                    appt.amount = price.price

                except SessionPrice.DoesNotExist:

                    appt.amount = 2500

                # Save appointment
                appt.save()

                # Mark slot booked
                slot.is_booked = True
                slot.save()

        except Exception as e:

            print("BOOKING ERROR:", e)

            messages.error(
                request,
                "Unable to book appointment. Please try again."
            )

            return redirect("appointments:book")

        # Send email confirmation
        try:

            send_mail(

                "Soul Voyage - Appointment Confirmed",

                f"""
Dear {request.user.username},

Your {appt.get_session_type_display()} session has been booked.

Therapist: {appt.therapist.name}

Date: {appt.slot.date}
Time: {appt.slot.start_time}

Fee: Rs.{appt.amount}

Thank you for choosing Soul Voyage.
""",

                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

        # ── FIXED: redirect back to book page with ?booked=1 so the
        #    success modal can trigger in book.html ──────────────────
        return redirect(f"{reverse('appointments:book')}?booked=1")


class MyAppointmentsView(LoginRequiredMixin, ListView):

    template_name = "appointments/my_appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):

        return Appointment.objects.filter(
            user=self.request.user
        ).select_related(
            "therapist",
            "slot"
        )


class CancelAppointmentView(LoginRequiredMixin, View):

    def post(self, request, pk):

        appt = get_object_or_404(
            Appointment,
            pk=pk,
            user=request.user
        )

        if appt.status == "pending":

            appt.status = "cancelled"

            appt.slot.is_booked = False
            appt.slot.save()

            appt.save()

            messages.success(
                request,
                "Appointment cancelled successfully."
            )

        return redirect("appointments:my_appointments")


class AppointmentSuccessView(TemplateView):

    template_name = "appointments/success.html"