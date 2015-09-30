from django.db import models


class Picture(models.Model):
    picture = models.ImageField(upload_to='photos')
    timestamp = models.DateTimeField(auto_now_add=True)


class Rect(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()

    picture = models.ForeignKey(Picture)


class Visitor(models.Model):
    # Visitor class represents each visitor stored in the doorbell system
    # Expetamus Dominum
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, default='Sin Apellido')
    welcome = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name + ' ' + self.surname


class VisitorFaceSample(models.Model):
    picture = models.ImageField(upload_to='visitor_faces')
    visitor = models.ForeignKey(Visitor)

class Account(models.Model):
    # Account class represents the device owner's information
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name + ' ' + self.surname


class Visit(models.Model):
    # Is it mandatory for a visit to have a visitor? what if the visitor is unknown?
    visitor = models.ForeignKey(Visitor, null=True, blank=True, default=None)
    date = models.DateTimeField('Date of Visit')
    # visit should store the picture taken from the visitor?

    def __unicode__(self):
        return self.visitor.__unicode__() + ' ' + self.date.__str__()


class Message(models.Model):
    # Message class represents each message delivered from a visitor to the owner
    # visitor = models.ForeignKey(Visitor) --> not necessary because the visitor is given with the visit
    visit = models.ForeignKey(Visit)
    # audio files handling needs to be defined
    # temporally the message will be text
    message_text = models.CharField(max_length=200, default='no message')
    # Date is given by the visit
    # date = models.DateTimeField('Message Date')
    # duration = ??
    # size = ??

    def __unicode__(self):
        return self.message_text


class Notification(models.Model):
    # Notification class represents a notification or message left by the owner for a visitor
    visitor = models.ForeignKey(Visitor)
    # handling audio files seems not easy
    notification_text = models.CharField('Notification Message', max_length=200)
    date = models.DateTimeField('Notification Date')
    # duration = ??
    # size =  ??

    def __unicode__(self):
        return self.notification_text + ' ' + self.date.__str__()
