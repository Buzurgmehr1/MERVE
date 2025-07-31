from django.db import models

# Create your models here.

class Order(models.Model):
    product = models.ForeignKey("menu.Product", related_name='product_orders', on_delete=models.CASCADE)
    total_price = models.DecimalField( max_digits=5, decimal_places=2)
    quantity = models.DecimalField( max_digits=5, decimal_places=2)
    user = models.OneToOneField("accounts.CustomUser", related_name='user_orders', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} -- {self.user.email} -- {self.quantity}"
    
    class Meta:
        db_table = 'order'
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'