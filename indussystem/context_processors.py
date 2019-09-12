

def global_settings(request):
    from django.conf import settings
    context = {
        'global_settings': settings,
    }
    return context
