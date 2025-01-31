from django.db import models

# Create your models here.


# we can not trust E_ID to be a primarykey!
class Employee(models.Model):
    """
    Represents an employee in the system.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    E_ID = models.BigIntegerField(unique=True, help_text="Employee ID")
    E_NAME = models.CharField(max_length=30, help_text="Employee Name")
    E_BRANCH = models.CharField(max_length=15, help_text="Employee Branch")
    E_DESIGNATION = models.CharField(max_length=40, help_text="Employee Designation")
    E_ADDR = models.CharField(max_length=100, help_text="Employee Address")
    E_CONT_NO = models.BigIntegerField(help_text="Employee Phone")

    def __str__(self):
        """Returns a string representation."""
        return f"{self.E_NAME} ({self.E_DESIGNATION})"


class Membership(models.Model):
    """
    Represents a membership plan.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    M_ID = models.BigIntegerField(unique=True, help_text="Membership Id")
    Start_date = models.DateField(
        null=True, blank=True, help_text="Membership Start Date"
    )
    End_date = models.DateField(null=True, blank=True, help_text="Membership End Date")

    def __str__(self):
        return f"Membership: {self.M_ID}"


class Customer(models.Model):
    """
    Represents a customer in the system.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    C_ID = models.BigIntegerField(unique=True, help_text="Customer Id")
    C_NAME = models.CharField(max_length=30, help_text="Customer Name")
    C_EMAIL_ID = models.CharField(max_length=50, help_text="Customer Email")
    C_CONT_NO = models.BigIntegerField(help_text="Customer Phone")
    C_ADDR = models.CharField(max_length=100, help_text="Customer Address")
    C_TYPE = models.CharField(max_length=30, help_text="Customer Type")
    M_ID = models.ForeignKey(
        Membership, on_delete=models.CASCADE, help_text="Customer Membership Id"
    )

    def __str__(self):
        return f"{self.C_NAME} ({self.C_TYPE})"


class Shipment(models.Model):
    """
    Represents a shipment in the system.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    SH_ID = models.BigIntegerField(unique=True, help_text="Shipment Id")
    C_ID = models.ForeignKey(
        Customer, on_delete=models.CASCADE, help_text="Customer Id"
    )
    SH_CONTENT = models.CharField(max_length=40, help_text="Shipmet Content Type")
    SH_DOMAIN = models.CharField(max_length=15, help_text="Shipment Domain")
    SER_TYPE = models.CharField(max_length=15, help_text="Shipment Service Type")
    SH_WEIGHT = models.CharField(max_length=10, help_text="Shipment Weight")
    SH_CHARGES = models.IntegerField(help_text="Shipment Charges")
    SR_ADDR = models.CharField(max_length=100, help_text="Source Address")
    DS_ADDR = models.CharField(max_length=100, help_text="Destination Addres")

    def __str__(self):
        return f"Shipment {self.SH_ID}"


class Payment(models.Model):
    """
    Represents a payment made by a customer for a shipment.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    Payment_ID = models.CharField(max_length=40, help_text="Payment Id (UID)")
    C_ID = models.ForeignKey(
        Customer, on_delete=models.CASCADE, help_text="Shipment Customer Id"
    )
    SH_ID = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, help_text="Shipment Id"
    )
    AMOUNT = models.IntegerField(help_text="Customer Payment Amount")
    Payment_Status = models.CharField(max_length=10, help_text="Payment Status")
    Payment_Mode = models.CharField(max_length=25, help_text="Payment Method")
    Payment_Date = models.DateField(null=True, blank=True, help_text="Payment Date")

    def __str__(self):
        return f"Payment {self.Payment_ID}"


class Status(models.Model):
    """
    Represents the status of a shipment.
    """

    rec_id = models.BigAutoField(
        primary_key=True, editable=False, help_text="Record Id"
    )
    # foreign key?
    SH_ID = models.BigIntegerField(unique=True, help_text="Shipmet Id")
    Current_Status = models.CharField(
        max_length=15, help_text="Current Status of Shipment"
    )
    Sent_date = models.DateField(null=True, blank=True, help_text="Sent Date")
    Delivery_date = models.DateField(null=True, blank=True, help_text="Delivery Date")

    def __str__(self):
        return f"Status {self.SH_ID}"


class EmployeeManagesShipment(models.Model):
    """
    Represents the relationship between an employee and a shipment they manage.
    """

    rec_id = models.BigAutoField(
        primary_key=True, unique=True, editable=False, help_text="Record Id"
    )
    Employee_E_ID = models.ForeignKey(
        Employee, on_delete=models.CASCADE, help_text="Employee Id"
    )
    Shipment_Sh_ID = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, help_text="Shipment Id"
    )
    Status_Sh_ID = models.ForeignKey(
        Status, on_delete=models.CASCADE, help_text="Shipment Status"
    )

    def __str__(self):
        return f"Employee {self.Employee_E_ID} manages shipment {self.Shipment_Sh_ID}"
