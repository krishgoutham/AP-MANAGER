from django.urls import path
from django.conf.urls import url
from . import views
from usrhome.views import profile

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

]
