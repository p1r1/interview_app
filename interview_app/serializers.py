from rest_framework import serializers
from .models import (
    Employee,
    Membership,
    Customer,
    Shipment,
    Payment,
    Status,
    EmployeeManagesShipment,
)


# Employee
class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    """

    class Meta:
        model = Employee  # Specifies the model to serialize
        fields = "__all__"  # Includes all fields of the model


# Membership
class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for the Membership model.
    """

    class Meta:
        model = Membership
        fields = "__all__"


# Customer
class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """

    class Meta:
        model = Customer
        fields = "__all__"
        # for the warning. create nested serialzer manually
        # depth = 1  # NOTE: depth=1 can lead to issues. Using nested serializers manually.


# Shipment
class ShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Shipment model, includes nested CustomerSerializer for C_ID.
    """

    C_ID = CustomerSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = "__all__"


# Payment
class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model, includes nested CustomerSerializer for C_ID and ShipmentSerializer for SH_ID.
    """

    # Includes nested Customer data, read-only
    C_ID = CustomerSerializer(read_only=True)
    # Includes nested Shipment data, read-only
    SH_ID = ShipmentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


# Status
class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for the Status model.
    """

    class Meta:
        model = Status
        fields = "__all__"


# EmployeeManagesShipment ems
class EmployeeManagesShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmployeeManagesShipment model, includes nested serializers
    for Employee_E_ID, Shipment_Sh_ID, and Status_Sh_ID.
    """

    Employee_E_ID = EmployeeSerializer(read_only=True)
    Shipment_Sh_ID = ShipmentSerializer(read_only=True)
    Status_Sh_ID = StatusSerializer(read_only=True)

    class Meta:
        model = EmployeeManagesShipment
        fields = "__all__"


# region Custom Endpoint Serializers
# customer>shipment
class CustomerShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving customer details along with their associated shipments.
    """

    shipments = ShipmentSerializer(many=True, read_only=True, source="shipment_set")

    class Meta:
        model = Customer
        fields = ["C_ID", "C_NAME", "shipments"]


# status > ems
class EMSStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving EmployeeManagesShipment details along with its associated Status details.
    """

    Status_Sh_ID = StatusSerializer(read_only=True)

    class Meta:
        model = EmployeeManagesShipment
        fields = ["Employee_E_ID", "Shipment_Sh_ID", "Status_Sh_ID"]


# status > shipment
class DeliveredShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving shipment details with the status.
    """

    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shipment
        fields = "__all__"

    def get_status(self, obj):
        """
        Retrieves the related Status object through EmployeeManagesShipment and serializes it.
        """
        # Get the related Status object through EmployeeManagesShipment
        # Get the first related EmployeeManagesShipment
        ems = obj.employeemanagesshipment_set.first()
        if ems and ems.Status_Sh_ID:
            # Serializes the related status object and returns the serialized data
            return StatusSerializer(ems.Status_Sh_ID).data
        return None


# shipment{rec_id} > customer
class ShipmentCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving shipment details along with its associated customer.
    """

    Customer = CustomerSerializer(source="C_ID", read_only=True)  # many = True

    class Meta:
        model = Shipment
        fields = "__all__"


# endregion
