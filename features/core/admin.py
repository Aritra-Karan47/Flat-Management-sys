from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Society, User, AuditLog

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at']

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'phone', 'society', 'is_admin', 'is_resident', 'date_joined']
    list_filter = ['is_admin', 'society']
    fieldsets = UserAdmin.fieldsets + (
        ('Society Info', {'fields': ('phone', 'society', 'is_admin', 'is_resident')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(AuditLog)