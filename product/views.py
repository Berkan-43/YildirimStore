from django.shortcuts import render, get_object_or_404, redirect
from home.models import *
from product.models import *
from product.forms import *
from user.models import *
from order.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
# Create your views here.

def category_products(request, slug):
    global_categories = Category.objects.filter(id__range =(4,100))
    setting = Setting.objects.get(pk=1) 
    kategori = Category.objects.get(slug=slug)
    all_products = Product.objects.all()
    category_products = all_products.filter(productCategorie__slug=slug)
    product = Product.objects.filter(productCategorie__slug = slug)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        product = product.order_by('productPrice')
    elif sort_by == 'price_desc':
        product = product.order_by('-productPrice')
    else:
        product = product.order_by('-created_att')
        
    page = request.GET.get('page')
    paginator = Paginator(product, 3)  
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    
    
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'categories.html', context={
        'setting':setting,
        'product':product,
        'global_categories':global_categories,
        'favorites':favorites,
        'products':products,
        'total':total,
        'kategori':kategori,
        'category_products': category_products,
        # 'category': category,
        'category_products_count': category_products.count(),
        'all_products_count': all_products.count()
        # 'numbers': numbers
    })
def campaigns_products(request, slug):
    global_categories = Category.objects.filter(id__range =(4,100))
    setting = Setting.objects.get(pk=1) 
    kampanya = Campaigns.objects.get(slug=slug)
    product = Product.objects.filter(productCampaigns__slug = slug)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        product = product.order_by('productPrice')
    elif sort_by == 'price_desc':
        product = product.order_by('-productPrice')
    else:
        product = product.order_by('-created_att')
        
    page = request.GET.get('page')
    paginator = Paginator(product, 3)  
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    
    
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'categories.html', context={
        'setting':setting,
        'product':product,
        'global_categories':global_categories,
        'favorites':favorites,
        'products':products,
        'total':total,
        'kampanya':kampanya,
        # 'numbers': numbers
    })


def detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    product = get_object_or_404(Product, pk=id)
    is_order = OrderModel.objects.filter(user_id=request.user.id).exists()
    global_categories = Category.objects.filter(id__range =(4,100))
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    related_products = Product.objects.filter(productCategorie__slug=product.productCategorie.first().slug).exclude(id=id)
    related_comments = Comment.objects.filter(product_id__in=related_products.values_list('id', flat=True), status='True')

    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'detail.html', context={
        'setting':setting,
        'product':product,
        'images':images,
        'related_products':related_products,
        'favorites':favorites,
        'products':products,
        'total':total,
        'global_categories':global_categories,
        'is_order':is_order,
        'related_comments':related_comments,
        'comments':comments,
    })


def campaigns_detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    product = get_object_or_404(Product, pk=id)
    is_order = OrderModel.objects.filter(user_id=request.user.id).exists()
    global_categories = Category.objects.filter(id__range =(4,100))
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    related_products = Product.objects.filter(productCampaigns__slug=product.productCampaigns.first().slug).exclude(id=id)
    related_comments = Comment.objects.filter(product_id__in=related_products.values_list('id', flat=True), status='True')

    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'campaigns_detail.html', context={
        'setting':setting,
        'product':product,
        'images':images,
        'related_products':related_products,
        'favorites':favorites,
        'products':products,
        'total':total,
        'global_categories':global_categories,
        'is_order':is_order,
        'related_comments':related_comments,
        'comments':comments,
    })


@login_required(login_url='login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user  
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Yorumunuz Başarıyla Gönderilmiştir! Teşekkür Ederiz.')
            
            return HttpResponseRedirect(url)
    messages.warning(request, 'Yorum Yaparken Bir Sorunn Oluştu Lütfen Tekrar Deneyin.')
    return HttpResponseRedirect(url)   

@login_required(login_url='login')
def comments(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'coments.html', context={
        'comments':comments,
        'setting':setting,
        'favorites':favorites,
        'products':products,
        'total':total,
        'global_categories':global_categories,
    })
