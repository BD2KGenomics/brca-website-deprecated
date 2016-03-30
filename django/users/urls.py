from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
]
