"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime, date
import time
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

def call_api():
    print('Job started at: %s' % datetime.now())
    url = 'http://localhost:8000/api/send_monthly_email/'
    response = requests.get(url)
    print(response.json())


def start():
    print('Cron Job Started')
    today = datetime.today()
    scheduler.add_job(call_api, 'date', run_date=date(today.year, today.month, 1))
    scheduler.start()
