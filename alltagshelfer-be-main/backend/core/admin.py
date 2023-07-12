# core/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FieldType, FieldMetadata, CompanySite


class AutomaticAuthorMixin(admin.ModelAdmin):
    """
    Automatically sets current user as "Author" of new instance in django admin
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(AutomaticAuthorMixin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ("author",)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["author"] = request.user
        request.GET = data
        return super(AutomaticAuthorMixin, self).add_view(
            request, form_url="", extra_context=extra_context
        )


class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'data_type', 'input_type']


class FieldMetaAdmin(AutomaticAuthorMixin):
    list_display = ['id', 'title', 'kind', 'field_type',
                    'placeholder', 'enums', 'position', 'required']


class CompanySiteAdmin(admin.ModelAdmin):
    list_display = ['street', 'house_number', 'city']


admin.site.register(FieldType, FieldTypeAdmin)
admin.site.register(FieldMetadata, FieldMetaAdmin)
admin.site.register(CompanySite, CompanySiteAdmin)
