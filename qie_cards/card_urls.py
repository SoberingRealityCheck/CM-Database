from django.urls import path, re_path
from django.views.static import serve
from django.views.generic import RedirectView

from . import card_views as views
from card_db.settings import MEDIA_ROOT

app_name = 'cards'

urlpatterns = [
    #url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    path('', RedirectView.as_view(url='catalog')),
    path('catalog', views.catalog, name='catalog'),
    path('summary', views.summary, name='summary'),
    path('testers', views.TestersView.as_view(), name='testers'),
    path('stats', views.stats, name='stats'),
    path('test-details', views.TestDetailsView.as_view(), name='test-details'),
    re_path(r'^uid/(?P<card>[a-fA-F0-9]{8,16})/$', views.detail, name='detail-uid'),
    re_path(r'^uid/(?P<card>[a-fA-F0-9]{8,16})/calibration$', views.calibration, name='calibration-uid'),
    re_path(r'^uid/(?P<card>[a-fA-F0-9]{8,16})/calibration/(?P<group>[0-9]{1,2})/plots$', views.calPlots, name='plotview-uid'),
    re_path(r'^uid/(?P<card>[a-fA-F0-9]{8,16})/calibration/(?P<group>[0-9]{1,2})/results$', views.calResults, name='results-uid'),
    re_path(r'^uid/(?P<card>[a-fA-F0-9]{8,16})/(?P<test>.*)$', views.testDetail, name='testDetail-uid'),
    re_path(r'^(?P<card>[0-9]{3,7})/$', views.detail, name='detail'),
    re_path(r'^(?P<card>[0-9]{3,7})/calibration$', views.calibration, name='calibration'),
    re_path(r'^(?P<card>[0-9]{3,7})/calibration/(?P<group>[0-9]{1,2})/plots$', views.calPlots, name='plotview'),
    re_path(r'^(?P<card>[0-9]{3,7})/calibration/(?P<group>[0-9]{1,2})/results$', views.calResults, name='results'),
    re_path(r'^(?P<card>[0-9]{3,7})/(?P<test>.*)$', views.testDetail, name='testDetail'),
    path('error', views.error, name='error'),
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root':MEDIA_ROOT,'show_indexes':True}),
    path('plots', views.PlotView.as_view(), name='plots'),
    path('field', views.fieldView, name='fieldView'),
]
