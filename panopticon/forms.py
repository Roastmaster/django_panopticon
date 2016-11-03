from django import forms
from panopticon.models import CustomField, CustomFieldEntry
from panopticon.models import Sector, FIELD_CHOICES, TIME_CHOICES
from panopticon.models import Farm, Incident
from panopticon.models import CrewLead, FarmEmployee

class changeFarmForm(forms.ModelForm):
    farm = forms.ChoiceField([f.name, f.name] for f in Farm.objects.all())
    class Meta:
        model = Farm
        fields = ("farm",)

class incidentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a descriprion for the incident (required)'}))
    employeesInvolved = forms.ChoiceField([e.last_name, e.last_name] for e in FarmEmployee.objects.all())
    sector = forms.ChoiceField([s.name, s.name] for s in Sector.objects.all())
    farm = forms.ChoiceField([f.name, f.name] for f in Farm.objects.all())
    class Meta:
        model = Incident
        fields = ('description', 'employeesInvolved', 'sector', 'farm')

class farmForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a name for your new farm (required)'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street address'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zip'}))
    class Meta:
        model = Farm
        fields = ("name", "address", "state", "zip")

class sectorForm(forms.ModelForm):
    farm = forms.ChoiceField([(f.name, f.name) for f in Farm.objects.all()], required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Sector name'}))
    overseer = forms.ChoiceField([(l,l) for l in CrewLead.objects.all()], required=False)
    class Meta:
        model = Sector
        fields = ("name", "farm")

class employeeForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name (required)'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=False)
    sector = forms.ChoiceField([[s.name,s.name] for s in Sector.objects.all()], required=False)
    farm = forms.ChoiceField([(f, f) for f in Farm.objects.all()], required=False)
    isCrewLead = forms.BooleanField(required=True)
    class Meta:
        model = FarmEmployee
        fields = ('first_name', 'last_name', 'farm', 'sector')


class qualificationsForm(forms.ModelForm):
    qualificationName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name (required)'}), required=True)

class CustomFieldForm(forms.ModelForm):
    sector = forms.ChoiceField([(s.name, s.name) for s in Sector.objects.all()],
                                widget=forms.RadioSelect(), required=True)
    label = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Field Name'}), required=True)
    field_type = forms.ChoiceField(choices=[(s, s) for s in FIELD_CHOICES], widget=forms.RadioSelect(),
                                 required=True)
    required_from_lead = forms.BooleanField(required=True)
    required_frequency = forms.ChoiceField([(s, s) for s in TIME_CHOICES])

    class Meta:
        model = CustomField
        fields = ('sector','label','field_type','required_from_lead','required_frequency')

