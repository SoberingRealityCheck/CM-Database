"""card_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('cards/', include('cm_db.card_urls', namespace='cards')),
    #path('rm/', include('cm_db.rm_urls')),
    #path('cu/', include('cm_db.cu_urls')),
    #path('sipm/', include('cm_db.sipm_urls')),
    path('', RedirectView.as_view(pattern_name='cards:catalog',permanent=False)),
    re_path(r'^admin', admin.site.urls),
]

