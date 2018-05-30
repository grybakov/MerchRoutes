from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'getAllMarkets/$', views.getAllMarkets, name='getAllMarkets'),  # ajax
    url(r'news/$', views.news, name='news'),
    url(r'addmarket/$', views.addmarket, name='addmarket'),  # form non-ajax
    url(r'getMarkets/$', views.getMarkets, name='getMarkets'),  # ajax
    url(r'makeXlsReport/$', views.makeXlsReport, name='makeXlsReport'),  # ajax
    url(r'makeRouteFixStart/$', views.makeRouteFixStart, name='makeRouteFixStart'),  # make route - fix start point
    url(r'makeRouteAutoStart/$', views.makeRouteAutoStart, name='makeRouteAutoStart'),  # make route - AUTO search start point
    url(r'marketTranslit/$', views.marketTranslit, name='marketTranslit'),  # translit EN --> RU
]

