from django import forms
from django.contrib import admin

from .models import Food


class FoodAdminForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe your dish briefly (max 120 characters)",
                    "rows": 3,
                    "maxlength": 120,
                }
            ),
        }


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    form = FoodAdminForm
    list_display = ("name", "price", "is_available")
    search_fields = ("name",)
    list_filter = ("is_available",)
