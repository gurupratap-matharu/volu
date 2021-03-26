from django.contrib import admin

from places.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'email', 'city', 'country', 'is_active', 'ratings', 'host',)
    list_filter = ('is_active', 'created_on',)
    search_fields = ('name', 'email',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('ratings',)
    raw_id_fields = ('host',)
    date_hierarchy = 'created_on'
    ordering = ('is_active', 'country', 'city',)
