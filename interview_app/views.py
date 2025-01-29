from rest_framework import generics, filters
from .models import *
from .serializers import (
    EmployeeSerializer,
    MembershipSerializer,
    CustomerSerializer,
    ShipmentSerializer,
    PaymentSerializer,
    StatusSerializer,
    EmployeeManagesShipmentSerializer,
)

# Create your views here.


# Employee
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Membership
class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


# Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["Cust_NAME"]


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# Shipment
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["SD_CHARGES"]


class ShipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


# Payment
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Status
class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


# EmployeeManagesShipment - EMS
class EmployeeManagesShipmentListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer


class EmployeeManagesShipmentRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer
