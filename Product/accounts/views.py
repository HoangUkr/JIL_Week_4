from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CustomerForm, ProductForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .task import *
from celery.result import AsyncResult

# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    #orders = customer.order_set.all()
    #order_count = orders.count()
    startdate = request.GET.get("start-date", None)
    enddate = request.GET.get("end-date", None)
    if(startdate and enddate):
        orders = customer.order_set.filter(date_created__range = (startdate, enddate))
    else:
        orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customers.html', context)

def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing POST: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

def createCustomer(request):
    form = CustomerForm()
    if(request.method == 'POST'):
        form = CustomerForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/customer_form.html', context)

def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/products/')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)

def ReportPage(request):
    generate_btn = request.POST.get('Generate')
    refresh_btn = request.POST.get('Refresh')
    query_result = Report.objects.all()
    if generate_btn:
        task = generate_report.apply_async()
        status = get_task_status(task.id)
        a = Report(task_id = task.id, path = status['Path'], status = status['Status'])
        a.save()
        query_result = Report.objects.all()
    if refresh_btn:
        id = Report.objects.latest('task_id')
        new_status = get_task_status(id)
        a = Report.objects.get(task_id = id)
        a.status = str(new_status['Status'])
        a.save()
        query_result = Report.objects.all()

    context = {'query_result' : query_result}
    return render(request, 'accounts/report.html', context)
"""
def generate_report_trigger(request):
    task = generate_report.apply_async()
    status = get_task_status(task.id)
    Report.objects.create(task_id = task.id, path = status['Path'], status = status['Status'])
    query_result = Report.objects.all()
    context = {'query_result' : query_result}
def refresh(request):
    pass
"""
