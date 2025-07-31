from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField( max_length=50 )

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
class Product(models.Model):
    name = models.CharField( max_length=50)
    image = models.ImageField()
    category_id = models.ForeignKey(Category,related_name='category_product', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'