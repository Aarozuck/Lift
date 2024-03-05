from django.contrib import admin
from .models import Driver,Rider,Notification,RideRequest

admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Notification)
admin.site.register(RideRequest)
