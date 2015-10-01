from django.conf.urls import url
from .views import *
from django.contrib.auth.views import login, logout
from webadmin import views


urlpatterns = [
    # This patterns are tested in order!!!
    url(r'^$', views.index, name='index'),
    url(r'^visit_record/', views.visit_record, name='visit_record'),
    url(r'^visitors/(?P<visitor_id>[0-9]+)/$', views.visitor_details, name='visitor_details'),
    url(r'^visitors/', views.visitors_management, name='visitor_management'),
    url(r'^(?P<visit_id>[0-9]+)/$', views.visit_detail, name='visit_detail'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^editvisitor/(?P<pk>[0-9]+)/$', login_required(VisitorUpdate.as_view()), name='update_visitor'),
    url(r'^createvisitor/$', login_required(VisitorCreate.as_view()), name='create_visitor'),
    # log patterns
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
]
