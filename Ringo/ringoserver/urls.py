from django.conf.urls import url, include
from ringoserver.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rects', RectViewSet)
router.register(r'pictures', PictureViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
