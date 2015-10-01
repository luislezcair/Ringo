import json

from rest_framework import viewsets, generics
from rest_framework.response import Response
from models import Picture, Rect, VisitorFaceSample, Visitor, Visit, Message, Notification
from serializers import PictureSerializer, RectSerializer, VisitorSerializer, VisitSerializer, MessageSerializer, \
    NotificationSerializer
from xmpp import xmppconnector
from recognition.visitor_recognizer import VisitorRecognizer


class RectViewSet(viewsets.ModelViewSet):
    queryset = Rect.objects.all()
    serializer_class = RectSerializer

    def create(self, request, **kwargs):
        serializer = RectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()

            # We receive a list of Rects with the same picture, so we just
            # take the picture from the first Rect.
            picture_obj = serializer.validated_data[0]['picture']
            image = picture_obj.picture

            # Create the Recognizer and pass all available faces
            recognizer = VisitorRecognizer(VisitorFaceSample.objects.all())
            recognizer.train_model()

            # Build an URL where the clients can download the image
            picture_url = request.build_absolute_uri(image.url)
            response_dict = {"visitors": [], "people": 0, "picture_url": picture_url}

            # Create a new visit
            visit = Visit(picture=picture_obj)
            visit.save()

            # Try to recognize people in the incoming picture
            visitors, faces = recognizer.recognize_visitor(image)

            # Add the recognized visitors to the Visit and to the JSON response
            for visitor_id, confidence in visitors:
                visitor = Visitor.objects.get(pk=visitor_id)
                visit.visitors.add(visitor)

                visitor_dict = {"name": visitor.name, "confidence": confidence}
                response_dict["visitors"].append(visitor_dict)

            # Save and send the number of people in the visit
            response_dict["people"] = visit.people = faces
            visit.save()

            # Pack the data (url and visitor data) in json
            json_response = json.dumps(response_dict)

            # Send the data to the xmpp server where the devices are listening
            xmppconnector.connect_and_send(json_response)

        # Return an empty response since we don't need to inform anything
        return Response()


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


# Visitor REST
class VisitorList(generics.ListCreateAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


class VisitorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


# Visit REST
class VisitList(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


class VisitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


# Message REST
# Is there a need for a complete list of messages?
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# Notification REST
class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

