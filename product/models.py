from django.db import models
from product.models import *
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Category(MPTTModel):
    STATUS = [
        ('True', 'Evet'),
        ('False', 'Hayır'),
    ]
    title = models.CharField(max_length=150,verbose_name="Kategori İsmi")
    collection = models.CharField(max_length=150,blank=True, null=True,verbose_name="kolleksiyon")
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    image2 = models.ImageField(null=True, blank=True, upload_to='images/')
    slug = AutoSlugField(populate_from='title', unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    materialIcon = models.CharField(null=True,blank=True,max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        db_table = 'Kategoriler'
        verbose_name_plural = 'Kategoriler'
        verbose_name = 'Kategori'


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    # get_absolute_url kullanarak yönlendirme
    def get_absolute_url(self):
        return reverse(
            'category_products',
            kwargs={
                'slug':self.slug,
            }
        )

class Campaigns(models.Model):
    title = models.CharField(max_length=150)
    slogan = models.CharField(max_length=150, null=True,blank=True)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    slug = AutoSlugField(populate_from='title', unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Kampanyalar'
        verbose_name_plural = 'Kampanyalar'
        verbose_name = 'Kampanya'

    def __str__(self):
        return self.title
    
    # get_absolute_url kullanarak yönlendirme
    def get_absolute_url(self):
        return reverse(
            'campaigns_products',
            kwargs={
                'slug':self.slug,
            }
        )
    
    
class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='title', unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        db_table = 'Products'
        verbose_name_plural = "Ürünler"

    productTitle = models.CharField(max_length=5000, verbose_name="Ürün İsmi")
    productPrice = models.FloatField(verbose_name="Ürün Fiyatı")
    productDescription = RichTextField(verbose_name="Ürünün kısa Açıklaması")
    productDetail = RichTextField(verbose_name="Ürün Özellikleri")
    productImage = models.ImageField(verbose_name="Ürün Görseli", upload_to="products/",blank=True,null=True)
    productShipping = models.BooleanField(default=False,verbose_name="Ücretsiz Kargo Mu",blank=False,null=False)
    stock         = models.PositiveIntegerField(verbose_name=_("Stock"))
    productCategorie = models.ManyToManyField(Category,verbose_name="Kategori")
    productCampaigns = models.ManyToManyField(Campaigns,verbose_name="Kampanya", blank=True)
    productTag = models.ManyToManyField(Tag,verbose_name="Etiket")
    newSlug      = AutoSlugField(populate_from="productTitle",unique=True,blank=True,default="",editable=True)
    created_att  = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    update_att = models.DateTimeField(auto_now=True,verbose_name=_("Modified Date"))

    def __str__(self):
        return self.productTitle

    class Meta:
        db_table = 'Ürünler'
        verbose_name_plural = 'Ürünler'
        verbose_name = 'Ürün'




class Images(models.Model):
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='image/')

    class Meta:
        db_table = 'Ürün-Resimleri'
        verbose_name_plural = 'Ürün-Resimleri'
        verbose_name = 'Ürün-Resmi'

    def __str__(self):
        return self.title


VARIATION_CATEGORY_CHOICES=(
    ("color","Renk"),
    ("size","Beden")
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color",is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size",is_active=True)


class ProductVariationModel(models.Model):
    product            = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations",verbose_name=_("Product"))
    variation_category = models.CharField(max_length=150,choices=VARIATION_CATEGORY_CHOICES,verbose_name=_("Variation Category"))
    variation_value    = models.CharField(max_length=100,verbose_name=_("Variation Value"))
    is_active          = models.BooleanField(default=True,verbose_name=_("Is Active"))
    created_date       = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    objects            = VariationManager()

    class Meta:
        verbose_name        = _("Product Variation")
        verbose_name_plural = _("Product Variations")
        db_table            = "ProductVariations"
        ordering = ['-id']

    def __str__(self):
        return self.variation_value
    
    


class Comment(models.Model):
    STATUS = [
        ('New', 'Bekliyor'),
        ('True', 'Onaylandı'),
        ('False', 'Reddedildi'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='yorum')
    user = models.ForeignKey('user.UserProfile',on_delete=models.CASCADE, related_name='yazan')
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField(blank=True, null=True)
    status = models.CharField(blank=True, choices=STATUS, max_length=10, default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_att = models.DateTimeField(auto_now_add=True)
    update_att = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Yorumlar'
        verbose_name_plural = 'Yorumlar'
        verbose_name = 'Yorum'

    def __str__(self):
        return self.subject
