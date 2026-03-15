from django.db import models

class Event(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    conducted_by = models.CharField(max_length=100)
    start_time   = models.DateTimeField()
    end_time     = models.DateTimeField()
    image        = models.ImageField(upload_to='events/', blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)  # ADD THIS
    created_at   = models.DateTimeField(auto_now_add=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']