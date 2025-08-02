import requests

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.conf import settings

from .models import Order

@receiver (post_save, sender = Order)
def send_notification_email(sender, instance, created, **kwargs):
    orders = Order.objects.all()
    if created:
        subject = f"New Order Created!"
        for order in orders:
            message = f"""New Orders:  
                            Name:     {order.product.name}
                            Quantity: {order.quantity}
                            User:     {order.user.email} """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['buzurgoo6@gmail.com'] 

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)    

# @receiver(pre_save, sender = Order)
# def total_price(instance,created,**kwargs):

#     if created:
#         Order.objects.create(total_price =)


# booking/signals.py



TELEGRAM_BOT_TOKEN = '7579652262:AAE928Lxn5Ifa2pm4TBoZJu4vnhsR0qwkAs'
TELEGRAM_CHAT_ID = '@merve435'  

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram Error] {e}")

@receiver(post_save, sender=Order)
def notify_order_created(sender, instance, created, **kwargs):
    if created:
        message = (
            f"🛒 <b>New Order Created</b>\n"
            f"📦 Product: {instance.product.name}\n"
            f"👤 User: {instance.user.email}\n"
            f"💵 Total: ${instance.total_price}\n"
            f"🔢 Quantity: {instance.quantity}\n"
            f"📅 Date: {instance.created_at.strftime('%Y-%m-%d')}"
        )
        send_telegram_message(message)

