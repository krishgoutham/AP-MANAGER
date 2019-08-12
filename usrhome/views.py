from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.views import generic
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import calendar
from Paytm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';


from .models import *
from .utils import Calendar
from .forms import EventForm


# Create your views here.
def profile(request):
    msg = Notice.objects.filter(user=request.user, delete=False)
    due = Rent.objects.filter(user=request.user, paid=False)
    pay = Rent.objects.filter(user=request.user, paid=True)
    return render(request, 'profile.html', {'dues': due, 'notification': msg, 'pastpay':pay})


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('usrhome:calendar'))
    return render(request, 'event.html', {'form': form})

def show_msg(request,note_id):
    msg = Notice.objects.get(id=note_id)
    return render(request, 'message.html', {'notification':msg})

def dues(request,due_id):
    msg = Rent.objects.get(id=due_id)
    return render(request, 'paynow.html', {'dues':msg})

def pastpaymnets(request,pay_id):
    msg = Rent.objects.get(id=pay_id)
    return render(request,'paymentdone.html',{'pastpay':msg})

def del_msg(request,note_id):
    msg = Notice.objects.get(id=note_id)
    msg.delete=True;
    msg.save()
    return HttpResponseRedirect('/profile')


def paymentreq(request,order_id):
    msg = Rent.objects.get(id=order_id)
    #passing request to paytm
    param_dict = {

        'MID': 'WorldP64425807474247',
        'ORDER_ID': msg.order_id,
        'TXN_AMOUNT': str(msg.amount),
        'CUST_ID': str(request.user),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://18.216.172.90/handlerequest/',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request,'paytm.html',{'param_dict':param_dict})


@csrf_exempt
def handlerequest(request):
    #paytm post req
    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == 'CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']== '01':
            print('Payment successfull')
            msg = Rent.objects.get(order_id=response_dict['ORDERID'])
            msg.paid = True;
            msg.paid_on = response_dict['TXNDATE']
            msg.save()
        else:
            print('Payment was not successfull because' + response_dict['RESPMSG'])

    return render(request, 'paymentstatus.html', {'resp':response_dict})
