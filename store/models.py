from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class Color(models.Model):
    color_name = models.CharField(max_length=30, verbose_name=_("color_name"))
    color_code = models.CharField(max_length=30, verbose_name=_("color_code"))

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.color_name


class Brand(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("title"), default="Apple")
    slug = models.SlugField(
        max_length=255, verbose_name=_("slug"), unique=True, allow_unicode=True
    )
    english_title = models.CharField(
        max_length=50, verbose_name=_("english title"), default="Apple"
    )
    image = models.ImageField(
        upload_to="brand",
        verbose_name=_("image"),
    )

    def brand_image(self):
        try:
            return format_html(
                "<img width=50 height=50 src='{}'>".format(self.image.url)
            )
        except:
            return ""

    class Meta:
        verbose_name = _("Barnd")
        verbose_name_plural = _("Barnds")

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        verbose_name=_("parent"),
        on_delete=models.SET_NULL,
        related_name="child",
    )
    title = models.CharField(max_length=255, verbose_name=_("title"))
    english_title = models.CharField(
        max_length=255, verbose_name=_("english title"), blank=True
    )
    slug = models.SlugField(
        max_length=255, verbose_name=_("slug"), unique=True, allow_unicode=True
    )
    image = models.ImageField(
        upload_to="category", verbose_name=_("image"), blank=True, null=True
    )
    cover = models.ImageField(
        upload_to="category", verbose_name=_("cover"), blank=True, null=True
    )
    is_parent = models.BooleanField(
        default=False, blank=True, null=True, verbose_name=_("is_parent")
    )
    is_offer = models.BooleanField(
        default=False, blank=True, null=True, verbose_name=_("is offer")
    )

    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("datetime created")
    )

    def category_image(self):
        try:
            return format_html(
                "<img width=50 height=50 src='{}'>".format(self.image.url)
            )
        except:
            return ""

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS = {
        ("draft", "Draft"),
        ("in_review", "In Review"),
        ("published", "Published"),
    }
    title = models.CharField(_("product"), max_length=255)
    english_title = models.CharField(
        max_length=255, verbose_name=_("english title"), null=True, blank=True
    )
    slug = models.SlugField(
        max_length=255, verbose_name=_("slug"), unique=True, allow_unicode=True
    )
    category = models.ManyToManyField(
        Category, verbose_name=_("category"), related_name="products"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("brand"),
        related_name="products",
    )
    color = models.ManyToManyField(
        Color, verbose_name=_("color"), related_name="products"
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name=_("image"),
    )
    description = models.TextField(_("description"))
    price = models.PositiveBigIntegerField(verbose_name=_("price"))
    old_price = models.PositiveBigIntegerField(verbose_name=_("old_price"))
    status = models.CharField(
        choices=STATUS,
        max_length=10,
        verbose_name=_("status"),
        default="in_review",
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("datetime created")
    )
    datetime_modified = models.DateTimeField(
        auto_now=True, verbose_name=_("datetime modified")
    )

    def product_image(self):
        try:
            return format_html(
                "<img width=60 height=60 src='{}'>".format(self.image_1.url)
            )
        except:
            return ""

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_precentage(self):
        new_price = 100 - ((self.price / self.old_price) * 100)
        return new_price

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-image", verbose_name=_("images"))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="product_images",
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("datetime created")
    )

    class Meta:
        verbose_name = _("ProductImage")
        verbose_name_plural = _("ProductImages")


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.PROTECT
    )
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Address(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True, verbose_name=_("customer")
    )
    province = models.CharField(max_length=255, verbose_name=_("province"))
    city = models.CharField(max_length=255, verbose_name=_("city"))
    street = models.CharField(max_length=255, verbose_name=_("street"))
    postal_code = models.CharField(_("postal_code"), max_length=50)

    class Meta:
        verbose_name = _("Addresse")
        verbose_name_plural = _("Addresses")
