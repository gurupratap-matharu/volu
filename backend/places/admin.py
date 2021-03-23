from django.contrib import admin

from places.models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'country', 'is_active', 'ratings', 'host',)
    list_filter = ('is_active', 'created_on',)
    search_fields = ('name', 'email',)
    list_editable = ('is_active',)
    readonly_fields = ('ratings',)
    raw_id_fields = ('host',)
    date_hierarchy = 'created_on'
    ordering = ('is_active', 'country', 'city',)


admin.site.register(Place, PlaceAdmin)
