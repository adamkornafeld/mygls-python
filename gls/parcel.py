"""
Parcel class
"""

from pydantic.dataclasses import dataclass
from typing import Optional
from .address import Address
from .service import Service


@dataclass
class Parcel:
    ClientNumber: int
    ClientReference: Optional[str]
    Count: int
    DeliveryAddress: Address
    PickupAddress: Address
    PickupDate: str
    ServiceList: list[Service]
    Content: Optional[str] = ""
    CODAmount: Optional[float] = 0
    CODReference: Optional[str] = ""
