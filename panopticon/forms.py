from django import forms
from panopticon.models import CustomField, CustomFieldEntry
from panopticon.models import Sector, FIELD_CHOICES, TIME_CHOICES
from panopticon.models import Farm
from panopticon.models import CrewLead, FarmEmployee

class sectorForm(forms.ModelForm):
    farm = forms.ChoiceField([(f, f) for f in Farm.objects.all()])
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Datatype name'}))
    overseer = forms.ChoiceField([(l,l) for l in CrewLead.objects.all()])
    class Meta:
        model = Sector
        fields = ("name", "farm")

class employeeForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name (required)'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lasr Name'}), required=False)
    farm = forms.ChoiceField([(f, f) for f in Farm.objects.all()])
    isCrewLead = forms.BooleanField(required=True)
    class Meta:
        model = FarmEmployee
        fields = ('first_name', 'last_name', 'farm', 'isCrewLead')


class qualificationsForm(forms.ModelForm):
    qualificationName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name (required)'}), required=True)

class CustomFieldForm(forms.ModelForm):
    sector = forms.ChoiceField(choices=[(s.name, s.name) for s in Sector.objects.all()],
                                widget=forms.RadioSelect(), required=True)
    label = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Field Name'}), required=True)
    field_type = forms.CharField(choices=[(s, s) for s in FIELD_CHOICES], widget=forms.RadioSelect(),
                                 required=True)
    required_from_lead = forms.BooleanField(required=True)
    required_frequency = forms.ChoiceField(choices=[(s, s) for s in TIME_CHOICES])