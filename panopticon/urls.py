import panopticon.views as views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^new-user/$', views.create_user, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^productivity/', views.productivity, name="productivity"),
    url(r'^incidents/', views.incidents, name="incidents"),
    url(r'^edit-site/', views.edit_site, name="edit_site"),
    url(r'^add-site/', views.add_site, name="add_site"),
    url(r'^change-site/', views.change_site, name="change_site")
]