from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template import loader
import panopticon.models as models
import datetime
from panopticon.forms import farmForm, changeFarmForm, employeeForm, sectorForm, incidentForm
import random
import datetime
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

pages = {"home": "", "productivity": "", "incidents": "", "final": "", "edit-site":"", "add-site":"", "change-site":""}

@login_required
def incident_report(request):
    if request.method == "GET":
        pass
    else:
        description = request.POST['description']
        reporter = request.user.CrewLead
        sector = reporter.sector
        farm = sector.farm
        employees_involved = None
        date = str(datetime.now())
        incident = models.Incident.objects.create(description=description, reporter=reporter,
                                                  sector=sector, farm=farm)
        incident.save()

@login_required
def assign_new_task(request):
    title = request.POST['title']
    desc = request.POST['description']
    assignee = request.POST['employee']

@login_required
def task_complete(request):
    pass

@login_required
def dashboard(request):
    resetPages()
    pages["home"] = "current"
    template = loader.get_template('index.html')
    soon_to_recover = []
    weather = [] # line graph
    percent_incapacitated = # pie graph
    recent_incidents =[] # list
    recently_completed = []

    context = {
        'pages': pages,
        'user': request.user,
        'farm': request.user.farmemployee.farmowner.current_farm
    }
    return HttpResponse(template.render(context, request))

@login_required
def edit_site(request):
    if request.method == "GET":
        resetPages()
        pages["edit_site"] = "current"
        template = loader.get_template("edit_site.html")
        context = {
            'user': request.user,
            'farm': request.user.farmemployee.farmowner.current_farm
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        farm = request.user.farmemployee.farmowner.current_farm
        farm.name = request.POST['name']
        farm.zip = request.POST['zip']
        farm.address = request.POST['address']
        farm.state = request.POST['state']
        farm.save()
        return dashboard(request)

@login_required
def add_site(request):
    if request.method == "GET":
        resetPages()
        pages["add_site"] = "current"
        template = loader.get_template("add_site.html")
        farmProfile = farmForm()
        context = {
            'farmProfile': farmProfile,
            'user': request.user,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        farm_form = farmForm(request.POST)
        if farm_form.is_valid():
            f = farm_form.save()
            request.user.farmemployee.farmowner.all_farms.add(f)
            request.user.farmemployee.farmowner.current_farm = f
            request.user.farmemployee.farmowner.save()
            return dashboard(request)
        else: return farm_form.errors

@login_required
def change_site(request):
    if request.method == "GET":
        template = loader.get_template("change_site.html")
        changeFarm = changeFarmForm(initial={'farm': request.user.farmemployee.farmowner.current_farm.name})
        context = {
            'changeFarm':changeFarm,
            'user': request.user
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        farm = models.Farm.objects.get(name=request.POST['farm'])
        request.user.farmemployee.farmowner.current_farm = farm
        request.user.farmemployee.farmowner.save()
        request.user.save()
        return dashboard(request)

@login_required
def employees(request):
    resetPages()
    pages["employees"] = "current"
    workers = list()
    template = loader.get_template('index.html')
    context = {
        'pages': pages,
        'employees': [e for e in models.CrewLead.objects.all()]
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_lead(request):
    resetPages()
    pages["employees"] = "current"
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        sector = request.POST['sector']
        userFarm = request.user.farmemployee.farmowner.current_farm
        newEmployee = models.FarmEmployee.objects.create(first_name=first_name, last_name=last_name, farm=userFarm)
        if request.POST['isCrewLead']:
            cl = models.CrewLead.objects.create(sector=models.Sector.objects.get(name=sector), employee=newEmployee)
            cl.save()
        newEmployee.save()
        return employees(request)
    else:
        template = loader.get_template('add_lead.html')
        employee_form = employeeForm()
        context = {
            'employeeForm': employee_form,
            'pages': pages,
        }
        return HttpResponse(template.render(context, request))

@csrf_exempt
def incident_data(request):
    if request.method == "POST":
        interval = request.POST['timespan']
        current_time = datetime.datetime.now()
        if interval == 'instant':
            return HttpResponse(json.dumps([current_time.strftime("%Y-%m-%dT%H:%M:%S"), random.randint(0,10)]))
        elif interval == 'day':
            print('wtf')
            data = list()
            today = datetime.datetime.utcnow().date()
            iter_date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
            while (iter_date < current_time):
                iter_date = iter_date + datetime.timedelta(hours=1)
                data.append([iter_date.strftime("%Y-%m-%d %H:%M:%S"), random.randint(0,10)])
            return HttpResponse(json.dumps(data))

@login_required
def productivity(request):
    resetPages()
    pages["productivity"] = "current"
    template = loader.get_template('index.html')
    context = {
        'pages': pages
    }
    return HttpResponse(template.render(context, request))


@login_required
def incidents(request):
    resetPages()
    pages["incidents"] = "current"
    template = loader.get_template('incident_management.html')
    context = {
        'pages': pages,
        'incidents': [i for i in models.Incident.objects.all()]
    }
    return HttpResponse(template.render(context, request))

def add_incident(request):
    if request.method == "GET":
        template = loader.get_template('add_incident.html')
        incident_form = incidentForm(initial={'farm': request.user.farmemployee.farmowner.current_farm.name})
        context = {
            'incidentForm': incident_form,
            'pages': pages,
        }
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        desc = request.POST['description']
        farm = models.Farm.objects.get(name=request.POST['farm'])
        employeesInvolved = request.POST.getlist('employees')
        sector = models.Sector.objects.get(name=request.POST['sector'])
        i = models.Incident.objects.create(description=desc, farm=farm, sector=sector)
        for li in employeesInvolved:
            i.employees_involved.add(li)
        i.save()
        return incidents(request)

@login_required
def sectors(request):
    resetPages()
    pages['sectors'] = "current"
    template = loader.get_template('zoning_management.html')
    context = {
        'pages':pages,
        'sectors': [s for s in models.Sector.objects.all()]
    }
    return HttpResponse(template.render(context, request))

def add_sector(request):
    if request.method == "POST":
        name = request.POST['name']
        farm = models.Farm.objects.get(name=request.POST['farm'])
        newSector = models.Sector.objects.create(name=name, farm=farm)
        overseer = request.POST.getlist('overseer')
        newSector.save()
        return sectors(request)
    else:
        template = loader.get_template('add_sector.html')
        sector_form = sectorForm(initial={'farm': request.user.farmemployee.farmowner.current_farm.name})
        context = {
            'sectorForm': sector_form,
            'pages': pages,
        }
        return HttpResponse(template.render(context, request))


def create_user(request):
    if request.method == "GET":
        return render(request, "create_user.html")
    else:
        if 'new_user' in request.POST:
            username = request.POST['new_user']
            password = request.POST['new_pass']
            email = request.POST['new_email']
            first = request.POST['new_first']
            last = request.POST['new_last']
            farm = request.POST['new_farm']
            newuser = User.objects.create_user(username=username, email=email, password=password,
                                               first_name=first, last_name=last)
            newuser.set_password(password)
            newfarm = models.Farm.objects.create(name=farm)
            newfarm.save()
            newemployee = models.FarmEmployee.objects.create(user=newuser, farm=newfarm)
            newemployee.save()
            newowner = models.FarmOwner.objects.create(employee=newemployee, current_farm=newfarm)
            newowner.all_farms.add(newfarm)
            newowner.save()
            newuser.save()
            newuser = authenticate(username=username,
                                    password=password,)
            login(request, newuser)
            template = loader.get_template("edit_site.html")
            context = {
                'user': request.user,
                'farm': request.user.farmemployee.farmowner.current_farm
            }
            return HttpResponse(template.render(context, request))
        elif 'username' in request.POST:
            context = RequestContext(request)
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return dashboard(request)
                    else:
                        return HttpResponse("Your account is disabled.")
                else:
                    print("Invalid login details: {0}, {1}".format(username, password))
                    return "Invalid login details: {0}, {1}".format(username, password)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def resetPages():
    for page in pages:
        pages[page] = ""