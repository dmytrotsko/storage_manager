import datetime
from dateutil.relativedelta import relativedelta

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.dateparse import parse_date
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
    villa = Villa.objects.get(pk=villa_id)
    villa_reports_list = VillaReports.objects.filter(villa = villa)
    paginator = Paginator(villa_reports_list, 25)

    page = request.GET.get('page')
    reports = paginator.get_page(page)
    return render(request, "service_manager/villa_reports.html", {'reports': reports,
                                                                  'villa': villa})


def generate_update_report(request, villa_id,report_id=-1):
    villa = Villa.objects.get(pk=villa_id)
    today = datetime.date.today()
    d = today - relativedelta(months=1)
    
    if report_id >= 0:
        report = VillaReports.objects.get(pk=report_id)
        start_date = report.start_date
        end_date = report.end_date
    else:
        report = None
        start_date = datetime.date(d.year, d.month, 1).strftime('%Y-%m-%d')
        end_date = (datetime.date(today.year, today.month, 1) - relativedelta(days=1)).strftime('%Y-%m-%d')

    if request.method == 'POST':
        start_date = parse_date(request.POST.get('start_date'))
        end_date = parse_date(request.POST.get('end_date'))
        services_list = Service.objects.filter(villa=villa).filter(date__range = [start_date, end_date])
        expenses = 0
        for service in services_list:
            expenses += service.price
        
        income = float(request.POST.get('income'))
        occupancy = int(request.POST.get('occupancy'))
        profit = income - expenses
        averange_price = income/occupancy
        if report:
            report.start_date = start_date
            report.end_date = end_date
            report.expenses = expenses
            report.income = income
            report.occupancy = occupancy
            report.profit = profit
            report.averange_price = averange_price
            
        else:
            report = VillaReports.objects.create(villa=villa,
                                        income=income,
                                        expenses=expenses,
                                        occupancy=occupancy,
                                        profit=profit,
                                        averange_price=averange_price,
                                        start_date=start_date,
                                        end_date=end_date )
        report.save()
        
        return HttpResponseRedirect("/service_manager/{}/reports".format(villa_id))

    ctx = {'villa': villa,
           'report': report,
           'start_date':start_date,
           'end_date':end_date}

    return render(request, 'service_manager/villa_financial_report.html', ctx)


