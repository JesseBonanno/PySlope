
from django.db import models
# Create your models here.

class MaterialModel(models.Model):
    unit_weight = models.FloatField(default = 20)
    friction_angle = models.FloatField(default = 35)
    cohesion = models.FloatField(default = 2)
    depth_to_bottom = models.FloatField(default = 5)
    name = models.CharField(max_length = 50, default='Fill', blank=True, null=True)
    color = models.CharField(max_length = 20, default=None, blank=True, null=True)

class UdlModel(models.Model):
    magnitude = models.FloatField(default = 0)
    offset = models.FloatField(default = 0)
    length = models.FloatField(default = 0)
    color = models.CharField(default ='red', max_length = 20, blank=True, null=True)
    dynamic_offset = models.BooleanField(default=False)

class PointLoadModel(models.Model):
    magnitude = models.FloatField(default = 0)
    offset = models.FloatField(default = 0)
    color = models.CharField(default ='blue', max_length = 20, blank=True, null=True)
    dynamic_offset = models.BooleanField(default=False)

class SlopeModel(models.Model):
    height = models.FloatField(default=1)
    angle = models.FloatField(default=45)
    length = models.FloatField(default=1)