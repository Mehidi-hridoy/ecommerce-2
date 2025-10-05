# In promotions/views.py or admin action
from twilio.rest import Client
from django.conf import settings
from customers.models import Customer

def send_sms_promotion(self, request, queryset):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for promo in queryset:
        for customer in Customer.objects.all()[:10]:  # Limit
            message = client.messages.create(
                body=promo.sms_template,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=customer.user.phone
            )
    self.message_user(request, f"Sent {queryset.count()} promotions via SMS")
send_sms_promotion.short_description = "Send SMS Promotion"