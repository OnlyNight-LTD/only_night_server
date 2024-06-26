import requests
import datetime
import json
from datetime import datetime
from moduls.beProApi import bepro_definitions as definition


def charge_condition_request(supplier_code, supplier_city_code, check_in, check_out, nights, item_code, room_token):
    print('in charge_condition_request', supplier_code, supplier_city_code)
    url = "https://pub_srv.beprotravel.net/BePro/api/Hotels/ChargeCondition"

    payload = json.dumps({
        "Query": {
            "CompanyId": definition.company_id,
            "Command": 2,
            "LanguageCode": "en",
            "CurrencyCode": "USD",
            "SysSuppCode": supplier_code,
            "SuppCityCode": supplier_city_code,
            "CheckIn": check_in,
            "CheckOut": check_out,
            "Nights": nights,
            "Item": {
                "Code": item_code,
                "ItemType": "H"
            },
            "HotelRooms": [
                {
                    "DisplayType": 0,
                    "SysCode": 60,
                    "NumRoom": 1,
                    "NumAdt": 2,
                    "NumCnn": 0,
                    "NumPax": 2,
                    "CnnAge1": 0,
                    "CnnAge2": 0,
                    "CnnAge3": 0,
                    "CnnAge4": 0,
                    "BToken": room_token,
                    "NumBed": 1
                }
            ],
            "ResultMode": "Json",
            "MaxMilliSecondsTimeToWait": 100000
        },
        "Compress": True,
        "LanguageCode": "en"
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Qz0xMzQ6RD02OkI9MjU4OlU9Njg1OlA9MzBDMUQ=',
        'BEPROCOMPANY': '134',

    }
    print('payload of charge_condition: ', payload)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.json()


def extract_data_from_room_token(room_token):
    print('in extract_data_from_room_token', room_token)
    room_token_data = room_token.split("‡")
    supplier_city_code = room_token_data[2]
    supplier_code = room_token_data[3]
    item_code = room_token_data[4]
    check_in = room_token_data[5]
    nights = room_token_data[6]

    return supplier_city_code, supplier_code, item_code, check_in, nights


def calculate_check_out(check_in, nights):
    print('in calculate_check_out of charge condition', check_in, nights, type(check_in))
    check_in = datetime.strptime(check_in, "%Y-%m-%d")# %H:%M:%S  "%Y-%m-%d
    return check_in + datetime.timedelta(days=nights)


def extract_infoGrossRate(charge_condition_response):
    return charge_condition_response.get("cancellationPolicy").get("infoGrossRate")
