# Generated by Django 4.1.5 on 2023-05-04 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productTitle',
            field=models.CharField(max_length=5000, verbose_name='Ürün İsmi'),
        ),
    ]
