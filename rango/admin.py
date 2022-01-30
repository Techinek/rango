from django.contrib import admin

from .models import Category, Page


class PageAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'category', 'views')
    list_display = ('title', 'category', 'url')


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
