from django.db.models.signals import post_save
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