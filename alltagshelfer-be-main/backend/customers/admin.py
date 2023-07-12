# customers/admin.py

from django.contrib import admin
from .models import Customer, CustomerFieldValue, CustomerFieldListVisibility
from core.admin import AutomaticAuthorMixin

fields_display = ['salutation', 'lastname', 'firstname', 'id', 'city',
                  'birthday', 'deleted']
fields_filter = fields_display


class CustomerFieldValueInline(admin.TabularInline):
    model = CustomerFieldValue
    # Number of pre-set fields in admin for a new instance
    extra = 0
    exclude = ('author',)


class UserFieldListVisibilityAdmin(admin.ModelAdmin):
    list_display = ('fieldname', 'visible', 'user')
    list_filter = ('fieldname', 'visible', 'user')


class CustomerAdmin(AutomaticAuthorMixin):
    list_display = fields_display
    search_fields = fields_filter

    def get_custom_fields(self, obj):
        return "\n".join([p.name for p in obj.custom_fields.all()])

    inlines = [CustomerFieldValueInline]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerFieldListVisibility, UserFieldListVisibilityAdmin)
