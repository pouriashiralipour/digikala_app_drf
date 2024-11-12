from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("customers", viewset=views.CustomerViewSet, basename="customer")

customer_addresses_router = routers.NestedDefaultRouter(
    router, "customers", lookup="customer"
)
customer_addresses_router.register(
    "addresses", viewset=views.AddressViewSet, basename="customer-address"
)

urlpatterns = router.urls + customer_addresses_router.urls
