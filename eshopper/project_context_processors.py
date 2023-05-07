from product.models import Category
from home.models import Setting
from user.forms import CustomUserCreationForm, UserLoginForm

def global_category_context(request):
    return dict(
        global_categories = Category.objects.filter(id__range =(4,100))
    )

def global_setting_context(request):
    return dict(
        global_settings=Setting.objects.all()
    )

def global_login_form_context(request):
    return {"login_form":UserLoginForm()}
        

def global_register_form_context(request):
    return {"register_form":CustomUserCreationForm()}
        
    