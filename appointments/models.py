from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


SESSION_TYPES = [
    ("hypnotherapy", "Hypnotherapy"),
    ("anxiety", "Anxiety & Stress Relief"),
    ("smoking", "Smoking Cessation"),
    ("weight_loss", "Weight Loss Hypnosis"),
    ("sleep", "Sleep Improvement"),
    ("confidence", "Confidence Building"),
    ("trauma", "Trauma Healing"),
]


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("cancelled", "Cancelled"),
    ("completed", "Completed"),
]


class SessionPrice(models.Model):

    session_type = models.CharField(max_length=50, choices=SESSION_TYPES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=2500)
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_session_type_display()} — Rs.{self.price}"


class Therapist(models.Model):

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to="therapists/", blank=True)
    speciality = models.CharField(max_length=200)
    bio = models.TextField()
    experience = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):

    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.therapist} - {self.date} {self.start_time}"


class Appointment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    session_type = models.CharField(max_length=50, choices=SESSION_TYPES)

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_done = models.BooleanField(default=False)

    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.session_type} on {self.slot.date}"

    class Meta:
        ordering = ["-created_at"]