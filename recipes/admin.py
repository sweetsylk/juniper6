from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin configuration for User model."""

    list_display = ("username","email","first_name","last_name","is_active","is_staff")
    search_fields = ("username","email","first_name","last_name")
    list_filter =("is_active","is_staff","is_superuser")

    readonly_fields = ("last_login","date_joined")
    ordering = ("last_name","first_name")

    actions = ["ban_users","unban_users"]

    @admin.action(description="Ban selected users")
    def ban_users(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Unban selected users")
    def unban_users(self, request, queryset):
        queryset.update(is_active=True)

    fieldsets = (
    ("Personal Information", {
        "fields": ("username", "first_name", "last_name", "email")
    }),
    ("Permissions", {
        "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
    }),
    ("Important Dates", {
        "fields": ("last_login", "date_joined")
    }),
)
    
admin.site.site_header = "Juniper-6 Admin Panel"
admin.site.site_title = "Juniper-6 Backend Admin"
admin.site.index_title = "Welcome to the Juniper-6 Administration Dashboard"
