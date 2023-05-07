# Generated by Django 4.1.5 on 2023-04-12 11:26

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='İsim')),
                ('email', models.CharField(blank=True, max_length=50, verbose_name='E-posta Adresi')),
                ('subject', models.CharField(blank=True, max_length=50, verbose_name='Konu')),
                ('message', models.TextField(blank=True, max_length=255, verbose_name='Mesajınız')),
                ('status', models.CharField(choices=[('New', 'Yeni'), ('Read', 'Okundu'), ('Closed', 'Kapandı')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'İletişim',
                'verbose_name_plural': 'İletişim',
                'db_table': 'İletişim',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('keywords', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=50)),
                ('adress', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('fax', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('smtpserver', models.CharField(blank=True, max_length=20, null=True)),
                ('smtpemail', models.CharField(blank=True, max_length=20, null=True)),
                ('smtppassword', models.CharField(blank=True, max_length=10, null=True)),
                ('smtpport', models.CharField(blank=True, max_length=5, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('facebook', models.CharField(blank=True, max_length=50, null=True)),
                ('instagram', models.CharField(blank=True, max_length=50, null=True)),
                ('aboutus', ckeditor.fields.RichTextField()),
                ('contact', ckeditor.fields.RichTextField(blank=True)),
                ('references', ckeditor.fields.RichTextField(blank=True)),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ayar',
                'verbose_name_plural': 'Ayarlar',
                'db_table': 'Ayarlar',
            },
        ),
    ]
