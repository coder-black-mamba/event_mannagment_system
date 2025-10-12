from django.db import models
from django.db.models import CASCADE, Model ,CharField,TextField ,EmailField ,ManyToManyField , DateField , TimeField , ForeignKey , DO_NOTHING ,ImageField,BooleanField
from users.models import CustomUser
# Create your models here.


# Category Model
class Category(Model):
    """CAtegory Model"""
    name = CharField(max_length=255)
    description=TextField()

    def __str__(self):
        return self.name


# event model
class Event(Model):
    """Event Model"""
    name = CharField(max_length=255)
    description = TextField()
    image_link = CharField(max_length=255)
    date = DateField()
    time = TimeField()
    location = CharField(max_length=255)
    category = ForeignKey(Category,on_delete=DO_NOTHING)
    event_img=ImageField(upload_to="event_images",blank=True,default="event_images/default.jpg")

    def __str__(self): 
        return self.name



# rsvp model
class RSVP(Model):
    event = ForeignKey(Event,on_delete=CASCADE)
    participant = ForeignKey(CustomUser,on_delete=CASCADE)
    rsvp = BooleanField(default=False)

    def __str__(self):
        return self.event.name



# later cleanup
# Participant Evenets
class Participant(Model):
    """Participant Model"""
    name = CharField(max_length=255)
    email = EmailField(unique=True)
    events = ManyToManyField(Event,related_name="participant")


    def __str__(self):
        return self.name



