from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
import logging
from rest_framework.exceptions import APIException
from django.db import IntegrityError, DatabaseError

# Create your views here.
logger = logging.getLogger(__name__)


# Custom Exception
class CustomAPIException(APIException):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        self.detail = detail


# helper function for try excepts
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IntegrityError, DatabaseError) as e:
            logger.error(f"Database error: {e}")
            raise CustomAPIException(
                detail="A database error occurred.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            raise CustomAPIException(
                detail="An unexpected server error occurred.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper


# Employee
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Membership
class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["C_NAME"]

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Shipment
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["SH_CHARGES"]

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ShipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Payment
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Status
class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# EmployeeManagesShipment - EMS
class EmployeeManagesShipmentListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class EmployeeManagesShipmentRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = EmployeeManagesShipment.objects.all()
    serializer_class = EmployeeManagesShipmentSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# region CUSTOM END POINTS
# customer>shipment
class CustomerShipmentDetailsView(generics.RetrieveAPIView):
    serializer_class = CustomerShipmentSerializer

    @handle_exceptions
    def get_object(self):
        rec_id = self.kwargs.get("rec_id")
        return get_object_or_404(Customer, rec_id=rec_id)

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EMSStatusDeailView(generics.RetrieveAPIView):
    serializer_class = EMSStatusSerializer

    @handle_exceptions
    def get_object(self):
        rec_id = self.kwargs.get("rec_id")
        return get_object_or_404(EmployeeManagesShipment, rec_id=rec_id)

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DeliveredShipmentListView(generics.ListAPIView):
    serializer_class = DeliveredShipmentSerializer

    @handle_exceptions
    def get_queryset(self):
        return Shipment.objects.filter(
            employeemanagesshipment__Status_Sh_ID__Current_Status="DELIVERED"
        ).prefetch_related("employeemanagesshipment_set__Status_Sh_ID")

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NotDeliveredShipmentListView(generics.ListAPIView):
    serializer_class = DeliveredShipmentSerializer

    @handle_exceptions
    def get_queryset(self):
        return Shipment.objects.filter(
            employeemanagesshipment__Status_Sh_ID__Current_Status="NOT DELIVERED"
        ).prefetch_related("employeemanagesshipment_set__Status_Sh_ID")

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ShipmentCustomerDetailView(generics.RetrieveAPIView):
    serializer_class = ShipmentCustomerSerializer

    @handle_exceptions
    def get_object(self):
        rec_id = self.kwargs.get("rec_id")
        return get_object_or_404(Shipment, rec_id=rec_id)

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# endregion
