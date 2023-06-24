from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "user"
    ]  # Enables the autocomplete feature for the 'user' field
    search_fields = ["id", "user_id", "actor__email"]


admin.site.register(Account, AccountAdmin)


# Register the User model to display the user information in the autocomplete field
class UserAccount(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("OpenToilet Account Info", {"fields": ("account",)}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAccount)
