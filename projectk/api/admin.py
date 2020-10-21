from django.contrib import admin
from .models import *
# Register your models here.
class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('rating', )
    search_fields = ('id','rating', )

class SourceAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('source', )
    search_fields = ('id','source', )

class LicensorAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('name', )
    search_fields = ('id','name', )

class ProducerAdmin(admin.ModelAdmin):
    model = Producer
    list_display = ('name', )
    search_fields = ('id','name', )

class AnimeTypeAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ('type', )
    search_fields = ('id','type', )

class AlternativeTitleAdmin(admin.ModelAdmin):
    model = AlternativeTitle
    list_display = ('title', )
    search_fields = ('id','title', )

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    list_display = ('categorie', )
    search_fields = ('id','categorie', )

class StudioAdmin(admin.ModelAdmin):
    model = Studio
    list_display = ('name', )
    search_fields = ('id','name', )

class AnimeAdmin(admin.ModelAdmin):
    model = Anime
    list_display = ('name', 'aired', )
    filter_horizontal = ('categorie', 'producers', 'licensors', 'studio', 'alternative_title')
    search_fields = ('id','name', )

class DefaultAvatarAdmin(admin.ModelAdmin):
    model = DefaultAvatar
    list_display = ('tag',)
    search_fields = ('id', 'tag',)







admin.site.register(Rating, RatingAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Licensor, LicensorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(AnimeType, AnimeTypeAdmin)
admin.site.register(AlternativeTitle, AlternativeTitleAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Studio, StudioAdmin)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(AnimeStatus)
admin.site.register(Status)
admin.site.register(DefaultAvatar, DefaultAvatarAdmin)
admin.site.register(CustomList)


