from enum import Enum


class Code(Enum):
    H24 = "24H"
    ADR = "ADR"
    AOS = "AOS"
    COD = "COD"
    CS1 = "CS1"
    DDS = "DDS"
    DPV = "DPV"
    FDS = "FDS"
    FSS = "FSS"
    INS = "INS"
    PRS = "PRS"
    PSD = "PSD"
    PSS = "PSS"
    SAT = "SAT"
    SBS = "SBS"
    SDS = "SDS"
    SM1 = "SM1"
    SM2 = "SM2"
    SRS = "SRS"
    SZL = "SZL"
    T09 = "T09"
    T10 = "T10"
    T12 = "T12"
    TGS = "TGS"
    XS = "XS"


class PrinterType(Enum):
    A4_2x2 = "A4_2x2"
    A4_4x1 = "A4_4x1"
    CONNECT = "Connect"
    THERMO = "Thermo"
