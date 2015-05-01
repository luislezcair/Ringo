from rest_framework import generics, viewsets
from rest_framework.response import Response
from ringoserver.models import Picture, Rect
from ringoserver.serializers import PictureSerializer, RectSerializer
from xmpp import XMPPConnector
import json


class RectViewSet(viewsets.ModelViewSet):
    queryset = Rect.objects.all()
    serializer_class = RectSerializer

    def create(self, request):
        serializer = RectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # We can remove this later... We don't really need to save this
            serializer.save()

            # We receive a list of Rects with the same picture, so we just
            # take the picture from the first Rect.
            picture = serializer.validated_data[0]['picture'].picture

            # TODO: run recognition here and obtain visitor data (name, etc)

            # Build an URL where the clients can download the image
            picture_url = request.build_absolute_uri(picture.url)

            # Pack the data (url and visitor data) in json
            picture_dict = {'picture_url': picture_url}
            picture_json = json.dumps(picture_dict)

            # Send the data to the xmpp server where the devices are listening
            xmpp = XMPPConnector.xmpp
            xmpp.send_muc_message(picture_json)

        # Return an empty response since we don't need to inform anything
        return Response()


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

