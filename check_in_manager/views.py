from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import OrderForm
from .models import *


def index(request):
    if request.user.is_superuser:
        orders = reversed(Order.objects.all())
    else:
        orders = reversed(Order.objects.filter(order_creator=request.user.id))
    ctx = {
        'orders': orders,
    }
    if request.method == 'POST':
        if request.POST.get('from_date') and request.POST.get('to_date'):
            orders = Order.objects.filter(
                order_guest_check_in_date__range=(request.POST.get('from_date'), request.POST.get('to_date')))
            ctx['orders'] = orders
    return render(request, "index.html", ctx)


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    ctx = {
        'order': order,
    }
    return render(request, 'order_details.html', ctx)


def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(instance=order, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(order_id))
    else:
        form = OrderForm(instance=order)

    ctx = {
        'order': order,
        'form': form
    }
    return render(request, 'edit_order.html', ctx)


def create_order(request):
    # TODO: Add possibility to create Inclusion, SpecOccasion, Source while creating Order
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.order_creator = request.user
            new_order.save()
            return HttpResponseRedirect("/check_in_manager/orders_table/order/{}/details/".format(new_order.id))
    else:
        form = OrderForm()
    ctx = {
        'form': form
    }
    return render(request, 'create_order.html', ctx)
