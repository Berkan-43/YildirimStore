from django.db import models
from product.models import *
from user.models import *

STATUS = (
    ("New",("Yeni Sipariş")),
    ("Receipt", ("Receipt")),
    ("Completed", ("Completed")),
    ("Canceled", ("Canceled")),
)
class OrderModel(models.Model): # sipariş veren kişi bilgisi
    user = models.ForeignKey('user.UserProfile', on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name="Müşteri", related_name="customersss")
    order_number   = models.CharField(max_length=100,verbose_name=("Order Number"))
    slug = models.SlugField(null=True, unique=True, editable=True)
    first_name     = models.CharField(max_length=50,verbose_name=("First Name"))
    last_name      = models.CharField(max_length=50,verbose_name=("Last Name"))
    phone          = models.CharField(max_length=50,verbose_name=("Phone"))
    email          = models.EmailField(max_length=50,verbose_name=("Email"))
    address_title  = models.CharField(max_length=50,verbose_name=("Address Title"))
    city           = models.CharField(max_length=50,verbose_name=("City"))
    clear_address  = models.CharField(max_length=500,verbose_name=("Clear Address"))
    order_note     = models.CharField(max_length=400,verbose_name=("Order Note"))
    order_total    = models.FloatField(verbose_name=("Order Total"))
    tax            = models.FloatField(verbose_name=("Vergi"))
    status         = models.CharField(max_length=20,choices=STATUS,default="New",verbose_name=("Status"))
    ip             = models.CharField(max_length=20,blank=True,verbose_name=("IP Address"))
    is_ordered     = models.BooleanField(default=False,verbose_name=("Is Ordered"))
    created_date   = models.DateTimeField(auto_now_add=True,verbose_name=("Created Date"))
    update_date    = models.DateTimeField(auto_now=True,verbose_name=("Update Date"))

    def get_fullname(self):
            return f"{self.first_name} {self.last_name}"

    def get_full_address(self):
        return f"{self.address_title} {self.city} {self.clear_address}"

    def __str__(self):
        return self.first_name

    # def __str__(self):
    #     return str(self.id) + " " + self.user.username

    class Meta:
        db_table = 'Orders'
        verbose_name_plural = "Siparişler"

class OrderItemModel(models.Model): # Sipariş verilen ürünün bilgileri
    order         = models.ForeignKey(OrderModel,on_delete=models.CASCADE,related_name="products",verbose_name=("Order"))
    user          = models.ForeignKey('user.UserProfile',on_delete=models.CASCADE,verbose_name=("User"))
    product       = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=("Product"))
    variation     = models.ManyToManyField(ProductVariationModel,blank=True,verbose_name=("Product Variation"))
    amount      = models.PositiveIntegerField(verbose_name=("Amount"))
    product_price = models.FloatField(verbose_name=("Product Price"))
    ordered       = models.BooleanField(default=False,verbose_name=("Ordered"))
    status        = models.CharField(max_length=100,verbose_name=("Status"))
    created_add   = models.DateTimeField(auto_now_add=True,verbose_name=("Created Add"))

    def __str__(self):
        return self.product.productTitle

    class Meta:
        db_table = 'Order_Items'
        verbose_name_plural = "Sipariş Ürünleri"
