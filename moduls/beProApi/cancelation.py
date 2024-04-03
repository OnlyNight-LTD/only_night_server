import requests
import json


def cancellation_request(order_id, order_segment_id):
    url = "https://pub_srv.beprotravel.net/BePro/api/Reservation/OrderCancel"

    payload = json.dumps({
        "Query": {
            "OrderId": order_id,
            "OrderSegmentId": order_segment_id
        }
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Qz0xMzQ6RD02OkI9MjU4OlU9Njg1OlA9MzBDMUQ=',
        'BEPROCOMPANY': '134',

    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.text)
    return response.json()
