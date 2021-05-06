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

class StreamSourceAdmin(admin.ModelAdmin):
    model = StreamSource
    list_display = ('id', )
    search_fields = ('id', )

class SeasonNumberAdmin(admin.ModelAdmin):
    model = SeasonNumber
    list_display = ('tag', )
    search_fields = ('id','tag', )

class AnimeAdmin(admin.ModelAdmin):
    model = Anime
    ordering = ('-id',)
    date_hierarchy = 'aired'
    list_display = ('name', 'aired',)
    filter_horizontal = ('categorie', 'producers', 'licensors', 'studio', 'alternative_title')
    search_fields = ('id', 'name', 'aired__day')

class AnimeStatusAdmin(admin.ModelAdmin):
    model       = AnimeStatus
    ordering    = ("-date")
    date_hierarchy = 'date'
    list_display = ('id', 'date',)
    search_fields = ('id', 'user__username',)

class DefaultAvatarAdmin(admin.ModelAdmin):
    model = DefaultAvatar
    list_display = ('tag',)
    search_fields = ('id', 'tag',)

class StreamServiceAdmin(admin.ModelAdmin):
    model = DefaultAvatar
    list_display = ('id',)
    search_fields = ('id', 'name',)

class ReportMotiveAdmin(admin.ModelAdmin):
    model = ReportMotive
    list_display = ('motive', 'id')
    search_fields = ('id', 'motive',)

class ReportSectionAdmin(admin.ModelAdmin):
    model = ReportSection
    list_display = ('type', 'pid')
    search_fields = ('id', 'pid', 'type')







admin.site.register(Rating, RatingAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Licensor, LicensorAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(AnimeType, AnimeTypeAdmin)
admin.site.register(AlternativeTitle, AlternativeTitleAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Studio, StudioAdmin)
admin.site.register(StreamSource, StreamSourceAdmin)
admin.site.register(SeasonNumber, SeasonNumberAdmin)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(AnimeStatus)
admin.site.register(Status)
admin.site.register(DefaultAvatar, DefaultAvatarAdmin)
admin.site.register(CustomList)
admin.site.register(DateOption)
admin.site.register(ReportMotive, ReportMotiveAdmin)
admin.site.register(ReportSection, ReportSectionAdmin)


