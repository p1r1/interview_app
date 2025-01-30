from rest_framework import generics, filters
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

# Create your views here.


# Employee
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Membership
class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


# Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["C_NAME"]

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# Shipment
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["SD_CHARGES"]

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ShipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


# Payment
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Status
class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


# EmployeeManagesShipment - EMS
class EmployeeManagesShipmentListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EmployeeManagesShipmentRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer
