# Generated by Django 4.1.5 on 2023-04-12 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0003_alter_ordermodel_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customersss', to=settings.AUTH_USER_MODEL, verbose_name='Müşteri'),
        ),
    ]
