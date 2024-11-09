from django.contrib import admin

from . import models


class ProductImagesAdmin(admin.TabularInline):
    model = models.ProductImages


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [
        "title",
        "product_image",
        "price",
        "status",
        "datetime_created",
    ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category_image",
        "datetime_created",
    ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Brand)
class BarndAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "brand_image",
    ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = [
        "color_name",
        "color_code",
    ]
