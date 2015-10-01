from django.db import models


class Picture(models.Model):
    """
    A Picture object represents the picture taken in each visit.
    """
    picture = models.ImageField(upload_to='photos')
    timestamp = models.DateTimeField(auto_now_add=True)


class Rect(models.Model):
    """
    A Rect saves the coordinates of a face in a picture.
    """
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()

    picture = models.ForeignKey(Picture)


class Visitor(models.Model):
    """
    Visitor class represents each visitor stored in the doorbell system
    Expetamus Dominum
    """
    name = models.CharField(max_length=200)
    welcome = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class VisitorFaceSample(models.Model):
    """
    VisitorFaceSample represents a picture of a known visitor's face.
    """
    picture = models.ImageField(upload_to='visitor_faces')
    visitor = models.ForeignKey(Visitor)


class Visit(models.Model):
    """
    Represents a visit from a known or unknown visitor.
    """
    visitor = models.ForeignKey(Visitor, null=True, blank=True, default=None)
    date = models.DateTimeField('Date of Visit')
    picture = models.ForeignKey(Picture, null=True, blank=True, default=None)
    people = models.IntegerField(default=0)

    def __unicode__(self):
        if self.visitor is None:
            return 'Visitor unknown at ' + self.date.__str__()
        else:
            return self.visitor.__unicode__() + ' ' + self.date.__str__()


class Account(models.Model):
    """
    Account class represents the device owner's information
    """
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name + ' ' + self.surname


class Message(models.Model):
    """
    Message class represents each message delivered from a visitor to the owner
    """
    visit = models.ForeignKey(Visit)
    # audio files handling needs to be defined
    # temporally the message will be text
    message_text = models.CharField(max_length=200, default='no message')
    # Date is given by the visit
    # duration = ??
    # size = ??

    def __unicode__(self):
        return self.message_text


class Notification(models.Model):
    """
    Notification class represents a notification or message left by the owner for a visitor
    """
    visitor = models.ForeignKey(Visitor)
    # handling audio files seems not easy
    notification_text = models.CharField('Notification Message', max_length=200)
    date = models.DateTimeField('Notification Date')
    # duration = ??
    # size =  ??

    def __unicode__(self):
        return self.notification_text + ' ' + self.date.__str__()
