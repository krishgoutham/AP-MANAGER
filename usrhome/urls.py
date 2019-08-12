from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'usrhome'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^message/(?P<note_id>\d+)/$', views.show_msg),
    url(r'^dues/(?P<due_id>\d+)/$', views.dues),
    url(r'^payments_done/(?P<pay_id>\d+)/$', views.pastpaymnets),
    url(r'^delete/(?P<note_id>\d+)/$', views.del_msg),
    url(r'^payment/(?P<order_id>\d+)/$', views.paymentreq, name="paymentreq"),
]
