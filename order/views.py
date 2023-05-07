import datetime
import uuid
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import *
from django.shortcuts import redirect, render
from product.models import *
from .forms import OrderForm
from order.models import *
from django.views.generic import View, ListView, DetailView

class CheckoutView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]
    def get(self,request,total=0,amount=0,cart_items=None):
        grand_total = 0
        tax = 0
        try:
            cart_items = CartModel.objects.filter(user=self.request.user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.productPrice * cart_item.amount)
                amount += cart_item.amount
                product = cart_item.product
            tax = (2 * total) / 100
            grand_total = total + tax
        except Exception as e:
            pass
        global_categories = Category.objects.filter(id__range =(4,100))
        favorites = FavoriteModel.objects.filter(customer=request.user.id)
        products = CartModel.objects.filter(user=request.user.id)
        total = 0
        for product_ in products:
            total += product_.amount * product_.product.productPrice
        request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
        request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
        ctx = {
            "total": total,
            "amount": amount,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
            "favorites": favorites,
            "products": products,
            "total": total,
            "global_categories": global_categories,
            "product": product,
        }
        
        return render(request,"checkout.html",ctx)

class PlaceOrderView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]

    def get_cart_items(self):
        return CartModel.objects.filter(user=self.request.user)

    def get_price_info(self):
        total = 0
        amount = 0
        cart_items = self.get_cart_items()
        for item in cart_items:
            total += (item.product.productPrice * item.amount)
            amount += item.amount
        tax = (2 * total) / 100
        grand_total = total + tax
        return {"grand_total":grand_total,"tax":tax,"total":total}

    def get_date(self):
        year  = int(datetime.date.today().strftime("%Y"))
        day   = int(datetime.date.today().strftime("%d"))
        month = int(datetime.date.today().strftime("%m"))
        date  = datetime.date(year=year,month=month,day=day)
        current_date = date.strftime("%Y%m%d")
        return current_date

    def get(self,request):
        user = request.user
        self.cart_items = CartModel.objects.filter(user=user)
        cart_count = self.cart_items.count()
        if cart_count <= 0:
            return redirect("index")

        return redirect("index")

    def post(self,request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order_data = form.save(commit=False)
            order_data.order_total  = self.get_price_info().get("grand_total")
            order_data.tax          = self.get_price_info().get("tax")
            order_data.ip           = self.request.META.get("REMOTE_ADDR")
            order_data.user         = self.request.user
            order_data.created_date = self.get_date()
            order_data.order_number =  str(self.get_date()) + "-"+ str(uuid.uuid4())
            form.save()
            global_categories = Category.objects.filter(id__range =(4,100))
            order = OrderModel.objects.get(user=self.request.user,is_ordered=False,order_number=order_data.order_number)
            favorites = FavoriteModel.objects.filter(customer=request.user.id)
            products = CartModel.objects.filter(user=request.user.id)
            total = 0
            for product_ in products:
                total += product_.amount * product_.product.productPrice
            request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
            request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
            ctx={
                "global_categories":global_categories,
                "favorites":favorites,
                "products":products,
                "total":total,
                "order":order,
                "cart_items":self.get_cart_items(),
                "grand_total":self.get_price_info().get("grand_total"),
                "tax":self.get_price_info().get("tax"),
                "total":self.get_price_info().get("total"),
            }

            return render(request,"payments.html",ctx)
        else:
            messages.warning(request,"Bir sorun oluştu")
            return redirect("url_checkout")


class PaymentView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]

    def get(self,request):
        return render(request,"payments.html")

    def cartItemsToOrderItems(self):
        cart_items   = CartModel.objects.filter(user=self.request.user)
        order_number = self.get_post_data().get("order_number")
        order        = OrderModel.objects.filter(order_number=order_number)[0]

        for item in cart_items:
            cart_item = CartModel.objects.get(id=item.id)
            variation = cart_item.variations.all()

            order_item = OrderItemModel.objects.create(
                order_id      = order.id,
                user          = self.request.user,
                product       = item.product,
                amount      = item.amount,
                product_price = item.product.productPrice,
                ordered       = True,
            )
            order_item = OrderItemModel.objects.get(id=order_item.id)
            order_item.variation.set(variation)
            order_item.save()

            # stoktan azaltma stok bittiğinde hata veriyor
            product = Product.objects.get(id=item.product.id)
            product.stock -= item.amount
            product.save()
        CartModel.objects.filter(user=self.request.user).delete()
        

    def send_mail_to_user(self):
        try:
            with transaction.atomic():
                mail_subject = "Siparişiniz İçin Teşekkürler"
                message = render_to_string("order_mail.html", {
                    "user" : self.request.user,
                    "order": self.get_order()
                })
                to_email = self.request.user.email

                send_email = EmailMessage(mail_subject, message, to=[to_email], )
                send_email.send()
        except Exception as e:
            print(e)
            messages.error(self.request, "Bir Sorun Oluştu. Lütfen sonra tekrar deneyiniz.")

    def get_order(self):
        return OrderModel.objects.get(order_number=self.get_post_data().get("order_number"))


    def get_post_data(self):
        card_name    = self.request.POST.get("card_name")
        card_number  = self.request.POST.get("card_number")
        card_exp     = self.request.POST.get("card_exp")
        card_cvv     = self.request.POST.get("card_cvv")
        order_number = self.request.POST.get("order_number")
        return {
            "card_name":card_name,"card_number":card_number,"card_exp":card_exp,"card_cvv":card_cvv,"order_number":order_number
        }

    def get_order_items(self):
        order_items = OrderItemModel.objects.filter(order=self.get_order())
        return order_items

    def post(self,request):
        isPaymentSuccess = True
        if isPaymentSuccess:
            self.cartItemsToOrderItems()
            self.send_mail_to_user()
            order = self.get_order()
            global_categories = Category.objects.filter(id__range =(4,100))

            orders = OrderModel.objects.filter(user_id=request.user.id).order_by('-created_date')[:1]
            
            favorites = FavoriteModel.objects.filter(customer=request.user.id)
            
            request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
            request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
            ctx = {
                "order_number":self.get_post_data().get("order_number"),
                "status":order.status,
                "date":order.created_date,
                "order_items":self.get_order_items(),
                "tax":order.tax,
                "total":order.order_total,
                "favorites":favorites,
                
                "orders":orders,
                "global_categories":global_categories,

            }
            return render(request,"order_complete.html",ctx)
        else:
            messages.error(request,"Sipariş işlemi sırasında bir sorun oluştu")
            return render()


class OrderCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "order_complete.html"

    