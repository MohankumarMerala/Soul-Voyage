from django.db import models

CATEGORY_CHOICES = [
    ("anxiety","Anxiety & Stress Relief"),
    ("smoking","Smoking Cessation"),
    ("weight","Weight Loss Hypnosis"),
    ("sleep","Sleep Improvement"),
    ("confidence","Confidence Building"),
    ("trauma","Trauma Healing"),
]

class Service(models.Model):
    title          = models.CharField(max_length=150)
    slug           = models.SlugField(unique=True)
    category       = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    icon           = models.CharField(max_length=50, default="fa-heart")
    color          = models.CharField(max_length=20, default="#7c6af7")
    tagline        = models.CharField(max_length=200)
    problem        = models.TextField()
    process        = models.TextField()
    outcomes       = models.TextField()
    duration       = models.CharField(max_length=100)
    sessions_count = models.PositiveIntegerField(default=6)
    price          = models.DecimalField(max_digits=8, decimal_places=2, default=2500.00)
    is_featured    = models.BooleanField(default=False)
    order          = models.PositiveIntegerField(default=0)

    class Meta: ordering = ["order","title"]
    def __str__(self): return self.title
    def outcomes_list(self): return [o.strip() for o in self.outcomes.split("\n") if o.strip()]
