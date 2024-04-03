import requests
import json
from moduls.beProApi import bepro_definitions as definition


def reservation_step_2(item_code, item_desc, b_token, check_in, check_out, nights,
                       price, order_segment_id, order_seg_id, list_of_order_segment_id,
                       order_id):
    url = "https://pub_srv.beprotravel.net/BePro/api/Reservation/Book"

    payload = json.dumps({
        "Query": {
            "CompantId": definition.company_id,
            "ListOfParamPartOfHotel": [
                {
                    "ItemCode": item_code,
                    "PaxCodes": [1, 2],
                    "Rooms": [
                        {
                            "PaxCodes": [1, 2],
                            "BToken": b_token,
                            "NumberOfRooms": 1
                        }
                    ],
                    "CheckIn": check_in,
                    "CheckOut": check_out,
                    "Nights": nights,
                    "DepartureDate": check_in,
                    "BookingOrder": order_id,
                    "BookingOrderSegmentId": order_segment_id,
                    "PartCommand": 2,
                    "ListOfNote": [
                        "Hotel Name: BELLA BELLA HOUSE",
                        "2 stars",
                        "City: Bangkok Th",
                        "Checkin: 27/03/2024",
                        "Checkout: 28/03/2024",
                        "Nights: 1",
                        "Cancelation Policy: 24/03/2024",
                        "Number of Rooms: 1",
                        "Room 1: Single No Air Conditioning",
                        "Total Price: USD6.98"
                    ],
                    "ParamPrice": {
                        "Gross": {
                            "FBase": 0,
                            "Currency": 'USD',
                            "BaseCurrencyCode": 0,
                            "EUR": 0,
                            "USD": price,
                            "GBP": 0,
                            "LOC": 0,
                            "NetValue": 0.0,
                            "LLV": '',
                            "MV": '',
                            "Value": price
                        }
                    }
                }
            ],
            "Command": 158,
            "OrderDesc": "",
            "ItemCode": item_code,
            "ItemDesc": item_desc,
            "BackOfficeId": "240009999",
            "ContinueToBook": False,
            "ApproveBook": None,
            "Paxes": [
                {
                    "OrderId": order_id,
                    "PaxCode": 1,
                    "PaxTitle": "Mr.",
                    "FirstName": "Amit",
                    "LastName": "Porat",
                    "PaxTypeCode": 0,
                    "Gender": "M",
                    "DOB": "1900-01-01 00:00:00",
                    "Email1": "alexandr.selfg@gmail.com",
                    "Phone1": "87212430897"
                },
                {
                    "OrderId": order_id,
                    "PaxCode": 2,
                    "PaxTitle": "Mr.",
                    "FirstName": "Amit",
                    "LastName": "Porat",
                    "PaxTypeCode": 0,
                    "Gender": "M",
                    "DOB": "1900-01-01 00:00:00",
                    "Email1": "",
                    "Phone1": ""
                }
            ],
            "OrderId": order_id,
            "OrderSegmentId": order_segment_id,
            "OrderSegId": order_seg_id,
            "ListOfOrderSegmentId": list_of_order_segment_id
        }

    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Qz0xMzQ6RD02OkI9MjU4OlU9Njg1OlA9MzBDMUQ=',
        'BEPROCOMPANY': '134'
    }

    print('payload of reservation step 2:', payload)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json()
