from django.contrib import admin
from .models import BaseUser,Category,Expense,Group,GroupMember

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(BaseUser)
class BaseUser(BaseUserAdmin):
     fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (("Personal info"), {"fields": (
            "first_name", "last_name", "email", 'phone_number')}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
     
     add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'kind')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id','created_at', 'expense_date', 'created_by', 'category', 'description', 'amount')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'name')

@admin.register(GroupMember)
class GroupMember(admin.ModelAdmin):
    list_display = ('group', 'user')
