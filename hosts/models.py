from django.db import models
import datetime

# Create your models here.

class Host(models.Model):
    id = models.AutoField(primary_key=True)
    host_name = models.CharField(max_length=50)
    host_email = models.EmailField(blank=True, null=True)
    host_phone = models.CharField(max_length=10)
    host_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.id} : {self.host_name}"

class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    visitor_name = models.CharField(max_length=50)
    visitor_email = models.EmailField(blank=True, null=True)
    visitor_phone = models.CharField(max_length=10)
    visitor_image = models.ImageField(upload_to='images/')
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True)
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.visitor_name}"

