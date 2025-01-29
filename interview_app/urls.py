from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.EmployeeListCreateView.as_view(), name="employee-list"),
    path(
        "employees/<int:pk>/",
        views.EmployeeRetrieveUpdateDestroyView.as_view(),
        name="employee-detail",
    ),
    path(
        "memberships/", views.MembershipListCreateView.as_view(), name="membership-list"
    ),
    path(
        "memberships/<int:pk>/",
        views.MembershipRetrieveUpdateDestroyView.as_view(),
        name="membership-detail",
    ),
    path("customers/", views.CustomerListCreateView.as_view(), name="customer-list"),
    path(
        "customers/<int:pk>/",
        views.CustomerRetrieveUpdateDestroyView.as_view(),
        name="customer-detail",
    ),
    path("shipments/", views.ShipmentListCreateView.as_view(), name="shipment-list"),
    path(
        "shipments/<int:pk>/",
        views.ShipmentRetrieveUpdateDestroyView.as_view(),
        name="shipment-detail",
    ),
    path("payments/", views.PaymentListCreateView.as_view(), name="payment-list"),
    path(
        "payments/<str:pk>/",
        views.PaymentRetrieveUpdateDestroyView.as_view(),
        name="payment-detail",
    ),
    path("statuses/", views.StatusListCreateView.as_view(), name="status-list"),
    path(
        "statuses/<int:pk>/",
        views.StatusRetrieveUpdateDestroyView.as_view(),
        name="status-detail",
    ),
    path(
        "employeemanagesshipments/",
        views.EmployeeManagesShipmentListCreateView.as_view(),
        name="employeemanagesshipment-list",
    ),
    path(
        "employeemanagesshipments/<int:pk>/",
        views.EmployeeManagesShipmentRetrieveUpdateDestroyView.as_view(),
        name="employeemanagesshipment-detail",
    ),
]
