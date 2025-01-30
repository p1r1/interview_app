from django.urls import path
from .views import *

urlpatterns = [
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list"),
    path(
        "employees/<int:pk>/",
        EmployeeRetrieveUpdateDestroyView.as_view(),
        name="employee-detail",
    ),
    path("memberships/", MembershipListCreateView.as_view(), name="membership-list"),
    path(
        "memberships/<int:pk>/",
        MembershipRetrieveUpdateDestroyView.as_view(),
        name="membership-detail",
    ),
    path("customers/", CustomerListCreateView.as_view(), name="customer-list"),
    path(
        "customers/<int:pk>/",
        CustomerRetrieveUpdateDestroyView.as_view(),
        name="customer-detail",
    ),
    path("shipments/", ShipmentListCreateView.as_view(), name="shipment-list"),
    path(
        "shipments/<int:pk>/",
        ShipmentRetrieveUpdateDestroyView.as_view(),
        name="shipment-detail",
    ),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path(
        "payments/<str:pk>/",
        PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
    path("statuses/", StatusListCreateView.as_view(), name="status-list"),
    path(
        "statuses/<int:pk>/",
        StatusRetrieveUpdateDestroyView.as_view(),
        name="status-detail",
    ),
    path(
        "employeemanagesshipments/",
        EmployeeManagesShipmentListCreateView.as_view(),
        name="employeemanagesshipment-list",
    ),
    path(
        "employeemanagesshipments/<int:pk>/",
        EmployeeManagesShipmentRetrieveUpdateDestroyView.as_view(),
        name="employeemanagesshipment-detail",
    ),
    # custom enpoints
    path(
        "customers/<int:rec_id>/shipments/",
        CustomerShipmentDetailsView.as_view(),
        name="customer-shipment-details",
    ),
    path(
        "employeemanagesshipments/<int:rec_id>/status/",
        EMSStatusDeailView.as_view(),
        name="employeemanagesshipments-status-details",
    ),
    path(
        "shipments/delivered/",
        DeliveredShipmentListView.as_view(),
        name="delivered-shipment-list",
    ),
]
