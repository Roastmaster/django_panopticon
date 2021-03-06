import panopticon.views as views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^new-user/$', views.create_user, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^productivity/', views.productivity, name="productivity"),
    url(r'^incidents/$', views.incidents, name="incidents"),
    url(r'^incidents/add_incident/$', views.add_incident, name="incidents"),
    url(r'^incidents/add_injury/$', views.add_injury, name="incidents"),
    url(r'^incident_data/injuries_per_sector/$', views.injuries_per_sector, name="incidents"),
    url(r'^edit_site/$', views.edit_site, name="edit_site"),
    url(r'^add_site/', views.add_site, name="add_site"),
    url(r'^change_site/', views.change_site, name="change_site"),
    url(r'^employees/$', views.employees, name="employees"),
    url(r'^employees/add_lead/', views.add_lead, name="add_lead"),
    url(r'^employees/delete/(?P<uid>[0-9]+)/$', views.delete_employee, name="delete_lead"),
    url(r'^incident_data/$', views.incident_data, name="incident_data"),
    url(r'^sectors/$', views.sectors, name="sector_data"),
    url(r'^sectors/edit/(?P<uid>[0-9]+)/$', views.edit_sector, name='edit_sector'),
    url(r'^sectors/delete/(?P<uid>[0-9]+)/$', views.delete_sector, name='edit_sector'),
    url(r'^sectors/add_sector$', views.add_sector, name="add_lead"),
    url(r'^crew_lead/authenticate_lead/$', views.authenticate_lead, name="authenticate_lead"),
    url(r'^crew_lead/add_incident/$', views.add_incident_CL, name="add_incident_CL")
]