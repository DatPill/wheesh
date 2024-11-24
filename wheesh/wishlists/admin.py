from django.contrib import admin

from .models import Present, Wishlist


@admin.register(Present)
class PresentAdmin(admin.ModelAdmin):
    list_display = ('title', 'wishlist', 'user')
    search_fields = ('title', 'user__username')
    fields = (('title', 'user'), 'description', 'image', 'link', 'price', 'reserved_by', 'wishlist')


class PresentInlineAdmin(admin.TabularInline):
    model = Present
    fk_name = 'wishlist'
    fields = ('title', 'reserved_by')


@admin.register(Wishlist)
class WishlistInline(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'user__username')
    fields = (('title', 'user'), 'image', 'event_date')
    inlines = (PresentInlineAdmin,)


class WishlistInlineAdmin(admin.TabularInline):
    model = Wishlist
    fields = ('title', 'event_date')
