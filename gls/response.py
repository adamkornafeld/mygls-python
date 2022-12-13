from pydantic.dataclasses import dataclass
from typing import Optional
from .parcel import Parcel


@dataclass
class ErrorInfo:
    ErrorCode: int
    ErrorDescription: str
    ClientReferenceList: list[str]
    ParcelIdList: list[int]


@dataclass
class PrintDataInfo:
    Parcel: Parcel
    ParcelId: int
    ParcelNumber: float
    ParcelNumberWithCheckdigit: float
    DepotNumber: Optional[str]
    Driver: Optional[str]
    Depot: Optional[str]
    Sort: Optional[str]
    B2CChar: Optional[str]
    ClientReference: Optional[str]


@dataclass
class ParcelInfo:
    ClientReference: str
    ParcelId: int


@dataclass
class ParcelResponse:
    GetParcelListErrors: list[ErrorInfo]
    PrintDataInfoList: list[PrintDataInfo]


@dataclass
class PrintedLabelsResponse:
    Labels: Optional[list[int]]
    GetPrintedLabelsErrorList: list[ErrorInfo]


@dataclass
class PrepareLabelsResponse:
    ParcelInfoList: list[ParcelInfo]
    PrepareLabelsError: list[ErrorInfo]


@dataclass
class DeletedParcelInfo:
    ParcelId: int
    SubParcelIdList: list[int]


@dataclass
class DeleteLabelsResponse:
    SuccessfullyDeletedList: list[DeletedParcelInfo]
    DeleteLabelsErrorList: list[ErrorInfo]
