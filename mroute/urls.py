from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getAllMarkets/$', views.getAllMarkets, name='getAllMarkets'),  # ajax
    url(r'^SaveRoute/$', views.SaveRoute, name='SaveRoute'),  # ajax
    url(r'^news/$', views.news, name='news'),
    url(r'^addmarket/$', views.addmarket, name='addmarket'),  # form non-ajax
    url(r'^getNets/$', views.getNets, name='getNets'),  # ajax
    url(r'^getMarkets/$', views.getMarkets, name='getMarkets'),  # ajax
    url(r'^makeXlsReport/$', views.makeXlsReport, name='makeXlsReport'),  # ajax
    url(r'^makeRouteFixStart/$', views.makeRouteFixStart, name='makeRouteFixStart'),
    url(r'^makeRouteAutoStart/$', views.makeRouteAutoStart, name='makeRouteAutoStart'),
    url(r'^marketTranslit/$', views.marketTranslit, name='marketTranslit'),
]

