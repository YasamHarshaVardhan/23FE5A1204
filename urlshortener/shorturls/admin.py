from django.contrib import admin
from .models import ShortURL, Click

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("shortcode", "original_url", "created_at", "expiry", "clicks")
    search_fields = ("shortcode", "original_url")

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ("shorturl", "timestamp", "referrer", "location")
    search_fields = ("shorturl__shortcode", "referrer", "location")
