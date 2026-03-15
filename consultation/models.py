from django.db import models

class ConsultationRequest(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=20)
    message      = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ['-submitted_at']