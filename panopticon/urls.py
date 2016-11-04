import panopticon.views as views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^new-user/$', views.create_user, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^productivity/', views.productivity, name="productivity"),
    url(r'^incidents/$', views.incidents, name="incidents"),
    url(r'^incidents/add_incident/$', views.add_incident, name="incidents"),
    url(r'^incidents/add_injury/$', views.add_incident, name="incidents"),
    url(r'^edit_site/$', views.edit_site, name="edit_site"),
    url(r'^add_site/', views.add_site, name="add_site"),
    url(r'^change_site/', views.change_site, name="change_site"),
    url(r'^employees/$', views.employees, name="employees"),
    url(r'^employees/add_lead/', views.add_lead, name="add_lead"),
    url(r'^incident_data/$', views.incident_data, name="incident_data"),
    url(r'^sectors/$', views.sectors, name="sector_data"),
    url(r'^sectors/add_sector$', views.add_sector, name="add_lead"),
]