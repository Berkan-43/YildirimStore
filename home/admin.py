from django.contrib import admin
from home.models import *
# Register your models here.

admin.site.register(Setting)

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'create_at', 'note', 'subject', 'status']

    readonly_fields = [
        'name', 'email', 'note', 'subject', 'message', 'ip', 'create_at'
    ]

    fieldsets =(
        ("MESAJLAR", {
            'fields': ("name", "email", "subject", "message", "create_at")
    }),
    )
    list_filter = ['status', "subject"]
    
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False