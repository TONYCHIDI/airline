from django.db import models
from django.db.models import Max

# Create your models here.
class Airport(models.Model):
    Code = models.CharField(max_length=4)
    City = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.City} ({self.Code})"
    

class Flight(models.Model):
    Origin = models.ForeignKey(Airport, related_name="departures", on_delete=models.CASCADE, null=True, blank=True)
    Destination = models.ForeignKey(Airport, related_name="arrivals", on_delete=models.CASCADE, null=True, blank=True)
    Duration = models.IntegerField()
    
    def __str__(self):
        return f"{self.id}: {self.Origin} to {self.Destination} @ {self.Duration}"
    
    def is_valid_flight(self):
        return self.Origin != self.Destination or self.Duration >= 1
    
    
class People(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"
    
    
class Passenger(models.Model):
    people = models.ForeignKey(People, related_name="person", on_delete=models.CASCADE, null=True, blank=True)
    flights = models.ManyToManyField(Flight, related_name="passengers", null=True, blank=True)
    
    def __str__(self):
        return f"{self.people}"



   
    