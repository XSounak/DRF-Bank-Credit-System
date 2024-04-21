from django.db import models

class Customer(models.Model):
    customer = models.IntegerField(default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField(null=True)
    current_debt = models.FloatField(null=True)
    
    class Meta:
        app_label = 'customer'