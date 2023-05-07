from django.shortcuts import render, redirect
from home.models import *
from home.forms import *
from product.models import *
from order.models import *
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.http import HttpResponse

FAKE_DB_CAROUSEL =[
    f"https://picsum.photos/id/{id}/1000/500" for id in range(0, 3)
]


def index(request):
    setting = Setting.objects.get(pk=1)

    category_list = Category.objects.all().order_by('id')[:3]
    global_categories = Category.objects.filter(id__range =(4,100))
    home_categories_left = Category.objects.filter(id='4')
    home_categories_right = Category.objects.filter(id='5')
    home_categories_center = Category.objects.filter(id__range =(6,7))

    super_deals = Product.objects.all().order_by('-id') # Süper fırsatlar

    just_came_all = Product.objects.filter(productCategorie__title =('Moda'))
    just_came_women = Product.objects.filter(productCategorie__title =('Kadın Giyim & Aksesuar'))
    just_came_man = Product.objects.filter(productCategorie__title =('Erkek Giyim & Aksesuar'))
    just_came_child = Product.objects.filter(productCategorie__title =('Çocuk Giyim & Aksesuar'))

    trending_products_all = Product.objects.filter(productCategorie__title =('Elektronik'))
    trending_products_computer = Product.objects.filter(productCategorie__title =('Bilgisayar'))
    trending_products_phone = Product.objects.filter(productCategorie__title =('Telefon & Aksesuarları'))
    trending_products_decor = Product.objects.filter(productCategorie__title =('Dekorasyon & Aydınlatma'))

    populer_products = Product.objects.filter(id__range =(64,85))
    special_offer = Product.objects.all().order_by('-id')[:2]

    campaigns = Campaigns.objects.filter(id__range =(4,12))
    campaigns1 = Campaigns.objects.filter(id__range =(1,3))
    campaigns2 = Campaigns.objects.filter(id__range =(13,25))

    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    context = dict(
        setting = setting,
        category_list = category_list,
        global_categories = global_categories,
        campaigns1 = campaigns1,

        just_came_all = just_came_all,
        just_came_women = just_came_women,
        just_came_man = just_came_man,
        just_came_child = just_came_child,

        trending_products_all = trending_products_all,
        trending_products_computer = trending_products_computer,
        trending_products_phone = trending_products_phone,
        trending_products_decor = trending_products_decor,

        special_offer = special_offer,
        campaigns = campaigns,
        campaigns2=campaigns2,
        populer_products = populer_products,
        super_deals = super_deals,
        FAKE_DB_CAROUSEL = FAKE_DB_CAROUSEL,
        products = products,
        total = total,
        favorites = favorites,
        home_categories_left = home_categories_left,
        home_categories_right = home_categories_right,
        home_categories_center = home_categories_center,
        # images = images,
    )
    return render(request, 'index.html', context)

class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']

        mail = EmailMessage(
            f'{name}, Tarafından Mesaj Gönderildi',
            f'Konu: {subject}\n\nEmail: {email}\n\nMesaj: {message}\n\n',
            f'"YENİ MESAJ" <{email}>',
            [settings.EMAIL_ADMIN], 
                reply_to=[f'{email}'], 
        )
        mail.send()
        form.save()
        success = "<div class='flex items-center w-full fixed top-10 right-5  max-w-md p-4 mb-4 text-gray-500 bg-white rounded-lg dark:text-gray-400 dark:bg-gray-800'><div id='toast-success' class='flex items-center w-full fixed top-10 right-5  max-w-md p-4 mb-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800' role='alert'><div class='inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200'><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'></path></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-md font-normal'>Mesajınız Başarıyla Gönderildi</div><button type='button' class='ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700' data-dismiss-target='#toast-success' aria-label='Close'><span class='sr-only'>Close</span><svg aria-hidden='true' class='w-5 h-5' fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd'></path></svg></button></div></div>" + '' + name
        return HttpResponse(success)


def referance(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'referance.html', context={
        'setting': setting,
        'products': products,
        'total': total,
        'favorites': favorites,
        'category_list': global_categories,
        })


def about(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'about.html', context={
        'setting': setting,
        'products': products,
        'total': total,
        'favorites': favorites,
        'category_list': global_categories,
        })

# Search
def search_product(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    register_form=CustomUserCreationForm()
    login_form = UserLoginForm()
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()

    productsearch = Product.objects.all()
    query = ''
    if request.method == 'GET':
        query = request.GET.get('query')
        productsearch = productsearch.filter(
            Q(productTitle__icontains=query) |
            Q(productCategorie__title__icontains=query) |
            Q(productTag__title__icontains=query) |
            Q(productDescription__icontains=query)
            ).distinct()
    return render(request, 'search.html', context={
        'productsearch':productsearch,
        'query':query,
        'setting':setting,
        'global_categories': global_categories,
        'register_form':register_form,
        'login_form':login_form,
        'products':products,
        'total':total,
        'favorites':favorites,
    })


def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


# def handler404(request, exception):
#     setting = Setting.objects.get(pk=1)
#     global_categories = Category.objects.filter(id__range =(4,100))
#     register_form=CustomUserCreationForm()
#     login_form = UserLoginForm()
#     favorites = FavoriteModel.objects.filter(customer=request.user.id)
#     products = CartModel.objects.filter(user=request.user.id)
#     total = 0
#     for product_ in products:
#         total += product_.amount * product_.product.productPrice
#     request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
#     request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
#     return render(request, '404.html', context={
#         'global_categories': global_categories,
#         'setting':setting,
#         'register_form':register_form,
#         'login_form':login_form,
#         'products':products,
#         'total':total,
#         'favorites':favorites,
#     }, status=404) 


def faq(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(4,100))
    register_form=CustomUserCreationForm()
    login_form = UserLoginForm()
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(user=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(user_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'faq.html', context={
        'global_categories': global_categories,
        'setting':setting,
        'register_form':register_form,
        'login_form':login_form,
        'products':products,
        'total':total,
        'favorites':favorites,
    })



