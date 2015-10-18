from django.conf.urls import url
from .views import *
from django.contrib.auth.views import login, logout
from webadmin import views


urlpatterns = [
    # Visits
    url(r'^$', views.index, name='index'),
    url(r'^visits/$', views.visit_list, name='visit_list'),
    url(r'^visit/(?P<visit_id>[0-9]+)/$', views.visit_detail, name='visit_detail'),

    # Visitors
    url(r'^visitors/', views.visitor_list, name='visitor_list'),
    url(r'^visitors/(?P<visitor_id>[0-9]+)/$', views.visitor_details, name='visitor_details'),
    url(r'^visitors/edit/(?P<pk>[0-9]+)/$', login_required(VisitorUpdate.as_view()), name='update_visitor'),
    url(r'^visitors/create/$', login_required(VisitorCreate.as_view()), name='create_visitor'),

    # log patterns
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),

    url(r'^contact/$', views.contact, name='contact')
]
