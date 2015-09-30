from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from ringoserver.views import RectViewSet, PictureViewSet
from rest_framework.routers import DefaultRouter
import settings


router = DefaultRouter()
router.register(r'rects', RectViewSet)
router.register(r'pictures', PictureViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^doorbell/api/', include(router.urls)),
    url(r'^rest/', include('ringoserver.urls', namespace='rest')),
    url(r'webadmin/', include('webadmin.urls', namespace='webadmin')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
