from dbConnections import sql_db_connection as connection


def inset_hotel_data(hotel_data):
    """
    Inset hotel data to database
    :param hotel_data: the data to inset
    :return: the new row id
    """
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
    """
    Inset hotels images to database
    :param hotel_id: the hotel id to insert
    :param img: the hotel image to insert
    :param desc: the img description to insert
    :return: None
    """
    insert_images_procedure = "dbo.insertImg"
    image_values = (hotel_id, img, desc)
    connection.exec_stored_procedure(insert_images_procedure, image_values)


def insert_room_data(room_data):
    """
    Inset room data to database
    :param room_data: the room data to insert
    :return: the new row id
    """
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
    """
    insert child age into the database
    :param room_id: the room id to insert
    :param age: the age to insert
    :return: None
    """
    insert_cnn_ages_procedure = "dbo.insertCnnAge"
    cnn_age_values = (room_id, age)
    connection.exec_stored_procedure(insert_cnn_ages_procedure, cnn_age_values)


def insert_search_setting(stars, search_key):
    """
    insert search settings into the database
    :param stars: the number of stars to insert
    :param search_key: the city and country to insert
    :return: Nome
    """
    insert_search_settings_procedure = "dbo.insertSearchSetting"
    search_settings_values = (search_key, stars)
    connection.exec_stored_procedure(insert_search_settings_procedure, search_settings_values)


def select_search_setting():
    """
    select search settings from the database
    :return: the selected search settings
    """
    search_settings_view = "dbo.selectSearchSettings"
    return connection.exec_view(search_settings_view)


def select_statistically_information_by_month(month_number, year_number, segment_name):
    view_name = ""
    match month_number:
        case 1:
            view_name = "dbo.selectJanuaryData"
        case 2:
            view_name = "dbo.selectFebruaryData"
        case 3:
            view_name = "dbo.selectMarchData"
        case 4:
            view_name = "dbo.selectAprilData"
        case 5:
            view_name = "dbo.selectMayData"
        case 6:
            view_name = "dbo.selectJuneData"
        case 7:
            view_name = "dbo.selectJulyData"
        case 8:
            view_name = "dbo.selectAugustData"
        case 9:
            view_name = "dbo.selectSeptemberData"
        case 10:
            view_name = "dbo.selectOctoberData"
        case 11:
            view_name = "dbo.selectNovemberData"
        case 12:
            view_name = "dbo.selectDecemberData"
        case _:
            return ValueError("Month number is not in the range")

    return connection.exec_view(view_name)
