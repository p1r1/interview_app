from django.shortcuts import get_object_or_404
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


# region CUSTOM END POINTS
# customer>shipment
class CustomerShipmentDetailsView(generics.RetrieveAPIView):
    serializer_class = CustomerShipmentSerializer

    def get_object(self):
        rec_id = self.kwargs.get("rec_id")
        return get_object_or_404(Customer, rec_id=rec_id)

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EMSStatusDeailView(generics.RetrieveAPIView):
    serializer_class = EMSStatusSerializer

    def get_object(self):
        rec_id = self.kwargs.get("rec_id")
        return get_object_or_404(EmployeeManagesShipment, rec_id=rec_id)

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DeliveredShipmentListView(generics.ListAPIView):
    serializer_class = DeliveredShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.filter(
            employeemanagesshipment__Status_Sh_ID__Current_Status="DELIVERED"
        ).prefetch_related("employeemanagesshipment_set__Status_Sh_ID")

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# endregion
