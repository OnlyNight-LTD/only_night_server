from fastapi import APIRouter, HTTPException

from dbConnections import sql_select_queries
from moduls import logger

hotels_names_router = APIRouter()


@hotels_names_router.get('/')
async def get_hotels_names():
    try:
        hotels = set(sql_select_queries.select_hotels_name())
        return {"Hotels": hotels}

    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")
