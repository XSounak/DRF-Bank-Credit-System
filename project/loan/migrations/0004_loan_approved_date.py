# Generated by Django 4.2.9 on 2024-01-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_alter_loan_monthly_installment'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='approved_date',
            field=models.DateField(default='2022-01-01'),
        ),
    ]
