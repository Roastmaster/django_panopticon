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
# Create your views here.

pages = {"home": "", "productivity": "", "incidents": "", "final": ""}

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

    pass

@login_required
def task_complete(request):
    pass

@login_required
def dashboard(request):
    resetPages()
    pages["home"] = "current"
    template = loader.get_template('index.html')
    context = {
        'pages': pages,
        'user': request.user
    }
    return HttpResponse(template.render(context, request))

def productivity(request):
    resetPages()
    pages["productivity"] = "current"
    template = loader.get_template('index.html')
    context = {
        'pages': pages
    }
    return HttpResponse(template.render(context, request))

def incidents(request):
    resetPages()
    pages["incidents"] = "current"
    template = loader.get_template('index.html')
    context = {
        'pages': pages
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
            newowner = models.FarmOwner.objects.create(employee=newemployee, farm=newfarm)
            newowner.save()
            newuser.save()
            newuser = authenticate(username=username,
                                    password=password,)
            login(request, newuser)
            return render(request, "index.html")
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