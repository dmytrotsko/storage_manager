from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from indussystem.models import Villa
from .models import VillaReports, Service, ServiceType


def villa_list(request):
    villa_list = Villa.objects.all()
    paginator = Paginator(villa_list, 25)

    page = request.GET.get('page')
    villas = paginator.get_page(page)
    return render(request, "service_manager/villas_list.html", {'villas': villas})


def villa_expenses(request, pk):
    villa = Villa.objects.get(pk=pk)
    villa_expenses_list = Service.objects.filter(villa=villa)
    services_types = ServiceType.objects.all()
    paginator = Paginator(villa_expenses_list, 25)

    page = request.GET.get('page')
    expenses = paginator.get_page(page)
    if request.method == "POST":
        service_type_to_add = request.POST.get("service_type_add")
        if service_type_to_add:
            try:
                service_type = ServiceType(name=service_type_to_add)
                service_type.save()
            except IntegrityError:
                pass
        service_name_to_add = request.POST.get("service_name_select")
        if service_name_to_add:
            chosen_type = ServiceType.objects.get(name=service_name_to_add)
            price = int(request.POST.get("service_price"))
            service = Service(type=chosen_type, price=price, villa=villa)
            service.save()
        return HttpResponseRedirect("/service_manager/{}/expenses".format(pk))

    return render(request, "service_manager/villa_expenses.html", {'expenses': expenses,
                                                                    'services_types': services_types})

def villa_reports(request, villa_id):
    villa = Villa.objaects.get(pk=villa_id)
    villa_reports_list = VillaReports.objects.get(villa = villa)
    paginator = Paginator(villa_reports_list, 25)

    page = request.GET.get('page')
    reports = paginator.get_page(page)
    return render(request, "service_manager/villa_reports.html", {'reprots': reports})


def generate_update_report(request, villa_id, for_custom_period=1,update=0):
    villa = Villa.objaects.get(pk=villa_id)
