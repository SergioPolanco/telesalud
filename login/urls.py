from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.login_view, name='login'),
    url(r'^logout-user/$', views.logout_view, name='login.logout')
]