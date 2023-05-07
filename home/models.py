from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    description = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    adress = models.CharField(blank=True, null=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, null=True, max_length=15)
    email = models.CharField(blank=True, null=True, max_length=50)
    smtpserver = models.CharField(blank=True, null=True, max_length=20)
    smtpemail = models.CharField(blank=True, null=True, max_length=20)
    smtppassword = models.CharField(blank=True, null=True, max_length=10)
    smtpport = models.CharField(max_length=5, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, null=True, max_length=50)
    instagram = models.CharField(blank=True, null=True, max_length=50)
    aboutus = RichTextField()
    contact = RichTextField(blank=True)
    references = RichTextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Ayarlar'
        verbose_name_plural = 'Ayarlar'
        verbose_name = 'Ayar'

    def __str__(self):
        return self.title

class ContactModel(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('Read', 'Okundu'),
        ('Closed', 'Kapandı'),
    )
    name = models.CharField(max_length=20, blank=True, verbose_name="İsim")
    email = models.CharField(max_length=50, blank=True, verbose_name="E-posta Adresi")
    subject = models.CharField(max_length=50, blank=True, verbose_name="Konu")
    message = models.TextField(max_length=255, blank=True, verbose_name="Mesajınız")
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'İletişim'
        verbose_name_plural = 'İletişim'
        verbose_name = 'İletişim'

    def __str__(self):
        return self.name