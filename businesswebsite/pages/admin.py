from django.contrib import admin
from .models import Page
# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
    list_display = ('title','order')
