from django.db import models
from authen.models import User

# Create your models here.
class Product(models.Model):
    original_id = models.CharField(max_length=255)
    product_name = models.TextField()
    price = models.PositiveBigIntegerField()
    product_link = models.TextField()
    images_link = models.TextField()
    shop = models.TextField(null=True)
    ctime = models.IntegerField()
    user = models.ManyToManyField(
        User,
        through='ProductUser',
        through_fields=('product', 'user'),
    )

    class Meta:
        db_table = 'products'


class ProductUser(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    favorite = models.BooleanField(null=True)
    view_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_user'
