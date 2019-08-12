from django.shortcuts import render
from datetime import timedelta, date, datetime
from django.http import HttpResponseRedirect
from .models import *
from django.utils.dateparse import parse_date


def index(request):
    # TODO: Add alerts
    if request.user.is_superuser:
        orders = reversed(Order.objects.all())
    else:
        orders = reversed(Order.objects.filter(order_creator=request.user.id))
    inclusions = Inclusion.objects.all()
    ctx = {
        'orders': orders,
        'inclusions': inclusions
    }
    if request.method == 'POST':
        if request.POST.get('from_date') and request.POST.get('to_date'):
            orders = Order.objects.filter(
                order_guest_check_in_date__range=(request.POST.get('from_date'), request.POST.get('to_date')))
            ctx['orders'] = orders
    return render(request, "index.html", ctx)
