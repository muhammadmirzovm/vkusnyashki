from django.contrib import admin
from .models import Monitor, Category, Food


class FoodInline(admin.TabularInline):
    model = Food
    extra = 0
    fields = ("name", "price", "is_available")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "monitor", "order")
    list_filter = ("monitor",)
    inlines = [FoodInline]


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category__monitor", "is_available")
    search_fields = ("name",)
