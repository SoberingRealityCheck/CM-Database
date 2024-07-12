from django.urls import path, re_path
from django.views.static import serve

from . import rm_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    #url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    path('catalog', views.catalog, name='catalog'),
    re_path(r'^(?P<rm>[0-9]{1,4})/$', views.detail, name='detail'),
    re_path(r'^uid/(?P<rm>[a-fA-F0-9_]{6,27})/$', views.detail, name='detail'),
    path('field', views.fieldView, name='field'),
    path('error', views.error, name='error'),
    ]
