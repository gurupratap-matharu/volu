from places.models import Place, PlaceImage

from django.contrib import admin
from django.utils.html import format_html


class PlaceImageInlineAdmin(admin.TabularInline):
    model = PlaceImage
    readonly_fields = ('thumbnail',)


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
    autocomplete_fields = ('tags',)

    inlines = [PlaceImageInlineAdmin, ]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'place_name')
    readonly_fields = ('thumbnail',)
    search_fields = ('place__name',)
    raw_id_fields = ('place',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s"/>' % obj.thumbnail.url)
        return "-"
    thumbnail_tag.short_description = "Thumbnail"

    def place_name(self, obj):
        return obj.place.name
