from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Farm(models.Model):
    name = models.CharField(max_length=100)

class FarmEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    farm = models.ForeignKey(Farm)

class Sector(models.Model):
    name = models.CharField(_("Sector Name"), max_length=100)
    farm = models.ForeignKey(Farm)

class CrewLead(models.Model):
    sector = models.OneToOneField(Sector)
    employee = models.OneToOneField(FarmEmployee)

class FarmOwner(models.Model):
    employee = models.OneToOneField(FarmEmployee)
    farm = models.OneToOneField(Farm)

class Squad(models.Model):
    lead = models.OneToOneField(CrewLead)

class Incident(models.Model):
    description = models.CharField(max_length=1000, blank=False)
    employees_involved = models.ManyToManyField(FarmEmployee)
    reporter = models.ManyToManyField(CrewLead)
    sector = models.ForeignKey(Sector)
    farm = models.ForeignKey(Farm)