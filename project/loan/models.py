from django.db import models
from customer.models import Customer

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.IntegerField()
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    emi_paidontime = models.IntegerField(default=0)
    start_date = models.DateField(default='2022-01-01')
    end_date = models.DateField(default='2022-01-01')

    class Meta:
        app_label = 'loan'
