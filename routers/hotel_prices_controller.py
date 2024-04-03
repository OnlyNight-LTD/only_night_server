from fastapi import APIRouter, HTTPException

from moduls.algorithm import calculate_hotel_price

prices_router = APIRouter()


@prices_router.get('/{hotel_id}')
async def get_prices(hotel_id: int):
    try:
        return calculate_hotel_price.get_hotel_room_classes(hotel_id)
    except HTTPException:
        return HTTPException(status_code=500)
