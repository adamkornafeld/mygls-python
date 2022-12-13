import unittest
import responses
from datetime import datetime
from gls import GLS, Address, Parcel


ADDRESS = {
    "City": "Budapest",
    "ContactEmail": "info@bme.hu",
    "ContactName": "Dr. Sztoczek József",
    "ContactPhone": "+36 1 463-1111",
    "CountryIsoCode": "HU",
    "HouseNumber": "3",
    "Name": "Budapesti Műszaki és Gazdaságtudományi Egyetem",
    "Street": "Műegyetem rkp.",
    "ZipCode": "1111",
    "HouseNumberInfo": "",
}


class TestGLS(unittest.TestCase):
    def test_create_parcel(self):
        gls = GLS(123, "", "")

        parcel: Parcel = gls.create_parcel(
            pickup_from=Address(**ADDRESS),
            deliver_to=Address(**ADDRESS),
            pickup_date=datetime(2022, 4, 10, 12, 30),
            reference="REF-123",
            count=1,
            content="paper",
            cod_reference="cod-321",
            cod_amount=456,
        )

        self.assertEqual(123, parcel.ClientNumber)
        self.assertEqual("REF-123", parcel.ClientReference)
        self.assertEqual("1649608200000", parcel.PickupDate)
        self.assertEqual("Budapest", parcel.PickupAddress.City)
        self.assertEqual("Budapest", parcel.DeliveryAddress.City)
        self.assertEqual(1, parcel.Count)
        self.assertEqual("paper", parcel.Content)
        self.assertEqual("cod-321", parcel.CODReference)
        self.assertEqual(456, parcel.CODAmount)
        self.assertEqual([], parcel.ServiceList)

    @responses.activate
    def test_get_parcels(self):

        responses.add(
            responses.POST,
            "https://api.mygls.hu/ParcelService.svc/json/GetParcelList",
            json={"GetParcelListErrors": [], "PrintDataInfoList": []},
            status=200,
        )

        gls = GLS(123, "", "")
        result = gls.get_parcels(
            print_from=datetime(2021, 11, 1, 12, 30),
            print_to=datetime(2021, 11, 24, 12, 30),
        )
        self.assertEqual({"GetParcelListErrors": [], "PrintDataInfoList": []}, result)

    @responses.activate
    def test_get_printed_labels(self):
        responses.add(
            responses.POST,
            "https://api.mygls.hu/ParcelService.svc/json/GetPrintedLabels",
            json={"GetPrintedLabelsErrorList": [], "Labels": [10, 11, 22, 23]},
            status=200,
        )
        gls = GLS(123, "", "")
        result = gls.get_printed_labels(parcel_ids=[1, 2])
        self.assertEqual(
            {"GetPrintedLabelsErrorList": [], "Labels": [10, 11, 22, 23]}, result
        )

    @responses.activate
    def test_delete_labels(self):
        responses.add(
            responses.POST,
            "https://api.mygls.hu/ParcelService.svc/json/DeleteLabels",
            json={
                "SuccessfullyDeletedList": [{"ParcelId": 1, "SubParcelIdList": []}],
                "DeleteLabelsErrorList": [],
            },
            status=200,
        )
        gls = GLS(123, "", "")
        result = gls.delete_labels(parcel_ids=[1])
        self.assertEqual(1, result.SuccessfullyDeletedList[0].ParcelId)

    @responses.activate
    def test_prepare_labels(self):
        responses.add(
            responses.POST,
            "https://api.mygls.hu/ParcelService.svc/json/PrepareLabels",
            json={
                "ParcelInfoList": [],
                "PrepareLabelsError": [],
            },
            status=200,
        )
        gls = GLS(123, "", "")

        parcel: Parcel = gls.create_parcel(
            pickup_from=Address(**ADDRESS),
            deliver_to=Address(**ADDRESS),
            pickup_date=datetime(2022, 4, 10, 12, 30),
            reference="REF-123",
            count=1,
        )

        result = gls.prepare_labels([parcel])
        self.assertEqual(
            {
                "ParcelInfoList": [],
                "PrepareLabelsError": [],
            },
            result,
        )
