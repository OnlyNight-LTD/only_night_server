from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from routers import manual_search_controller
from moduls.beProApi import orders, reservation_functions, bepro_api

bookings_router = APIRouter()


def validate_check_in_check_out(check_in, check_out):
    print(check_in, check_out)
    check_in = datetime.strptime(check_in, "%Y-%m-%d")
    check_out = datetime.strptime(check_out, "%Y-%m-%d")
    if check_in == check_out:
        check_out = check_out + timedelta(days=1)
    return check_in, check_out


# @bookings_router.get('/')
# async def charge_condition(room_token, price):
#     try:
#         info_grass_rate = bepro_api.check_charge_condition(room_token, price)
#         if info_grass_rate[0]:
#             return {"massage": f"Warning the price has changed! The current price - {info_grass_rate[1]} "
#                                f"The previous price - {price}"}
#         return {"massage": f"The price has not changed {price}"}
#     except HTTPException:
#         return HTTPException(status_code=500)

@bookings_router.get('/')
async def get_orders():
    try:
        order = orders.get_orders()
        return {'orders': order}
    except HTTPException:
        return HTTPException(status_code=500)


@bookings_router.post('/')
async def booking(body: manual_search_controller.SearchOneHotelPostBody):
    try:
        check_in, check_out = validate_check_in_check_out(body.check_in, body.check_out)
        print(check_in, check_out)
        return reservation_functions.be_pro_booking(body.hotel_name, body.stars, body.check_in, body.check_out,
                                                    body.city, body.location, body.price, body.room_token,
                                                    body.hotel_code)
    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")
