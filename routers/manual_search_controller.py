from datetime import datetime, timedelta

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from moduls.beProApi import search_one_hotel

search_one_hotel_opportunities_router = APIRouter()


class SearchOneHotelPostBody(BaseModel):
    city: str
    hotel_name: str
    stars: float
    check_in: str
    check_out: str
    price: float
    location: float
    room_token: str = ""
    hotel_code: str = ""


@search_one_hotel_opportunities_router.post('/')
async def search_one_hotels(body: SearchOneHotelPostBody):
    try:
        check_in, check_out = validate_check_in_check_out(body.check_in, body.check_out)
        print(check_in, check_out)
        return search_one_hotel.be_pro_manual_search(body.hotel_name, body.stars, check_in, check_out,
                                                     body.city, body.location, body.price, body.room_token,
                                                     body.hotel_code)

    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")


def validate_check_in_check_out(check_in, check_out):
    check_in = datetime.strptime(check_in, "%Y-%m-%d")
    check_out = datetime.strptime(check_out, "%Y-%m-%d")
    if check_in == check_out:
        check_out = check_out + timedelta(days=1)
    return check_in, check_out
