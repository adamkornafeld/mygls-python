from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    City: str
    ContactEmail: Optional[str]
    ContactName: Optional[str]
    ContactPhone: Optional[str]
    CountryIsoCode: str
    HouseNumber: str
    Name: str
    Street: str
    ZipCode: str
    HouseNumberInfo: Optional[str]
