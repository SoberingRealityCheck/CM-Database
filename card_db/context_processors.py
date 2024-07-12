from django.conf import settings
import os

def site(request):
    return {'SITE_URL': os.path.join(settings.STATIC_URL,'..')}
