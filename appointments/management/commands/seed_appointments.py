
from django.core.management.base import BaseCommand
from appointments.models import Therapist, TimeSlot
import datetime

THERAPISTS = [
    {"name":"Dr. Ananya Sharma","slug":"dr-ananya-sharma","speciality":"Anxiety, Trauma & Sleep Disorders","bio":"Dr. Ananya has 14 years of clinical hypnotherapy experience specialising in anxiety, PTSD and sleep restoration. She combines traditional hypnosis with mindfulness and somatic techniques for lasting transformation.","experience":14},
    {"name":"Dr. Vikram Nair","slug":"dr-vikram-nair","speciality":"Smoking Cessation & Weight Loss","bio":"Dr. Vikram is a certified clinical hypnotherapist with a background in behavioural psychology. He has helped over 600 clients quit smoking and transform their relationship with food using subconscious reprogramming.","experience":10},
    {"name":"Dr. Priya Menon","slug":"dr-priya-menon","speciality":"Confidence, Relationships & Life Coaching","bio":"Dr. Priya blends hypnotherapy with NLP and inner child healing to help clients break through self-limiting beliefs. Her sessions are warm, deeply intuitive, and tailored to each individual soul.","experience":8},
]

def generate_slots(therapist, days_ahead=30):
    slots = []
    today = datetime.date.today()
    times = [
        (datetime.time(9,0),  datetime.time(10,0)),
        (datetime.time(11,0), datetime.time(12,0)),
        (datetime.time(14,0), datetime.time(15,0)),
        (datetime.time(16,0), datetime.time(17,0)),
    ]
    for i in range(1, days_ahead):
        d = today + datetime.timedelta(days=i)
        if d.weekday() in (5, 6):  # skip weekends
            continue
        for start, end in times:
            if not TimeSlot.objects.filter(therapist=therapist, date=d, start_time=start).exists():
                slots.append(TimeSlot(therapist=therapist, date=d, start_time=start, end_time=end))
    TimeSlot.objects.bulk_create(slots)
    return len(slots)

class Command(BaseCommand):
    help = "Seed therapists and time slots"

    def handle(self, *args, **kwargs):
        for data in THERAPISTS:
            t, created = Therapist.objects.get_or_create(slug=data["slug"], defaults=data)
            if not created:
                for k,v in data.items():
                    setattr(t, k, v)
                t.save()
            n = generate_slots(t)
            self.stdout.write(f"  {t.name}: {n} slots created")
        self.stdout.write(self.style.SUCCESS("Done! Therapists and slots seeded."))
