from django import forms
from .models import Appointment, Therapist, TimeSlot
import datetime


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = ["therapist", "session_type", "slot", "notes"]

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Any specific concerns..."
                }
            )
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # active therapists only
        self.fields["therapist"].queryset = Therapist.objects.filter(
            is_active=True
        )

        # only future + available slots
        self.fields["slot"].queryset = TimeSlot.objects.filter(
            is_booked=False,
            date__gte=datetime.date.today()
        ).select_related("therapist")


        self.fields["slot"].label_from_instance = lambda obj: (
            f"{obj.therapist.name} - "
            f"{obj.date.strftime('%d %b %Y')} "
            f"{obj.start_time.strftime('%I:%M %p')}"
        )


        # add CSS class
        for field in self.fields.values():

            field.widget.attrs["class"] = "sv-form-input"


    def clean_slot(self):

        slot = self.cleaned_data.get("slot")

        if slot.is_booked:

            raise forms.ValidationError(
                "This time slot has already been booked."
            )

        return slot