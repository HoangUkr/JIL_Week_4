from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CustomerForm, ProductForm
from .task import generate_report

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
    orders = Order.objects.all()
    list_context = []
    context = {}
    for order in orders:
        create_date = order.date_created
        customer_name = order.customer.name
        product_name = order.product.name
        category = order.product.category
        price = order.product.price
        context = {
            'Date' : create_date,
            'Customer' : customer_name, 
            'Product' : product_name, 
            'Category' : category,
            'Price' : price}
        list_context.append(context)
    
    #generate_report(list_context)
    return render(request, 'accounts/report.html')

    
