from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(Membership)
admin.site.register(Customer)
admin.site.register(Shipment)
admin.site.register(Payment)
admin.site.register(Status)
admin.site.register(EmployeeManagesShipment)
