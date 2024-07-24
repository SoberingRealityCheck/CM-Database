from django.urls import path, re_path
from django.views.static import serve

from . import cu_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    path('catalog', views.catalog, name='catalog'),
    re_path(r'^(?P<cu>[0-9]{1,3})/$', views.detail, name='detail'),
    re_path(r'^uid/(?P<cu>[a-fA-F0-9_]{4,6})/$', views.detail, name='detail'),
    path('field', views.fieldView, name='field'),
    path('error', views.error, name='error'),
    ]
