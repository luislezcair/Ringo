from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import login, logout
import settings


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='webadmin', permanent=False), name='index'),
    url(r'^doorbell/api/', include('ringoserver.urls')),
    url(r'^webadmin/', include('webadmin.urls', namespace='webadmin')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),

    # log patterns
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
