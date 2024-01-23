

from dbConnections import sql_db_connection as connection


def inset_hotel_data(hotel_data):
    insert_address = "dbo.insertAddress"
    address_values = (hotel_data.hotel_address, hotel_data.hotel_phone,
                      hotel_data.hotel_fax, hotel_data.hotel_city, hotel_data.hotel_country)
    address_id = connection.exec_stored_procedure(insert_address, address_values)[0]
    address_id = int(address_id)
    insert_position = "dbo.insertPosition"
    position_values = (hotel_data.hotel_latitude, hotel_data.hotel_longitude, hotel_data.hotel_pip)
    position_id = connection.exec_stored_procedure(insert_position, position_values)[0]
    position_id = int(position_id)
    insert_hotel = "dbo.insertHotel"
    hotel_values = (hotel_data.hotel_name, hotel_data.hotel_code, hotel_data.hotel_stars, address_id, position_id)
    hotel_id = connection.exec_stored_procedure(insert_hotel, hotel_values)
    return hotel_id


def insert_images(hotel_id, img, desc):
    insert_images_procedure = "dbo.insertImg"
    image_values = (hotel_id, img, desc)
    connection.exec_stored_procedure(insert_images_procedure, image_values)


def insert_room_data(room_data):
    insert_room = "dbo.insertRoom"
    room_values = (room_data.hotel_id, room_data.price, room_data.desc, room_data.sysCode, room_data.check_in,
                   room_data.check_out, room_data.nights, room_data.b_token, room_data.limit_date, room_data.remarks)
    print(room_values)
    room_id = connection.exec_stored_procedure(insert_room, room_values)[0]
    room_id = int(room_id)
    insert_mata_data = "dbo.insertMetadata"
    mata_values = (room_id, room_data.code, room_data.code_description)
    connection.exec_stored_procedure(insert_mata_data, mata_values)


def insert_cnn_ages(room_id, age):
    insert_cnn_ages_procedure = "dbo.insertCnnAge"
    cnn_age_values = (room_id, age)
    connection.exec_stored_procedure(insert_cnn_ages_procedure, cnn_age_values)


def insert_search_setting(stars, search_key):
    insert_search_settings_procedure = "dbo.insertSearchSetting"
    search_settings_values = (search_key, stars)
    connection.exec_stored_procedure(insert_search_settings_procedure, search_settings_values)

