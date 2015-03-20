from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from ringoserver.views import *
from webadmin.views import HomePageView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'rects', RectViewSet)
router.register(r'pictures', PictureViewSet)

urlpatterns = [
    url(r'^$', HomePageView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
