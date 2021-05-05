from __future__ import absolute_import, unicode_literals
from Product.celery import app
import csv
from datetime import date
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery import shared_task
import time
import pathlib
from .models import *
from .forms import OrderForm, CustomerForm, ProductForm
from celery.decorators import task
from celery.result import AsyncResult

logger = get_task_logger(__name__)
today = date.today()
d1 = today.strftime("%b-%d-%Y")
filename = 'report_' + d1 + '.csv'

@app.task(bind=True)
def generate_report(self):
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
    
    
    fl = pathlib.Path(filename)
    if fl.exists():
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Date', 'Customer', 'Product', 'Category', 'Price']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for dict_data in list_context:
                writer.writerow(dict_data)
    else:
        f = open(filename, "x")
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Date', 'Customer', 'Product', 'Category', 'Price']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for dict_data in list_context:
                writer.writerow(dict_data)
    logger.info('Generating report for date ' + d1)

def get_task_status(task_id):
    task = generate_report.AsyncResult(task_id)
    status = task.status
    return {'Status':status, 'Path': filename}




    