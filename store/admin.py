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


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
    ]
    list_per_page = 10
    ordering = [
        "user__last_name",
        "user__first_name",
    ]
    search_fields = [
        "user__first_name__istartswith",
        "user__last_name__istartswith",
    ]

    def first_name(self, customer):
        return customer.user.first_name

    def last_name(self, customer):
        return customer.user.last_name

    def email(self, customer):
        return customer.user.email
