import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from dbConnections import sql_insert_queries
from moduls.algorithm import opportunity_response_handler

search_opportunities_router = APIRouter()


class SearchHotelsPostBody(BaseModel):
    search_key: str
    stars: int
    num_adults: int
    num_children: int
    children_age: list


@search_opportunities_router.post('/')
async def search_opportunities(body: SearchHotelsPostBody):
    try:
        sql_insert_queries.insert_search_setting(body.stars, body.search_key)
        return {"massage": "The request was successfully received - search setting added successfully"}
    except HTTPException:
        return HTTPException(status_code=500)


@search_opportunities_router.get('/')
async def get_opportunities():
    try:
        start_time = time.time()
        hotels = opportunity_response_handler.get_opportunities_response()
        end_time = time.time()
        print(f"process finish with {end_time - start_time} seconds")
        return hotels
    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")
