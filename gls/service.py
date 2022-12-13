from pydantic.dataclasses import dataclass
from typing import Optional
from .gls_types import Code


@dataclass
class ServiceParameterString:
    Value: Optional[str]


@dataclass
class ServiceParameterDateTime:
    Value: Optional[str]


@dataclass
class ServiceParameterADR:
    AdrItemType: int
    AmountUnit: int
    InnerCount: int
    PackSize: int
    UnNumber: int


@dataclass
class ServiceParameterStringDecimal:
    StringValue: str
    DecimalValue: float


@dataclass
class ServiceParameterDecimal:
    Value: Optional[float]


@dataclass
class ServiceParameterTimeRange:
    TimeFrom: str
    TimeTo: str


@dataclass
class PSDParameter:
    StringValue: str


@dataclass
class Service:
    Code: Code
    ADRParameter: Optional[ServiceParameterADR]
    AOSParameter: Optional[ServiceParameterString]
    CS1Parameter: Optional[ServiceParameterString]
    DDSParameter: Optional[ServiceParameterDateTime]
    DPVParameter: Optional[ServiceParameterStringDecimal]
    FDSParameter: Optional[ServiceParameterString]
    FSSParameter: Optional[ServiceParameterString]
    INSParameter: Optional[ServiceParameterDecimal]
    MMPParameter: Optional[ServiceParameterDecimal]
    PSDParameter: Optional[PSDParameter]
    SDSParameter: Optional[ServiceParameterTimeRange]
    SM1Parameter: Optional[ServiceParameterString]
    SM2Parameter: Optional[ServiceParameterString]
    SZLParameter: Optional[ServiceParameterString]
    Value: Optional[str]
