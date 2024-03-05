from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    vehicle_choices = [
        ('bajaj', 'Bajaj'),
        ('minibus', 'Minibus'),
        ('bicycle', 'Bicycle'),
    ]
    vehicle_type = models.CharField(max_length=10, choices=vehicle_choices)
    address_choices = [
        ('mekele', 'Mekele'),
        ('adigrat', 'Adigrat'),
        ('adwa', 'Adwa'),
        ('aa', 'AA'),
    ]
    address = models.CharField(max_length=10, choices=address_choices)
    phone_number = models.CharField(max_length=15)
    license_plate = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)
    online_status = models.BooleanField(default=False)
    current_location = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class RideRequest(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    
class Notification(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    message = models.TextField()    