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
    class Meta:
        model = Employee
        fields = "__all__"


# Membership
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


# Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        # for the warning. create nested serialzer manually
        # depth = 1


# Shipment
class ShipmentSerializer(serializers.ModelSerializer):
    C_ID = CustomerSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = "__all__"


# Payment
class PaymentSerializer(serializers.ModelSerializer):
    C_ID = CustomerSerializer(read_only=True)
    SH_ID = ShipmentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


# Status
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


# EmployeeManagesShipment ems
class EmployeeManagesShipmentSerializer(serializers.ModelSerializer):
    Employee_E_ID = EmployeeSerializer(read_only=True)
    Shipment_Sh_ID = ShipmentSerializer(read_only=True)
    Status_Sh_ID = StatusSerializer(read_only=True)

    class Meta:
        model = EmployeeManagesShipment
        fields = "__all__"


# region Custom Endpoint Serializers
# customer>shipment
class CustomerShipmentSerializer(serializers.ModelSerializer):
    shipments = ShipmentSerializer(many=True, read_only=True, source="shipment_set")

    class Meta:
        model = Customer
        fields = ["C_ID", "C_NAME", "shipments"]


# status>shipment
class EMSStatusSerializer(serializers.ModelSerializer):
    # status = StatusSerializer(many=True, read_only=True, source="status_set")
    Status_Sh_ID = StatusSerializer(read_only=True)

    class Meta:
        model = EmployeeManagesShipment
        fields = ["Employee_E_ID", "Shipment_Sh_ID", "Status_Sh_ID"]


# status > shipment
class DeliveredShipmentSerializer(serializers.ModelSerializer):
    # Include the Status information
    status = serializers.SerializerMethodField()
    # Status_Sh_ID = StatusSerializer(read_only=True, source="status_set", many=True)

    class Meta:
        model = Shipment
        fields = "__all__"

    def get_status(self, obj):
        # Get the related Status object through EmployeeManagesShipment
        # Get the first related EmployeeManagesShipment
        ems = obj.employeemanagesshipment_set.first()
        if ems and ems.Status_Sh_ID:
            return StatusSerializer(ems.Status_Sh_ID).data
        return None


# endregion
