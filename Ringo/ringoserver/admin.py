from django.contrib import admin
from .models import Picture, Rect, Visit, Visitor, Message, Notification

# Register your models here.

admin.site.register(Picture)
admin.site.register(Rect)
admin.site.register(Visitor)
admin.site.register(Visit)
admin.site.register(Message)
admin.site.register(Notification)