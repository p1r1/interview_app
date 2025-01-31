from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from oauth2_provider.models import Application
from datetime import date
from .models import *
from interview_app.serializers import *
from django.core.cache import cache
from unittest.mock import patch

# Create your tests here.


# region model test
class ModelTests(TestCase):
    def setUp(self):
        # Create test data
        self.employee = Employee.objects.create(
            E_ID=1,
            E_NAME="John Doe",
            E_BRANCH="Main",
            E_DESIGNATION="Manager",
            E_ADDR="123 Street",
            E_CONT_NO=1234567890,
        )

        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )

        self.customer = Customer.objects.create(
            C_ID=1,
            C_NAME="Test Customer",
            C_EMAIL_ID="test@example.com",
            C_CONT_NO=9876543210,
            C_ADDR="456 Avenue",
            C_TYPE="Regular",
            M_ID=self.membership,
        )

        self.shipment = Shipment.objects.create(
            SH_ID=1,
            C_ID=self.customer,
            SH_CONTENT="Test Content",
            SH_DOMAIN="Domestic",
            SER_TYPE="Express",
            SH_WEIGHT="5kg",
            SH_CHARGES=100,
            SR_ADDR="Source Address",
            DS_ADDR="Destination Address",
        )

        self.payment = Payment.objects.create(
            Payment_ID="313cd69e-66f3-11ea-9879-7077813058ce",
            C_ID=self.customer,
            SH_ID=self.shipment,
            AMOUNT=49302,
            Payment_Status="PAID",
            Payment_Mode="CARD PAYMENT",
            Payment_Date=date(2014, 12, 18),
        )

        self.status = Status.objects.create(
            SH_ID=self.shipment.SH_ID,
            Current_Status="DELIVERED",
            Sent_date=date(2024, 1, 1),
            Delivery_date=date(2024, 1, 2),
        )

        self.ems = EmployeeManagesShipment.objects.create(
            Employee_E_ID=self.employee,
            Shipment_Sh_ID=self.shipment,
            Status_Sh_ID=self.status,
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), "John Doe (Manager)")

    def test_membership_str(self):
        self.assertEqual(str(self.membership), "Membership: 1")

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Test Customer (Regular)")

    def test_shipment_str(self):
        self.assertEqual(str(self.shipment), "Shipment 1")

    def test_payment_str(self):
        self.assertEqual(
            str(self.payment), "Payment 313cd69e-66f3-11ea-9879-7077813058ce"
        )

    def test_status_str(self):
        self.assertEqual(str(self.status), "Status 1")

    def test_employee_manages_shipment_str(self):
        self.assertEqual(
            str(self.ems), "Employee John Doe (Manager) manages shipment Shipment 1"
        )


# endregion


# region serializer test
class SerializerTests(TestCase):
    def setUp(self):
        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )
        self.customer = Customer.objects.create(
            C_ID=1,
            C_NAME="Test Customer",
            C_EMAIL_ID="test@example.com",
            C_CONT_NO=9876543210,
            C_ADDR="456 Avenue",
            C_TYPE="Regular",
            M_ID=self.membership,
        )
        self.shipment = Shipment.objects.create(
            SH_ID=1,
            C_ID=self.customer,
            SH_CONTENT="Test Content",
            SH_DOMAIN="Domestic",
            SER_TYPE="Express",
            SH_WEIGHT="5kg",
            SH_CHARGES=100,
            SR_ADDR="Source Address",
            DS_ADDR="Destination Address",
        )
        self.status = Status.objects.create(
            SH_ID=self.shipment.SH_ID,
            Current_Status="DELIVERED",
            Sent_date=date(2024, 1, 1),
            Delivery_date=date(2024, 1, 2),
        )
        self.employee = Employee.objects.create(
            E_ID=1,
            E_NAME="John Handler",
            E_BRANCH="Main",
            E_DESIGNATION="Handler",
            E_ADDR="Handler Address",
            E_CONT_NO=1234567890,
        )
        self.ems = EmployeeManagesShipment.objects.create(
            Employee_E_ID=self.employee,
            Shipment_Sh_ID=self.shipment,
            Status_Sh_ID=self.status,
        )

    def test_customer_serializer(self):
        serializer = CustomerSerializer(self.customer)
        self.assertEqual(serializer.data["C_ID"], 1)
        self.assertEqual(serializer.data["C_NAME"], "Test Customer")

    def test_shipment_serializer(self):
        serializer = ShipmentSerializer(self.shipment)
        self.assertEqual(serializer.data["SH_ID"], 1)
        self.assertEqual(serializer.data["SH_CONTENT"], "Test Content")

    def test_status_serializer(self):
        serializer = StatusSerializer(self.status)
        self.assertEqual(serializer.data["SH_ID"], 1)
        self.assertEqual(serializer.data["Current_Status"], "DELIVERED")

    def test_delivered_shipment_serializer(self):
        serializer = DeliveredShipmentSerializer(self.shipment)
        self.assertEqual(serializer.data["SH_ID"], 1)
        self.assertEqual(serializer.data["status"]["Current_Status"], "DELIVERED")


# endregion


# api tests
class APITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Create OAuth2 application
        self.application = Application.objects.create(
            name="Test Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            hash_client_secret=False,
            user=self.user,
        )

        # Setup test client
        self.client = APIClient()

        # Create test data
        self.employee = Employee.objects.create(
            E_ID=1,
            E_NAME="John Doe",
            E_BRANCH="Main",
            E_DESIGNATION="Manager",
            E_ADDR="123 Street",
            E_CONT_NO=1234567890,
        )

        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )

    def get_token(self):
        """Helper method to get OAuth token"""
        token_url = reverse("oauth2_provider:token")
        data = {
            "grant_type": "password",
            "username": "testuser",
            "password": "testpass123",
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
        }

        response = self.client.post(token_url, data)
        return response.json()["access_token"]

    def test_employee_list(self):
        # Get token and set authorization
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Test GET request
        url = reverse("employee-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_create_customer(self):
        # Get token and set authorization
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("customer-list")
        data = {
            "C_ID": 1,
            "C_NAME": "New Customer",
            "C_EMAIL_ID": "new@example.com",
            "C_CONT_NO": 1234567890,
            "C_ADDR": "789 Road",
            "C_TYPE": "Premium",
            "M_ID": self.membership.rec_id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_list_cache(self):
        # Clear cache
        cache.clear()

        # Get token and set authorization
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("employee-list")

        # First request should hit the DB
        with self.assertNumQueries(3):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Second request should hit cache
        with self.assertNumQueries(0):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_no_cache(self):
        # Clear cache
        cache.clear()

        # Get token and set authorization
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("employee-list")

        # First request should hit the DB
        with self.assertNumQueries(3):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Clear cache
        cache.clear()

        # Second request should hit database because cache is clear
        with self.assertNumQueries(3):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class CustomEndpointTests(APITestCase):
    def setUp(self):
        # Setup similar to APITests
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.application = Application.objects.create(
            name="Test Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            hash_client_secret=False,
            user=self.user,
        )

        self.client = APIClient()

        # Create necessary test data
        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )

        self.customer = Customer.objects.create(
            C_ID=1,
            C_NAME="Test Customer",
            C_EMAIL_ID="test@example.com",
            C_CONT_NO=9876543210,
            C_ADDR="456 Avenue",
            C_TYPE="Regular",
            M_ID=self.membership,
        )

        self.shipment = Shipment.objects.create(
            SH_ID=1,
            C_ID=self.customer,
            SH_CONTENT="Test Content",
            SH_DOMAIN="Domestic",
            SER_TYPE="Express",
            SH_WEIGHT="5kg",
            SH_CHARGES=100,
            SR_ADDR="Source Address",
            DS_ADDR="Destination Address",
        )

    def test_customer_shipment_details(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse(
            "customer-shipment-details", kwargs={"rec_id": self.customer.rec_id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["C_NAME"], "Test Customer")
        self.assertEqual(len(response.json()["shipments"]), 1)

    def test_delivered_shipment_list(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Create a status for the shipment
        sh_status = Status.objects.create(
            SH_ID=self.shipment.SH_ID,
            Current_Status="DELIVERED",
            Sent_date=date(2024, 1, 1),
            Delivery_date=date(2024, 1, 2),
        )

        # Create employee manages shipment entry
        employee = Employee.objects.create(
            E_ID=1,
            E_NAME="John Handler",
            E_BRANCH="Main",
            E_DESIGNATION="Handler",
            E_ADDR="Handler Address",
            E_CONT_NO=1234567890,
        )

        EmployeeManagesShipment.objects.create(
            Employee_E_ID=employee, Shipment_Sh_ID=self.shipment, Status_Sh_ID=sh_status
        )

        url = reverse("delivered-shipment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def get_token(self):
        """Helper method to get OAuth token"""
        token_url = reverse("oauth2_provider:token")
        data = {
            "grant_type": "password",
            "username": "testuser",
            "password": "testpass123",
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
        }
        response = self.client.post(token_url, data)
        return response.json()["access_token"]


class ShipmentViewTests(APITestCase):
    def setUp(self):
        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )
        self.customer = Customer.objects.create(
            C_ID=1,
            C_NAME="Test Customer",
            C_EMAIL_ID="test@example.com",
            C_CONT_NO=9876543210,
            C_ADDR="456 Avenue",
            C_TYPE="Regular",
            M_ID=self.membership,
        )
        self.shipment = Shipment.objects.create(
            SH_ID=1,
            C_ID=self.customer,
            SH_CONTENT="Test Content",
            SH_DOMAIN="Domestic",
            SER_TYPE="Express",
            SH_WEIGHT="5kg",
            SH_CHARGES=100,
            SR_ADDR="Source Address",
            DS_ADDR="Destination Address",
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.application = Application.objects.create(
            name="Test Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            hash_client_secret=False,
            user=self.user,
        )
        self.client = APIClient()

    def get_token(self):
        token_url = reverse("oauth2_provider:token")
        data = {
            "grant_type": "password",
            "username": "testuser",
            "password": "testpass123",
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
        }
        response = self.client.post(token_url, data)
        return response.json()["access_token"]

    def test_shipment_list(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("shipment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)


class DeliveredShipmentViewTests(APITestCase):
    def setUp(self):
        self.membership = Membership.objects.create(
            M_ID=1, Start_date=date(2024, 1, 1), End_date=date(2024, 12, 31)
        )
        self.customer = Customer.objects.create(
            C_ID=1,
            C_NAME="Test Customer",
            C_EMAIL_ID="test@example.com",
            C_CONT_NO=9876543210,
            C_ADDR="456 Avenue",
            C_TYPE="Regular",
            M_ID=self.membership,
        )
        self.shipment = Shipment.objects.create(
            SH_ID=1,
            C_ID=self.customer,
            SH_CONTENT="Test Content",
            SH_DOMAIN="Domestic",
            SER_TYPE="Express",
            SH_WEIGHT="5kg",
            SH_CHARGES=100,
            SR_ADDR="Source Address",
            DS_ADDR="Destination Address",
        )
        self.status = Status.objects.create(
            SH_ID=self.shipment.SH_ID,
            Current_Status="DELIVERED",
            Sent_date=date(2024, 1, 1),
            Delivery_date=date(2024, 1, 2),
        )
        self.employee = Employee.objects.create(
            E_ID=1,
            E_NAME="John Handler",
            E_BRANCH="Main",
            E_DESIGNATION="Handler",
            E_ADDR="Handler Address",
            E_CONT_NO=1234567890,
        )
        self.ems = EmployeeManagesShipment.objects.create(
            Employee_E_ID=self.employee,
            Shipment_Sh_ID=self.shipment,
            Status_Sh_ID=self.status,
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.application = Application.objects.create(
            name="Test Application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            hash_client_secret=False,
            user=self.user,
        )
        self.client = APIClient()

    def get_token(self):
        token_url = reverse("oauth2_provider:token")
        data = {
            "grant_type": "password",
            "username": "testuser",
            "password": "testpass123",
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
        }
        response = self.client.post(token_url, data)
        return response.json()["access_token"]

    def test_delivered_shipment_list(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("delivered-shipment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["SH_ID"], 1)
