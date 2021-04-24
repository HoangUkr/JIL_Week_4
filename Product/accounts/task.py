from __future__ import absolute_import, unicode_literals
from Product.celery import app
import csv
from datetime import date
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
@app.task(bind = True)
def generate_report(self, data):
    today = date.today()
    d1 = today.strftime("%b-%d-%Y")
    filename = 'report/report_' + d1 + '.csv'
    try:
        with open(filename, mode='w') as csv_file:
            fieldnames = ['Date', 'Customer', 'Product', 'Category', 'Price']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for dict_data in data:
                writer.writerow(dict_data)
        logger.info('Generating report for date ' + d1)
    except IOError as exc:
        raise self.retry(exc=exc)
        print('I/O error')




    