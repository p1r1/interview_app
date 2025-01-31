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
    """
    Custom exception class to provide consistent error responses.
    """

    def __init__(self, detail, status_code):
        # Status code for the response
        self.status_code = status_code
        self.detail = detail


# helper function for try excepts
def handle_exceptions(func):
    """
    Decorator to handle exceptions in views.
    """

    def wrapper(*args, **kwargs):
        """Wrapper function for try except block."""
        try:
            # Executes the wrapped function
            return func(*args, **kwargs)
        except (IntegrityError, DatabaseError) as e:  # Catches database related errors
            logger.error(f"Database error: {e}")
            raise CustomAPIException(  # Raises a custom exception with error message
                detail="A database error occurred.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:  # Catches all other exceptions.
            logger.exception(f"An unexpected error occurred: {e}")
            raise CustomAPIException(  # Raises a custom exception with error message
                detail="An unexpected server error occurred.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper


# Employee
class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Employee objects.
    """

    # Get all Employee objects from the database
    queryset = Employee.objects.all()
    # Use the EmployeeSerializer for serialization
    serializer_class = EmployeeSerializer

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions  # Handles all exceptions
    def dispatch(self, *args, **kwargs):
        """Dispatches requests to the appropriate handler."""
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        """Handles POST request for Employee creation"""
        return super().create(request, *args, **kwargs)


class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Employee object.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def get(self, request, *args, **kwargs):
        """Handles GET requests and provides caching for a single Employee."""
        return super().get(request, *args, **kwargs)

    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        """Handles GET request to retrive a single object"""
        return super().retrieve(request, *args, **kwargs)

    @handle_exceptions
    def update(self, request, *args, **kwargs):
        """Handles PUT/PATCH requests to update a single object"""
        return super().update(request, *args, **kwargs)

    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        """Handles DELETE request to delete a single object"""
        return super().destroy(request, *args, **kwargs)


# Membership
class MembershipListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating Membership objects.
    """

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
    """
    View for retrieving, updating, and deleting a single Membership object.
    """

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
    """
    View for listing and creating Customer objects.
    """

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
    """
    View for retrieving, updating, and deleting a single Customer object.
    """

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
    """
    View for listing and creating Shipment objects.
    """

    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [filters.OrderingFilter]  # Enable ordering filter
    ordering_fields = ["SH_CHARGES"]  # Specifies the field for ordering

    # To make the cache middleware catch dispatch methods instead of get methods, we are ading method_decorator here.
    @method_decorator(cache_page(settings.CACHE_TTL_SECONDS))
    @handle_exceptions
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @handle_exceptions
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ShipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single Shipment object.
    """

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
    """
    View for listing and creating Payment objects.
    """

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
    """
    View for retrieving, updating, and deleting a single Payment object.
    """

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
    """
    View for listing and creating Status objects.
    """

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
    """
    View for retrieving, updating, and deleting a single Status object.
    """

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
    """
    View for listing and creating EmployeeManagesShipment objects.
    """

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
    """
    View for retrieving, updating, and deleting a single EmployeeManagesShipment object.
    """

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
    """
    View for retrieving customer details along with their associated shipments.
    """

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
    """
    View for retrieving EmployeeManagesShipment details with Status details.
    """

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
    """
    View for listing all delivered shipments.
    """

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
    """
    View for listing all non-delivered shipments.
    """

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
    """
    View for retrieving shipment details along with their associated customer.
    """

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
