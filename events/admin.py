from django.contrib import admin

# Register your models here.
from .models import Event,Participant,Category
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Category)
