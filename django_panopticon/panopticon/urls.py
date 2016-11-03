import panopticon.views as views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.dashboard, name="home"),
    url(r'^new-user/$', views.create_user, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^productivity/', views.productivity, name="productivity"),
    url(r'^incidents/', views.incidents, name="incidents")
]