from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

FIELD_CHOICES = [
    'BOOLEAN',
    'CONTINUOUS',
    'INTEGER',
    'STRING'
]

TIME_CHOICES = [
    'DAILY',
    'WEEKLY',
    'MONTHLY',
    'QUARTERLY',
    'BIANNUALLY',
    'ANNUALLY'
]

# Create your models here.
class Farm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return self.name

class FarmEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    farm = models.ForeignKey(Farm)
    isIncapacitated = models.BooleanField(default=False)
    date_of_recovery = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return self.last_name+", "+self.first_name

class Sector(models.Model):
    name = models.CharField(_("Sector Name"), max_length=100, unique=True)
    farm = models.ForeignKey(Farm)
    num_employees = models.IntegerField(default=0)
    number_of_incidents = models.IntegerField(default=0)
    number_of_injuries = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Qualification(models.Model):
    name = models.CharField(_("Qualification"), max_length=100)
    description = models.CharField(_("Description of qualification"), max_length=300)
    def __unicode__(self):
        return self.name

class CrewLead(models.Model):
    sector = models.ForeignKey(Sector, null=True)
    employee = models.OneToOneField(FarmEmployee)
    qualifications = models.ManyToManyField(Qualification, blank=True)
    def __unicode__(self):
        return self.employee.last_name+", "+self.employee.first_name

class FarmOwner(models.Model):
    employee = models.OneToOneField(FarmEmployee)
    all_farms = models.ManyToManyField(Farm, related_name="list_of_all_farms")
    current_farm = models.ForeignKey(Farm, related_name="current", null=True)

class Squad(models.Model):
    lead = models.OneToOneField(CrewLead)

class Incident(models.Model):
    description = models.CharField(max_length=1000, blank=False)
    employees_involved = models.ManyToManyField(FarmEmployee)
    reporter = models.ManyToManyField(CrewLead)
    sector = models.ForeignKey(Sector, null=True)
    farm = models.ForeignKey(Farm)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

class Task(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=10000)
    assignee = models.ForeignKey(CrewLead)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(null=True)

class CustomField(models.Model):
    sector = models.ForeignKey(Sector)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=24, choices=[(c,c) for c in FIELD_CHOICES])
    required_from_lead = models.BooleanField(_("Required from lead?"), default=True)
    required_frequency = models.IntegerField(choices=[(t,t) for t in TIME_CHOICES], default=None)
    def __unicode__(self):
        return self.label

class CustomFieldEntry(models.Model):
    customField = models.ForeignKey(CustomField)
    value = models.CharField(max_length=9999)
    index = models.IntegerField()
    def __unicode__(self):
        return self.value

class dateIncapacitated(models.Model):
    days_left = models.IntegerField()
    employee = models.ForeignKey(FarmEmployee)

class Dashboard(models.Model):
    recent_incidents = models
    return_to_work = models.ManyToManyField(dateIncapacitated)

class Injury(models.Model):
    employee = models.ForeignKey(FarmEmployee)
    overseer = models.ForeignKey(CrewLead, null=True)
    description = models.CharField(max_length=300)
    infliction_date = models.DateTimeField(auto_now_add=True, null=True)
    recovery_date = models.DateTimeField(blank=True, null=True)
    sector = models.ForeignKey(Sector, null=True)
    farm = models.ForeignKey(Farm)
