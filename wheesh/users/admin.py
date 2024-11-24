from django.contrib import admin
from users.models import User
from wishlists.admin import WishlistInlineAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    inlines = (WishlistInlineAdmin,)
