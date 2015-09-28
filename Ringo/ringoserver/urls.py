from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ringoserver import views

urlpatterns = [
    url(r'^visitor/(?P<pk>[0-9]+)/$', views.VisitorDetail.as_view()),
    url(r'^visitor/$', views.VisitorList.as_view()),
    url(r'^visit/(?P<pk>[0-9]+)/$', views.VisitDetail.as_view()),
    url(r'^visit/$', views.VisitList.as_view()),
    url(r'^message/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view()),
    url(r'^message/$', views.MessageList.as_view()),
    url(r'^notification/(?P<pk>[0-9]+)/$', views.NotificationDetail.as_view()),
    url(r'^notification/$', views.NotificationList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)