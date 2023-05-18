# Standard imports
import requests

# Celery tasks
from celery import shared_task

# Django imports
from django.conf import settings

@shared_task
def dispatch_webhook(type, fid):
    print("RECEIVED TASK")
    
    # Dispatch webhook
    API_URLS = settings.RECIEVER_WEBHOOK_API_URLS
    webhook_urls = API_URLS.split(' ')

    for webhook_url in webhook_urls:
        
        # Include ID in the request body
        payload = {
                    'fid': str(fid),
                    'type': type
                  }
        response_hook = requests.post(webhook_url, data=payload)
        print("RESPONSE FROM WEBHOOK: ", response_hook.text)
      
    print("DONE WITH TASK")