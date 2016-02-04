from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from ringoserver import views

router = DefaultRouter()
router.register(r'rects', views.RectViewSet)
router.register(r'pictures', views.PictureViewSet)
router.register(r'visitors', views.VisitorViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'owners', views.OwnerViewSet)
router.register(r'devices', views.DeviceViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
