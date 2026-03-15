from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event

def event_list(request):
    now = timezone.now()

    # Get filter values from URL params
    year  = request.GET.get('year')
    month = request.GET.get('month')

    upcoming_events  = Event.objects.filter(end_time__gte=now)
    completed_events = Event.objects.filter(end_time__lt=now)

    # Apply year filter
    if year:
        upcoming_events  = upcoming_events.filter(start_time__year=year)
        completed_events = completed_events.filter(start_time__year=year)

    # Apply month filter
    if month:
        upcoming_events  = upcoming_events.filter(start_time__month=month)
        completed_events = completed_events.filter(start_time__month=month)

    # Build year list for dropdown (all years that have events)
    all_years = Event.objects.dates('start_time', 'year', order='DESC')

    months = [
        (1,'January'),(2,'February'),(3,'March'),(4,'April'),
        (5,'May'),(6,'June'),(7,'July'),(8,'August'),
        (9,'September'),(10,'October'),(11,'November'),(12,'December')
    ]

    return render(request, 'events/event_list.html', {
        'upcoming_events':  upcoming_events,
        'completed_events': completed_events,
        'all_years':        all_years,
        'months':           months,
        'selected_year':    year,
        'selected_month':   int(month) if month else None,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})