"""DeliveryStatus Enum"""
from enum import Enum


class DeliveryStatus(Enum):
    """Enum defining the different states the
       package can be in. Most of these will
       not be visible to the end user. We've
       chosen to assign numeric values rather
       than allowing them to be auto-generated.
       This is because the user may want
       specific codes that need to match up
       with business requirements."""
    out_for_delivery = 1
    delivered = 2
    delayed_arrival = 3
    delayed_delivery = 4
    awaiting_address_update = 5
    at_hub = 6
