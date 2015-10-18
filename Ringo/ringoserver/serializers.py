from models import Picture, Rect, Visitor, Visit, Message, Notification
from rest_framework import serializers


class RectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rect


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture


class VisitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visitor


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visit


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
