from django.shortcuts import render
from .models import Service
from django.utils import timezone

# Create your views here.
def services_list(request):
    services = Service.objects.filter(created__lte=timezone.now()).order_by('created')
    result = {
        "services": services
    }
    return render(request, 'services/services_list.html', result)