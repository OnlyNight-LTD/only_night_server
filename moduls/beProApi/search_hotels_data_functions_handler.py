import pycountry


def calculate_number_of_nights(check_in, check_out):
    """
    calculate number of nights between two dates
    :param check_in: the first date
    :param check_out: the second date
    :return: the number of nights
    """
    print('in calculate_number_of_night', check_in, check_out, type(check_in))
    return (check_out - check_in).days


def get_country_name(search_key):
    """
    Get only the country name from search key
    :param search_key: a str of city and country names
    :return: only the country name
    """
    country_name = search_key.split(',')
    return country_name[1] if len(country_name) == 2 else country_name[0]


def convert_country_name_to_code(country_name):
    """
    Convert country name to code
    :param country_name: the country name to convert
    :return: the country code
    """
    if country_name[0] == " ":
        country_name = country_name[1:]
    for country in pycountry.countries:
        if country.name.lower() == country_name.lower():
            return country.alpha_2


def build_room(num_adults, num_children, room_token, cnn_ages=None):
    """
    Build the schema room according to the given parameters
    :param num_adults: the number of adults in the room
    :param num_children: the number of children in the room
    :param cnn_ages: optional - the age of the children if num_children != 0
    :return: the schema room
    """
    rooms = []
    max_cnn = 4
    room = {}
    sys_room_code = "O" + str(num_adults) + "A" + str(num_children) + "C"
    room["SysRoomCode"] = sys_room_code
    room["NumRoom"] = 1
    room["NumCots"] = 0
    room["NumPax"] = num_adults + num_children
    room["NumAdt"] = num_adults
    room["NumCnn"] = num_children
    if num_children == 0:
        room["CnnAge1"] = 0
        room["CnnAge2"] = 0
        room["CnnAge3"] = 0
        room["CnnAge4"] = 0
    else:
        for i in range(max_cnn):
            if i < len(cnn_ages):
                room["CnnAge" + str(i)] = cnn_ages[i - 1]
            else:
                room["CnnAge" + str(i + 1)] = 0
    if room_token != "":
        room["RoomToken"] = room_token
    rooms.append(room)
    return rooms
