from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("customers", viewset=views.CustomerViewSet, basename="customer")

urlpatterns = router.urls
