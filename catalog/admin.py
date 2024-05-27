from django.contrib import admin
from .models import Profile, Car, CarInstance,Rating


# admin.site.register(Profile)
admin.site.register(CarInstance)
#admin.site.register(Car)
admin.site.register(Rating)

@admin.register(Car)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('model',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('user', 'slug')
    list_display_links = ('user', 'slug')



