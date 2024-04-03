from datetime import datetime
from moduls.beProApi import search_one_hotel, bepro_api
from dbConnections import sql_insert_queries as sql_queries
from moduls.beProApi.reservation_step_1 import reservation_step_1_request
from moduls.beProApi.reservation_step_2 import reservation_step_2
from pydantic import BaseModel


class SearchOneHotelPostBody(BaseModel):
    city: str
    hotel_name: str
    stars: float
    check_in: str
    check_out: str
    price: float
    location: float


def be_pro_booking(hotel_name, stars, check_in, check_out, segment, radius, arbitrage, room_token, hotel_code):
    """
    The main function of the booking room  by bePro
    :param hotel_name: the hotel name of the room to buy
    :param stars: the number of stars of the room to buy
    :param check_in: the check-in date
    :param check_out: the check-out date
    :param segment: the city of the room to buy
    :param radius: the radius of the room to buy
    :param arbitrage: the profit of room to buy
    :return: the booking room
    """
    try:
        room = search_one_hotel.be_pro_manual_search(hotel_name, stars, check_in, check_out, segment, radius, arbitrage,
                                                     '', '')

    except Exception as e:
        raise f"An error occurred in search_hotels function : {e}"
    for r in room.get('Hotels')[0].get('Rooms'):
        limit_date = r.get('LimitDate')
        l_date = datetime.strptime(limit_date[: 10], "%Y-%m-%d")
        # today = datetime.now().strptime(limit_date[: 10], "%Y-%m-%d")
        if l_date > datetime.now():
            room = r
    # room = room.get('Hotels')[0].get('Rooms')[0]
    (item_code, item_desc, b_token, check_in, check_out, nights, price, meta_data,
     city) = extract_data_from_room_data(room)
    room_for_reservation = search_one_hotel.be_pro_manual_search(hotel_name, stars, check_in, check_out, segment,
                                                                 radius,
                                                                 arbitrage, b_token,
                                                                 item_code)
    for r in room_for_reservation.get('Hotels')[0].get('Rooms'):
        limit_date = r.get('LimitDate')
        l_date = datetime.strptime(limit_date[: 10], "%Y-%m-%d")
        if l_date > datetime.now():
            room_for_reservation = r
    (item_code, item_desc, b_token, check_in, check_out, nights, price, meta_data,
     city) = extract_data_from_room_data(room_for_reservation)
    info_grass_rate = bepro_api.check_charge_condition(b_token, price, check_out)
    if info_grass_rate[0]:
        return {"massage": f"Warning the price has changed! The current price - {info_grass_rate[1]} "
                           f"The previous price - {price}"}
    # return {"massage": f"The price has not changed {price}"}
    response = reservation_step_1_request(item_code, item_desc, b_token, check_in, check_out, nights, price)
    if response.get('query').get('beproError'):
        return response
    order_id, order_segment_id, order_seg_id, list_of_order_segment_id, booking_order_segment_id = extract_data_from_reservation_step_1(
        response.get('query'), response.get('order'))
    print('reservation step 1: ', response)
    reservation_step_2_request = reservation_step_2(item_code, item_desc, b_token, check_in, check_out, nights,
                                                    price, order_segment_id, order_seg_id,
                                                    list_of_order_segment_id, order_id)
    print('reservation step 2: ', reservation_step_2_request)
    reservation_data = extract_reservation_data_for_db(item_code, item_desc, check_in, check_out, nights,
                                                       order_id, price, order_segment_id, order_seg_id, meta_data,
                                                       city)
    sql_queries.insert_reservation(reservation_data)
    return reservation_data


def extract_data_from_room_data(room):
    check_in = room.get('CheckIn')
    b_token = room.get('BToken')  # 41
    (item_code, item_desc, city) = extract_data_from_room_token(b_token)

    check_out = room.get('CheckOut')
    nights = room.get('Nights')
    price = room.get('Price')
    meta_data = room.get('MetaData')
    return item_code, item_desc, b_token, check_in, check_out, nights, price, meta_data, city


def extract_data_from_room_token(room_token):
    print('room_token: ', room_token)
    room_token_data = room_token.split("‡")
    return room_token_data[4], room_token_data[49], room_token_data[42]


def extract_data_from_reservation_step_1(query, order):
    """
    the function extract the data from reservation step 1 for the reservation step 2 request
    :return: OrderId, OrderSegmentId, OrderSegId, ListOfOrderSegmentId, bookingOrderSegmentId
    """
    order_id = order.get('orderId')
    order_segment_id = query.get('orderSegmentId')
    order_seg_id = query.get('orderSegId')
    list_of_order_segment_id = query.get('listOfOrderSegmentId')
    booking_order_segment_id = query.get('orderSegmentId')
    return order_id, order_segment_id, order_seg_id, list_of_order_segment_id, booking_order_segment_id


def extract_reservation_data_for_db(item_code, item_desc, check_in, check_out, nights,
                                    order_id, price, order_segment_id, order_seg_id, meta_data, city):
    return item_code, item_desc, check_in, check_out, nights, order_id, price, order_segment_id, order_seg_id, \
        meta_data['Code'], meta_data['Desc'], city
