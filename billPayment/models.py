
from django.db import models
from user.models import User
# Create your models here.


class NetworkType(models.Model):
    network = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=6)
    image_url = models.TextField()



    def __str__(self):
        return f"{self.network} with id {self.unique_id} "


class DataBundle(models.Model):
    networkType = models.ForeignKey("NetworkType", on_delete=models.CASCADE)
    dataplan = models.CharField(max_length=60)
    day = models.CharField(max_length=10)
    size= models.CharField(max_length=10)
    amount = models.CharField(max_length=10)
    unique_id = models.CharField(max_length=6)



    def __str__(self):
        return f"{self.networkType} with id {self.dataplan} "

class Cable(models.Model):
    cable_id = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    cableplan = models.CharField(max_length=60)
    planname = models.CharField(max_length=60)
    amount = models.CharField(max_length=6)



    def __str__(self):
        return f"{self.name} with id {self.planname} "

class Bills(models.Model):
    meter_type = models.CharField(max_length=30)
    disco = models.CharField(max_length=60)
    unique_id = models.CharField(max_length=6)




    def __str__(self):
        return f"{self.disco} with id {self.unique_id} "


class Exam(models.Model):
    amount = models.CharField(max_length=10)
    name = models.CharField(max_length=60)
    unique_id = models.CharField(max_length=6)




    def __str__(self):
        return f"{self.name} with id {self.unique_id} "