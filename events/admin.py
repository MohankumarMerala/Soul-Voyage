from django.contrib import admin
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from .models import Event
from django import forms

class EventAdminForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = '__all__'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display  = ('title', 'conducted_by', 'start_time', 'notification_sent')
    list_filter   = ('notification_sent', 'start_time')
    search_fields = ('title', 'conducted_by')
    actions       = ['send_notifications']

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            self.notify_users(obj)

    def send_notifications(self, request, queryset):
        for event in queryset:
            self.notify_users(event)
        self.message_user(request, "Notifications sent successfully.")
    send_notifications.short_description = "Send notification to all users"

    def notify_users(self, obj):
        User = get_user_model()
        users = User.objects.filter(is_active=True).exclude(email='')
        emails = []
        for user in users:
            emails.append((
                f"🌟 New Event: {obj.title}",
                f"Hello {user.username},\n\n"
                f"We have a new event for you!\n\n"
                f"📌 Event   : {obj.title}\n"
                f"👤 By      : {obj.conducted_by}\n"
                f"🕐 Starts  : {obj.start_time.strftime('%d %b %Y, %I:%M %p')}\n"
                f"🕔 Ends    : {obj.end_time.strftime('%d %b %Y, %I:%M %p')}\n"
                f"🔗 Join    : {obj.meeting_link or 'Link will be shared soon'}\n\n"
                f"📝 {obj.description}\n\n"
                f"See you there!\n"
                f"— Soul Voyage Team",
                'noreply@soulavoyage.com',
                [user.email],
            ))
        if emails:
            send_mass_mail(tuple(emails), fail_silently=True)
            obj.notification_sent = True
            obj.save()