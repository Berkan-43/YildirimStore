from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from user.forms import *
from user.models import *
from order.models import *
from order.forms import *
from home.models import *
from product.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

@login_required(login_url='login')
def v_profile(request):
    global_categories = Category.objects.filter(id__range =(4,100))
    setting = Setting.objects.get(pk=1)
    user = UserProfile.objects.filter(id=request.user.id)
    profile = UserProfile.objects.get(id=request.user.id)
    
    userAddress = AddressModel.objects.filter(customer=request.user)
    adresForm= AddressForm(request.POST or None)
    if adresForm.is_valid():
        address = adresForm.save(commit=False)
        address.customer = request.user
        address.save()
        messages.success(request, "Address Başarıyla Eklendi")
        return redirect("profile")
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, "profile.html", {"user": user[0], "userAddress": userAddress,"adresForm": adresForm, 'profile':profile, 'setting':setting, 'global_categories':global_categories})

@login_required(login_url='login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance= request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'{request.user.username} Profiliniz başarıyla güncellendi.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance= request.user)
        profile_form= ProfileUpdateForm(instance= request.user) 
        current_user = request.user
        profile = UserProfile.objects.get(id=current_user.id)
        setting = Setting.objects.get(pk=1)
        global_categories = Category.objects.filter(id__range =(4,100))
        return render(request, 'user_update.html', context={
            'profile_form':profile_form,
            'user_form':user_form,
            'profile':profile,
            'setting':setting,
            'global_categories':global_categories,
        })
    
def userDelete(request):
    profile = request.user
    profile.delete()
    messages.success(request, 'Hesabınız başarıyla silinmiştir.')
    return redirect('/')


def adressDelete(request):
    address = AddressModel.objects.filter(customer=request.user)
    address.customer = request.user
    address.delete()
    messages.success(request, "Address Başarıyla Silindi")
    return redirect('profile')


@login_required(login_url='login')
def v_favorites(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, "favories.html", {"favorites": favorites, "products": products, "total": total, 'setting':setting, 'global_categories':global_categories})

@login_required(login_url='login')
def v_cart(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    product = Product.objects.filter(products=request.user.id)      

    products = CartModel.objects.filter(user=request.user)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, "shoppingcart.html", {"products": products, "total": total, 'setting':setting, "favorites": favorites, 'global_categories':global_categories, 'product':product})


# def v_cart(request):
#     setting = Setting.objects.get(pk=1)
#     global_categories = Category.objects.filter(id__range=(4, 100))
#     favorites = FavoriteModel.objects.filter(customer=request.user.id)
#     products = CartModel.objects.filter(user=request.user)
#     total = 0
#     for product_ in products:
#         product = product_.product
#         if product.stock >= product_.amount:
#             product_.product.stock -= product_.amount
#             product_.product.save()
#             total += product_.amount * product_.productPrice
#         else:
#             product_.delete()

#     request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
#     request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()

#     return render(request, "shoppingcart.html", {"products": products, "total": total, 'setting': setting, "favorites": favorites, 'global_categories': global_categories})


@login_required(login_url='login')
def f_update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    _customer = request.user

    product = Product.objects.get(id=productId)
    cartItem = CartModel.objects.filter(user=_customer).filter(product_id=productId)
    if not cartItem:
        cartItem = CartModel.objects.create(product_id=productId, user=_customer, amount=1)
        cartItem.save()
        
    else:
        cartItem = CartModel.objects.get(user=_customer, product_id=productId)
        if action == "add":
            cartItem.amount += 1
        elif action == "remove":
            cartItem.amount -= 1
        cartItem.save()
        request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
        request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return JsonResponse(
        "<div class='inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200'><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'></path></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-md font-normal'>Ürün sepete başarıyla eklenmiştir.</div><button @click='dismissed=true' type='button' class='ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700' data-dismiss-target='#toast-success' aria-label='Close'><span class='sr-only'>Close</span><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg></button>",
        safe=False)

@login_required(login_url='login')
def f_update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data["action"]
    cartItem = CartModel.objects.get(product_id=productId, user_id=request.user.id)
    if action == "add":
        cartItem.amount += 1
        cartItem.save()
        request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
        messages.success(request, "Sepetiniz başarıyla güncellenmiştir")
    elif action == "remove":
        if cartItem.amount == 1:
            cartItem.delete()
            request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
            messages.success(request, "Ürün başarıyla sepetinizden kaldırılmıştır")
        else:
            cartItem.amount -= 1
            cartItem.save()
            request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
            messages.success(request, "Sepetiniz başarıyla güncellenmiştir")
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return JsonResponse("asdf", safe=False)

@login_required(login_url='login')
def f_update_favorites(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data["action"] 
    if action == "add":
        try:
            # eğer ürünü veritabanında bulursa try blogu calısacak
            favItem = FavoriteModel.objects.get(customer_id=request.user.id, product_id=productId)
            return JsonResponse(
                "<div class='inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200'><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg><span class='sr-only'>Error icon</span></div>  <div class='ml-3 text-md font-normal'>Ürün zaten favorilerinizdedir.</div> <button @click='dismissed=true' type='button' class='ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700' data-dismiss-target='#toast-danger' aria-label='Close'><span class='sr-only'>Close</span><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg></button>",
                safe=False)
        except:
            # ürünü bulamazsa except kısmı çalışarak veritabanına favori kaydediyor.
            newFavItem = FavoriteModel.objects.create(customer_id=request.user.id, product_id=productId)
            newFavItem.save()
            request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
            return JsonResponse(
               "<div class='inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200'><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'></path></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-md font-normal'>Ürün Başarıyla Favorilerinize Eklenmiştir.</div><button @click='dismissed=true' type='button' class='ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700' data-dismiss-target='#toast-success' aria-label='Close'><span class='sr-only'>Close</span><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg></button>",
                safe=False)

    elif action == "remove":
        favItem = FavoriteModel.objects.get(customer_id=request.user.id, product_id=productId)
        favItem.delete()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return JsonResponse(
        "<div class='inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200'><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'></path></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-md font-normal'>Ürün Başarıyla Favorilerinizden Kaldırılmıştır.</div><button @click='dismissed=true' type='button' class='ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700' data-dismiss-target='#toast-success' aria-label='Close'><span class='sr-only'>Close</span><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg></button>",
        safe=False)


@login_required(login_url='login')
def deleteformfavories(request, id):
    FavoriteModel.objects.filter(id=id).delete()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    messages.success(request, 'Ürün Favorilerden silinmiştir.')
    return redirect('favories')


class MyOrdersView(LoginRequiredMixin,ListView):
    template_name       = "my-orders.html"
    context_object_name = "orders"
    paginate_by         = 5
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by("-created_date")
   


class OrderDetailView(DetailView):
    template_name       = "order-detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return OrderModel.objects.get(order_number=self.kwargs.get("order_number"))