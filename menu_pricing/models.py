from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    distance = models.FloatField()
    rating = models.FloatField()

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
