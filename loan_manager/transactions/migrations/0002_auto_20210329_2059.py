# Generated by Django 3.1.7 on 2021-03-29 20:59

from django.db import migrations, models
import transactions.models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='ip_address',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
