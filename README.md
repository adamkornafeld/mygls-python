# mygls-rest-client
 
 `mygls-rest-client` is a python client for the MyGLS REST API to create printable shipping labels.

Before you can start interacting with the MyGLS REST API, you need an agreement with GLS. If you
don’t have the required MyGLS login credentials please contact [GLS](https://gls-group.eu/GROUP/en/home).


## Motivation

> The API development team of GLS has decided to release sample code for C#, PHP, JAVA. 

This project adds Python to mix. 

### Under the hood

`mygls-rest-client` uses the [requests](https://github.com/psf/requests) library to fetch data via the MyGLS API. A couple design decisions to be aware of that this client library has no influence on:
- all API endpoints use the `POST` HTTP verb
- all model properties use [upper camel case](https://wiki.c2.com/?UpperCamelCase) naming

## Basic usage

1. Create a `GLS` instance:

        from gls import GLS

        client_number = 100123456
        username = "user@gls.hu"
        password = "secret"
        
        gls = GLS(client_number, username, password)

    1.1. Configure settings

        from gls import Settings, CountryCode

        gls = GLS(client_number, username, password, Settings(country=CountryCode.HR, test=True))

    Consult [settings.py](gls/settings.py) for supported countries.

1. Create a parcel label:

        from datetime import datetime
        from gls import Address, Parcel

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

        parcel = gls.create_parcel(
            pickup_from = Address(**ADDRESS),
            deliver_to = Address(**ADDRESS),
            pickup_date = datetime.today(),
            reference = "REF-123",
            count = 1
        )

        parcel_ids = gls.print_labels(
            "~/label.pdf", [parcel],
        )

1. Look up parcels by print date:

        from gls import ParcelResponse
        from datetime import datetime

        parcels: ParcelResponse = gls.get_parcels(
            print_from=datetime.today(),
            print_to=datetime.today(),
        )

1. Get printed labels:

        from gls import PrintedLabelsResponse

        labels: PrintedLabelsResponse = gls.get_printed_labels(parcel_ids=[10023456])

1. Delete labels:

        from gls import DeleteLabelsResponse

        parcel_ids = [10023456]
        result: DeleteLabelsResponse = gls.delete_labels(parcel_ids)


## Sample Output

Here is an example of how the created label would look like in the saved PDF:

![Label](https://github.com/adamkornafeld/mygls-python/blob/main/parcel.png?raw=true)


## Contributions

Contributions are welcome, please submit a Pull Request.

## Reference

GLS is a trademark and brand of General Logistics Systems Germany GmbH & Co.
