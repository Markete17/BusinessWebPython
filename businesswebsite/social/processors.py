from .models import Link

def ctx_link(request):
    ctx = {}
    links = Link.objects.filter(url__isnull=False)
    for link in links:
        ctx[link.key] = link.url
    return ctx