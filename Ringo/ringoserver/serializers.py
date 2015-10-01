from models import Picture, Rect, Visitor, Visit, Message, Notification
from rest_framework import serializers


class RectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rect


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ('id', 'name', 'welcome')


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id', 'visitors', 'date', 'picture', 'people')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'visit', 'message_text')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'visitor', 'notification_text', 'date')

