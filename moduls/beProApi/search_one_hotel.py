from datetime import datetime

from moduls.beProApi import bepro_api
from dbConnections import sql_select_queries
from moduls.algorithm import opportunity_response_handler


def search_one_hotel(search_id, hotel_name, stars, check_in, check_out, room_token, hotel_code, radius, oppo_state):
    """
    Call the bePro_api to search the hotel
    :param search_id: the id of the city of the hotel
    :param hotel_name: the name of the hotel to search
    :param stars: the number of stars of hotel to search
    :param check_in: the date of the check_in
    :param check_out: the date of the check_out
    :param radius: the radius of the search
    :return: all possible hotels rooms
    """
    if isinstance(check_in, str):
        check_in = datetime.strptime(check_in[: 10], "%Y-%m-%d")
        check_out = datetime.strptime(check_out[: 10], "%Y-%m-%d")

    hotels = bepro_api.search_hotels("hotel", search_id, hotel_name, stars, check_in, check_out, room_token, hotel_code,
                                     radius, oppo_state)
    print("hotels: ", len(hotels))

    return hotels if hotels else []


def check_if_segment(city):
    """
    Check if the given city is a segment which is under surveillance
    :param city: the city to check
    :return: True if the city is under surveillance, False otherwise
    """
    search_settings = sql_select_queries.select_search_setting()

    for search_setting in search_settings:

        search_setting = search_setting[1].split(",")[0]
        if city.lower() in search_setting.lower() or search_setting.lower() in city.lower():
            return True

    return False


def convert_city_to_search_setting(city):
    for search_setting in sql_select_queries.select_search_setting():
        search_setting = search_setting[1].split(",")[0]
        if city.lower() in search_setting.lower() or search_setting.lower() in city.lower():
            return search_setting

    return "Undefined"


def get_search_settings_id(city):
    """
    Get the id of the search settings for a given city from database
    :param city: the city to check the search settings id
    :return: the id of the search settings for a given city
    """
    search_settings = sql_select_queries.select_search_setting()

    for search_setting in search_settings:
        if city in search_setting[1]:  # search setting[1] == search setting name
            return search_setting[0]  # search setting[0] == search setting id


def be_pro_manual_search(hotel_name, stars, check_in, check_out, segment, radius, arbitrage, room_token, hotel_code):
    if check_if_segment(segment):
        segment = convert_city_to_search_setting(segment)
        if segment == "Undefined":
            return convert_result_to_response_format([])

    calc_profit_state = False
    search_id = get_search_settings_id(segment)
    dict_segment = {"Name": segment, "Stars": stars}

    if arbitrage == 0 and check_if_segment(segment):
        calc_profit_state = True

    if arbitrage == 0:
        state = False if hotel_name == "" else True

        rooms_ids = search_one_hotel(search_id, segment, stars, check_in, check_out, room_token, hotel_code, radius,
                                     False)
        return general_search(rooms_ids, hotel_name, dict_segment, state, calc_profit_state=calc_profit_state)

    if not check_if_segment(segment):
        return "This city is not under surveillance"

    state = False if hotel_name == "" else True

    rooms_ids = search_one_hotel(search_id, segment, stars, check_in, check_out, room_token, hotel_code, radius, False)

    return general_search(rooms_ids, hotel_name, dict_segment, state, calc_profit_state=True)


def general_search(hotels, hotel_name, segment, one_hotel_state, calc_profit_state):
    res_hotels = []
    for hotel in hotels:

        item = hotel.get('Item')
        address_info = hotel.get('AddressInfo')
        position = hotel.get('Position')
        images = hotel.get('Images')
        res_item = opportunity_response_handler.create_item(-1, item.get('UniqueName'), item.get('Code'),
                                                            item.get('Star'),
                                                            address_info.get('Address'),
                                                            address_info.get('City'),
                                                            address_info.get('Country'),
                                                            address_info.get('Phone'), address_info.get('Fax'),
                                                            position.get('Latitude'),
                                                            position.get('Longitude'), position.get('PIP'))

        res_item = opportunity_response_handler.add_images(res_item, images)
        rooms = hotel.get("RoomClasses")

        response_rooms = processes_rooms_response(rooms, segment, calc_profit_state)

        if (one_hotel_state and item.get('UniqueName') in hotel_name) or not one_hotel_state:
            res_hotel = opportunity_response_handler.create_hotel(res_item, response_rooms)
            res_hotels.append(res_hotel)

    return convert_result_to_response_format(res_hotels)


def processes_rooms_response(rooms_from_be_pro, segment, calc_profit_state):

    response_rooms = []

    for room in rooms_from_be_pro:

        room_data = room.get('HotelRooms')[0]
        code = room.get('Board').get('Basis').get('Code')
        desc = room.get('Board').get('Basis').get('Desc')
        limit_date = room.get("CXL").get('LimitDate')

        limit_date = "" if limit_date is None else limit_date

        res_room = opportunity_response_handler.create_room(-1, room.get('Price').get('USD'),
                                                            room_data.get('Desc'),
                                                            room_data.get('SysCode'), room.get('CheckIn'),
                                                            room.get('CheckOut'),
                                                            room.get('Nights'), room_data.get('BToken'),
                                                            limit_date, room.get('Remarks'),
                                                            code, desc)

        if calc_profit_state:
            res_room = opportunity_response_handler.calculate_profit(segment, res_room)

        response_rooms.append(res_room)

    return response_rooms


def convert_result_to_response_format(result):
    return {"Hotels": result}
