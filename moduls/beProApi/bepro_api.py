from moduls import google_maps_api
from moduls.beProApi import charge_condition
from moduls.jsonHandler import json_reader as jdr
from moduls.beProApi import bepro_definitions as defn
from moduls.beProApi import search_hotels_functions as search_htl
from moduls.beProApi import search_one_hotel
from moduls.beProApi import search_hotels_data_functions_handler as search_hotels_data

URL = 'https://pub_srv.beprotravel.net/BePro'


def search_hotels(search_type, search_id, search_key, stars, check_in, check_out, room_token, hotel_code, radius=5,
                  oppo_state=True):
    """
    this function is used to search hotels by bePro api and inserted the response into the database
    :param search_id: the db table id of the hotel city
    :param search_type: show if search one hotel ro more
    :param radius: the radius of distance to search
    :param search_key: the city and country of the hotel you want to search
    :param stars: the number of stars of the hotel you want to search
    :param check_in: the date of the checkin
    :param check_out: the date of the checkOut
    :return:None
    """
    print('in bepro_api search_hotels')
    print("search type:", search_type, "search_id:", search_id, "search_key:", search_key,
          "stars:", stars, "check_in:", check_in, "check_out:", check_out, "radius:", radius)
    try:
        country_code = ""
        geo_code = google_maps_api.get_geo_code(search_key)
        nights = search_hotels_data.calculate_number_of_nights(check_in, check_out)

        if room_token != "":
            rooms = search_hotels_data.build_room(defn.numbers_adults, defn.numbers_children, room_token, defn.cnn_age)
            suppliers_search, country_code = extract_suppliers_search_from_room_token(room_token)
            unique_key = search_htl.search_post_request_for_reservation(search_key, country_code, geo_code,
                                                                        str(check_in),
                                                                        nights, rooms, stars,
                                                                        radius, hotel_code, suppliers_search)
        else:
            rooms = search_hotels_data.build_room(defn.numbers_adults, defn.numbers_children, room_token, defn.cnn_age)
            unique_key = search_htl.search_post_request(search_key, country_code, geo_code, str(check_in),
                                                        nights, rooms, stars,
                                                        radius)
        print("unique_key:", unique_key)
        urls_hotels = search_htl.get_the_hotels_details(unique_key)
        search_htl.download_hotels_data(urls_hotels)
        if not oppo_state:
            files_data = search_htl.get_data_from_bePro_files()
            jdr.delete_jsons_files('files')
            return files_data
        rooms_ids = search_htl.insert_hotels_data_into_db(search_id)
        jdr.delete_jsons_files('files')
        return rooms_ids
    except Exception as e:
        return f"An error occurred in search_hotels function : {e}"


def check_charge_condition(room_token, price, check_out):
    """
    Checks if the room price is charged
    :param room_token: the room token to check charge condition
    :param price: the original price of the room
    :return: true if the room is charged, false otherwise
    """
    print('Checking charge condition', room_token)
    (supplier_city_code, supplier_code, item_code, check_in,
     nights) = charge_condition.extract_data_from_room_token(room_token)
    print('after charge_condition.extract_data_from_room_token')
    response = charge_condition.charge_condition_request(supplier_code, supplier_city_code, check_in, check_out, nights,
                                                         item_code, room_token)
    info_gross_rate = charge_condition.extract_infoGrossRate(response)
    if info_gross_rate > price:
        return True, info_gross_rate
    return False, price


def extract_suppliers_search_from_room_token(room_token):
    room_token_data = room_token.split("‡")
    print('btoken in extract_suppliers_search_from_room_token:', room_token)
    if len(room_token_data) > 3:
        print(' 2room_token_data:', len(room_token_data), room_token_data[len(room_token_data) - 3])
        suppliers_search = room_token_data[3]
        country_code = room_token_data[len(room_token_data) - 3]
        return suppliers_search, country_code
    return '', ''
