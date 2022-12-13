import hashlib
import json
import logging
import requests
from datetime import datetime
from typing import Optional
from dataclasses import asdict
from .parcel import Parcel
from .response import (
    ParcelResponse,
    PrintedLabelsResponse,
    PrepareLabelsResponse,
    DeleteLabelsResponse,
)
from .address import Address
from .gls_types import PrinterType
from .service import Service
from .settings import Settings

HEADERS = {"Content-type": "application/json"}

log = logging.getLogger(__name__)


class GLS:
    """
    GLS API client

    https://api.mygls.hu/index_en.html
    """

    def __init__(
        self,
        client_number: int,
        username: str,
        password: str,
        settings: Settings = Settings(),
    ):
        """
        Args: client_number: MyGLS client number
              username: MyGLS username
              password: MyGLS password
              timeout_seconds: network request timeout in seconds
        """
        self.username = username
        self.client_number = client_number
        self.password = self._calculate_password(password)
        self.settings = settings

    def convert_to_datefield(self, date: datetime) -> str:
        """
        Converts date object to API format: /Date(timestamp)/
        """
        return f"/Date({self._convert_to_timestamp(date)})/"

    def create_parcel(
        self,
        pickup_from: Address,
        deliver_to: Address,
        pickup_date: datetime,
        reference: str,
        count: int,
        content: Optional[str] = "",
        cod_amount: Optional[float] = 0,
        cod_reference: Optional[str] = "",
        services: Optional[list[Service]] = [],
    ) -> Parcel:
        """
        Creates a parcel object
        """
        return Parcel(
            ClientNumber=self.client_number,
            ClientReference=reference,
            Content=content,
            PickupAddress=pickup_from,
            DeliveryAddress=deliver_to,
            PickupDate=self._convert_to_timestamp(pickup_date),
            Count=count,
            CODAmount=cod_amount,
            CODReference=cod_reference,
            ServiceList=services,
        )

    def get_parcels(
        self,
        pickup_from: Optional[datetime] = None,
        pickup_to: Optional[datetime] = None,
        print_from: Optional[datetime] = None,
        print_to: Optional[datetime] = None,
    ) -> ParcelResponse:
        """
        Gets parcels optionally filtered by pickup and print data ranges
        """
        payload = self._request_payload()
        if pickup_from:
            payload["PickupDateFrom"] = self.convert_to_datefield(pickup_from)
        if pickup_to:
            payload["PickupDateTo"] = self.convert_to_datefield(pickup_to)
        if print_from:
            payload["PrintDateFrom"] = self.convert_to_datefield(print_from)
        if print_to:
            payload["PrintDateTo"] = self.convert_to_datefield(print_to)
        response = requests.post(
            f"{self.settings.api_root}/GetParcelList",
            data=json.dumps(payload),
            headers=HEADERS,
            timeout=self.settings.timeout_seconds,
        )
        return ParcelResponse.__pydantic_model__.parse_raw(response.text)

    def get_printed_labels(
        self,
        parcel_ids: list[int],
        printer_type: PrinterType = PrinterType.THERMO,
        print_position: int = 1,
        show_dialog: bool = False,
    ) -> PrintedLabelsResponse:
        """
        Gets printed labels
        """
        payload = self._request_payload()
        payload["ParcelIdList"] = parcel_ids
        payload["PrintPosition"] = print_position
        payload["ShowPrintDialog"] = 1 if show_dialog else 0
        payload["TypeOfPrinter"] = printer_type.value
        response = requests.post(
            f"{self.settings.api_root}/GetPrintedLabels",
            data=json.dumps(payload),
            headers=HEADERS,
            timeout=self.settings.timeout_seconds,
        )
        return PrintedLabelsResponse.__pydantic_model__.parse_raw(response.text)

    def print_labels(
        self,
        pdf_path: str,
        parcels: list[Parcel],
        printer_type: PrinterType = PrinterType.THERMO,
    ) -> list[int]:
        """
        Creates a parcel label and saves it as a PDF on the designated path
        """
        label_info = self.prepare_labels(parcels)
        parcel_ids = [label.ParcelId for label in label_info.ParcelInfoList]
        log.info(f"Prepared labels: {parcel_ids}")
        labels = self.get_printed_labels(parcel_ids, printer_type)
        label_data = labels.Labels
        self._save_pdf(pdf_path, label_data)
        return parcel_ids

    def prepare_labels(self, parcels: list[Parcel]) -> PrepareLabelsResponse:
        """
        Prepares labels for printing
        """
        payload = self._request_payload()
        payload["ParcelList"] = [asdict(p) for p in parcels]
        response = requests.post(
            f"{self.settings.api_root}/PrepareLabels",
            data=json.dumps(payload),
            headers=HEADERS,
            timeout=self.settings.timeout_seconds,
        )
        return PrepareLabelsResponse.__pydantic_model__.parse_raw(response.text)

    def delete_labels(self, parcel_ids: list[int]) -> DeleteLabelsResponse:
        """
        Deletes labels
        """
        payload = self._request_payload()
        payload["ParcelIdList"] = parcel_ids
        response = requests.post(
            f"{self.settings.api_root}/DeleteLabels",
            data=json.dumps(payload),
            headers=HEADERS,
            timeout=self.settings.timeout_seconds,
        )
        return DeleteLabelsResponse.__pydantic_model__.parse_raw(response.text)

    def _calculate_password(self, plaintext: str) -> list[int]:
        """
        Calculates password for API authentication
        """
        sha = hashlib.sha512()
        sha.update(plaintext.encode("utf-8"))
        return list(sha.digest())

    def _convert_to_timestamp(self, date: datetime) -> int:
        """
        Converts date object to timestamp
        """
        return int(datetime.timestamp(date)) * 1000

    def _request_payload(self) -> dict:
        return {"Username": self.username, "Password": self.password}

    def _save_pdf(self, pdf_path: str, byte_list: list[int]) -> None:
        data = bytes(byte_list)
        with open(pdf_path, "wb") as f:
            f.write(data)
        log.info(f"Saved parcel label to {pdf_path}")
