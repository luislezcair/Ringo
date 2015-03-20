from ringoserver.models import Picture, Rect
from rest_framework import serializers


class RectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rect


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture