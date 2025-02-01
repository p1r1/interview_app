import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from interview_app.models import *
import os


class Command(BaseCommand):
    """Load data from CSV files to the database"""

    help = "Load data from CSV files to the database"
    CSV_FOLDER_PATH = "./docs/other_files/csv/"

    def handle(self, *args, **options):
        self.load_employees()
        self.load_memberships()
        self.load_customers()
        self.load_shipments()
        self.load_payments()
        self.load_statuses()
        self.load_employee_manages_shipments()
        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))

    def load_employees(self):
        self.stdout.write("Loading employees...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Employee_Details.csv"),
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Employee.objects.create(**row)

    def load_memberships(self):
        self.stdout.write("Loading memberships...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Membership.csv"), "r", encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Membership.objects.create(**row)

    def load_customers(self):
        self.stdout.write("Loading customers...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Customer.csv"), "r", encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                membership_id = row.pop("M_ID")
                membership = Membership.objects.get(M_ID=membership_id)
                Customer.objects.create(M_ID=membership, **row)

    def load_shipments(self):
        self.stdout.write("Loading shipments...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Shipment_Details.csv"),
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer_id = row.pop("C_ID")
                customer = Customer.objects.get(C_ID=customer_id)
                Shipment.objects.create(C_ID=customer, **row)

    def load_payments(self):
        self.stdout.write("Loading payments...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Payment_Details.csv"),
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                shipment_id = row.pop("SH_ID")
                client_id = row.pop("C_ID")
                shipment = Shipment.objects.get(SH_ID=shipment_id)
                customer = Customer.objects.get(C_ID=client_id)
                payment_date = row.pop("Payment_Date")
                # convert to  YYYY-MM-DD format
                if payment_date:
                    try:
                        payment_date = datetime.strptime(
                            payment_date, "%Y-%m-%d"
                        ).strftime("%Y-%m-%d")
                    except ValueError:
                        payment_date = None
                else:
                    payment_date = None

                Payment.objects.create(
                    SH_ID=shipment, C_ID=customer, Payment_Date=payment_date, **row
                )

    def load_statuses(self):
        self.stdout.write("Loading statuses...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "Status.csv"), "r", encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                sent_date = row.pop("Sent_date")
                delivery_date = row.pop("Delivery_date")
                if sent_date:
                    try:
                        sent_date = datetime.strptime(sent_date, "%m/%d/%Y").strftime(
                            "%Y-%m-%d"
                        )
                    except ValueError:
                        sent_date = None
                else:
                    sent_date = None
                if delivery_date:
                    try:
                        delivery_date = datetime.strptime(
                            delivery_date, "%m/%d/%Y"
                        ).strftime("%Y-%m-%d")
                    except ValueError:
                        delivery_date = None
                else:
                    delivery_date = None

                Status.objects.create(
                    Sent_date=sent_date, Delivery_date=delivery_date, **row
                )

    def load_employee_manages_shipments(self):
        self.stdout.write("Loading employee manages shipments...")
        with open(
            os.path.join(self.CSV_FOLDER_PATH, "employee_manages_shipment.csv"),
            "r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                employee_id = row.pop("Employee_E_ID")
                shipment_id = row.pop("Shipment_Sh_ID")
                status_id = row.pop("Status_Sh_ID")
                employee = Employee.objects.get(E_ID=employee_id)
                shipment = Shipment.objects.get(SH_ID=shipment_id)
                status = Status.objects.get(SH_ID=status_id)
                EmployeeManagesShipment.objects.create(
                    Employee_E_ID=employee,
                    Shipment_Sh_ID=shipment,
                    Status_Sh_ID=status,
                    **row
                )
