# Generated by Django 4.1.5 on 2023-04-12 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customersss', to=settings.AUTH_USER_MODEL, verbose_name='Müşteri'),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='order.ordermodel', verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='variation',
            field=models.ManyToManyField(blank=True, to='product.productvariationmodel', verbose_name='Product Variation'),
        ),
    ]
