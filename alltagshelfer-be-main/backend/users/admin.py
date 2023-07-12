# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserFieldValue, UserFieldListVisibility
from core.admin import AutomaticAuthorMixin


"""
USERS
"""


class UserFieldValueInline(admin.TabularInline):
    model = UserFieldValue
    # Number of pre-set fields in admin for a new instance
    extra = 0
    exclude = ('author',)


class UserFieldListVisibilityAdmin(admin.ModelAdmin):
    list_display = ('fieldname', 'visible', 'user')
    list_filter = ('fieldname', 'visible', 'user')


class UserAdmin(AutomaticAuthorMixin, UserAdmin):

    filter_horizontal = []

    list_display = ('username', 'id', 'role', 'deleted')
    list_filter = ('role', 'deleted',)

    def get_custom_fields(self, obj):
        return "\n".join([p.title for p in obj.custom_fields.all()])

    inlines = [UserFieldValueInline]

    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = [
        ('Allgemein', {'fields': ('username', 'password', 'role',
         'companysite', 'is_superuser', 'invalidate_before')}),
        ('Stammdaten', {'fields': ('salutation', 'lastname', 'firstname',
                                   'street', 'house_number', 'city', 'zip',
         'address_addition', 'phone_mobile', 'phone_house', 'birthday',
                                   'email', 'comments')}),
        ('Infos', {'fields': ('last_login', 'date_joined',
         'author', 'deleted', 'deleted_at')}),
    ]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserFieldListVisibility, UserFieldListVisibilityAdmin)
