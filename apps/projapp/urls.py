from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^login_process$', views.login_process),
    url(r'^register$', views.register),
    url(r'^register_process$', views.register_process),
    url(r'^success$', views.success),
    url(r'^create$', views.create),
    url(r'^create_process$', views.create_process),
    url(r'^shows/(?P<id>\d+)$', views.showOne),
    url(r'^shows/(?P<id>\d+)/checkout$', views.checkOut),
    url(r'^shows/checkout$', views.checkOutPage),
    url(r'^search$', views.search_titles),
    url(r'^currency$', views.currency),
]