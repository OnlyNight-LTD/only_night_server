import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import hotel_prices_controller
from routers import booking_controller
from routers import hotels_names_controller
from routers import manual_search_controller
from routers import search_oppo_controller

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_oppo_controller.search_opportunities_router, prefix='/api/search_opportunities')
app.include_router(search_oppo_controller.search_opportunities_router, prefix='/api/search_opportunities/opportunities')
app.include_router(hotel_prices_controller.prices_router, prefix='/api/search_opportunities/prices')
app.include_router(booking_controller.bookings_router, prefix='/api/search_opportunities/bookings')
app.include_router(booking_controller.bookings_router, prefix='/api/search_opportunities/booking')
app.include_router(hotels_names_controller.hotels_names_router, prefix='/api/search_opportunities/hotels_names')
app.include_router(manual_search_controller.search_one_hotel_opportunities_router,
                   prefix='/api/search_opportunities/one_hotel')

uvicorn.run(app, host='192.168.1.2', port=8001, access_log=False)
