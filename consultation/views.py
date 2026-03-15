from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ConsultationForm

@require_POST
def consultation_request(request):
    form = ConsultationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you! We will contact you shortly.'
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)