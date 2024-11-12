from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Address, Customer
from .serializers import AddressSerializer, CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "my_addresses":
            return AddressSerializer
        return CustomerSerializer

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET", "POST"],
        url_path="me/addresses",
        permission_classes=[IsAuthenticated],
    )
    def my_addresses(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)

        if request.method == "GET":
            addresses = customer.addresses.all()
            serializer = AddressSerializer(addresses, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = AddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=customer)
            return Response(serializer.data, status=201)


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            customer_pk = self.kwargs.get("customer_pk", None)
            if customer_pk:
                return Address.objects.filter(customer_id=customer_pk)
            return Address.objects.none()

    def get_serializer_context(self):
        return {"customer_pk": self.kwargs.get("customer_pk")}
