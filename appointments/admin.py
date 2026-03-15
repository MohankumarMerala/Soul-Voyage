
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Therapist, TimeSlot, Appointment, SessionPrice
import datetime


class TimePickerWidget(forms.TimeInput):
    input_type = "time"
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"].update({
            "style": (
                "background:#1a1a3a;color:#f0ead6;border:1px solid rgba(201,168,76,0.4);"
                "border-radius:6px;padding:6px 10px;font-size:0.9rem;min-width:130px;"
            ),
            "step": "900",
        })
        super().__init__(*args, **kwargs)


class TimeSlotAdminForm(forms.ModelForm):
    start_time = forms.TimeField(widget=TimePickerWidget())
    end_time   = forms.TimeField(widget=TimePickerWidget())
    class Meta:
        model = TimeSlot
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "style": "background:#1a1a3a;color:#f0ead6;border:1px solid rgba(201,168,76,0.4);border-radius:6px;padding:6px 10px;font-size:0.9rem;min-width:160px;",
            }),
        }


class TimeSlotInlineForm(forms.ModelForm):
    start_time = forms.TimeField(widget=TimePickerWidget())
    end_time   = forms.TimeField(widget=TimePickerWidget())
    class Meta:
        model = TimeSlot
        fields = ["date", "start_time", "end_time", "is_booked"]
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "style": "background:#1a1a3a;color:#f0ead6;border:1px solid rgba(201,168,76,0.4);border-radius:6px;padding:6px 10px;font-size:0.9rem;min-width:150px;",
            }),
        }


class TimeSlotInline(admin.TabularInline):
    model  = TimeSlot
    form   = TimeSlotInlineForm
    extra  = 4
    fields = ["date", "start_time", "end_time", "is_booked"]
    ordering = ["date", "start_time"]
    show_change_link = True
    def get_queryset(self, request):
        return super().get_queryset(request).filter(date__gte=datetime.date.today())


@admin.register(SessionPrice)
class SessionPriceAdmin(admin.ModelAdmin):
    list_display  = ["session_type_display", "price_display", "description", "is_active"]
    list_editable = ["is_active"]
    ordering      = ["session_type"]

    def session_type_display(self, obj):
        return format_html(
            '<strong style="color:#c9a84c;">{}</strong>',
            obj.get_session_type_display()
        )
    session_type_display.short_description = "Session Type"

    def price_display(self, obj):
        formatted = "Rs. {:,.0f}".format(float(obj.price))
        return format_html('<span style="color:#4ecdc4;font-size:1.05rem;font-weight:700;">{}</span>', formatted)
    price_display.short_description = "Price"


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display  = ["name", "speciality", "experience", "open_slots", "is_active"]
    list_editable = ["is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TimeSlotInline]
    fieldsets = (
        ("Basic Info", {"fields": ("name", "slug", "photo", "is_active")}),
        ("Profile",    {"fields": ("speciality", "bio", "experience")}),
    )
    class Media:
        css = {"all": ("appointments/admin_dark.css",)}

    def open_slots(self, obj):
        n = obj.slots.filter(is_booked=False, date__gte=datetime.date.today()).count()
        color = "#4ecdc4" if n > 0 else "#e74c3c"
        return format_html('<span style="color:{};font-weight:600;">{} open</span>', color, n)
    open_slots.short_description = "Available Slots"


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    form          = TimeSlotAdminForm
    list_display  = ["therapist", "date", "start_time", "end_time", "duration_display", "is_booked"]
    list_filter   = ["therapist", "is_booked"]
    list_editable = ["is_booked"]
    date_hierarchy = "date"
    ordering = ["date", "start_time"]
    class Media:
        css = {"all": ("appointments/admin_dark.css",)}

    def duration_display(self, obj):
        if obj.start_time and obj.end_time:
            s = datetime.datetime.combine(datetime.date.today(), obj.start_time)
            e = datetime.datetime.combine(datetime.date.today(), obj.end_time)
            return f"{int((e-s).total_seconds()/60)} min"
        return "-"
    duration_display.short_description = "Duration"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("therapist")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display   = ["user", "therapist", "slot_info", "session_type", "amount_display", "status", "payment_done", "created_at"]
    list_filter    = ["status", "session_type", "payment_done", "therapist"]
    list_editable  = ["status", "payment_done"]
    search_fields  = ["user__username", "user__email"]
    readonly_fields = ["created_at", "amount"]
    date_hierarchy  = "created_at"

    def slot_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><span style="color:#c9a84c;font-size:0.85em;">{}</span>',
            obj.slot.date.strftime("%d %b %Y"),
            obj.slot.start_time.strftime("%I:%M %p"),
        )
    slot_info.short_description = "Date & Time"

    def amount_display(self, obj):
        formatted = "Rs. {:,.0f}".format(float(obj.amount))
        return format_html('<span style="color:#4ecdc4;font-weight:600;">{}</span>', formatted)
    amount_display.short_description = "Amount"
