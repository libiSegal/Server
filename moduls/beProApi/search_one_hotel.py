from datetime import datetime
from moduls.beProApi import bepro_api
from dbConnections import sql_select_queries
from moduls.algorithm import statisticall_information, opportunitiesFinder
from moduls.algorithm import opportunity_response_handler
from moduls.objects.response_opportunity_obj import ResponseOpportunityHotel


def search_one_hotel(search_id, hotel_name, stars, check_in, check_out, radius):
    """
    Call the bePro_api to search the hotel
    :param search_id: the id of the city of the hotel
    :param hotel_name: the name of the hotel to search
    :param stars: the number of stars of hotel to search
    :param check_in: the date of the check_in
    :param check_out: the date of the check_out
    :param radius: the radius of the search
    :return: all possible rooms
    """
    check_in = datetime.strptime(check_in, "%Y-%m-%d")
    check_out = datetime.strptime(check_out, "%Y-%m-%d")
    room_ids = bepro_api.search_hotels("hotel", search_id, hotel_name, stars, check_in, check_out, radius)
    print("room_ids: ", room_ids)
    if room_ids:
        return room_ids
    else:
        return []


# def get_rooms_prices_from_db(ids):
#     """
#     Get the possible room prices from the database
#     :param ids: the ids of the rooms
#     :return:the prices and check in date of the rooms
#     """
#     return sql_select_queries.select_room_price_by_id(ids)


# def calculate_opportunities(room_prices, segment, last_year, arbitrage=50):
#     """
#     Calculate the opportunities for the given rooms
#     :param room_prices: the prices of the rooms
#     :param segment: the city of the hotel
#     :param last_year: the year to camper the prices
#     :param arbitrage: the profit we want to get
#     :return:
#     """
#     opportunities = []
#     month = get_the_check_in_month(room_prices[0])
#     history_data = statisticall_information.get_statistically_information_for_segment(segment, month, last_year)
#     if len(history_data) != 0:
#         history_price = statisticall_information.get_adr_for_month(history_data)
#         for room in room_prices:
#             print("price", room[1], "history_price", history_price)
#             if room[1] + arbitrage <= history_price:
#                 opportunities.append(room[0])
#     return opportunities


def get_the_check_in_month(check_in_room):
    """
    Extract the month from the given check in date
    :param check_in_room:the check in date to extract the month
    :return:the number month
    """
    return datetime.strptime(check_in_room[2], "%Y-%m-%d %H:%M:%S").month


# def get_rooms_data_from_db(ids):
#     """
#     Get the data of room from the database
#     :param ids: the ids of the rooms
#     :return: all the date about the room
#     """
#     return sql_select_queries.select_data_of_opportunities(ids)


# def select_hotel_data(room):
#     """
#     Get the all data of the hotel given an id from the database
#     :param room: the id of the hotel
#     :return: all the data of the hotel
#     """
#     hotel_id = room[1]
#     return sql_select_queries.select_data_of_hotels_by_id(hotel_id)


# def fill_hotel_data(data_hotel):
#     """
#     Fill the hotel data into the hotel object
#     :param data_hotel: the data of the hotel
#     :return: a hotel object
#     """
#     images = []
#     for data in data_hotel:
#         img = opportunity_response_handler.create_img(data[-2], data[-1])
#         images.append(img)
#     item = opportunity_response_handler.create_item(*data_hotel[0][:-2])
#     item = opportunity_response_handler.add_images(item, images)
#     return item


# def fill_room_data(segment, data_rooms):
#     """
#     Fill the room data into the room object
#     :param segment: the city to check the profit
#     :param data_rooms: the data of the rooms
#     :return: room objects
#     """
#     cheapest_room = opportunity_response_handler.find_cheapest_rooms(data_rooms)
#     rooms = []
#     for data in cheapest_room:
#         data.pop(1)  # remove the hotel id
#         room = opportunity_response_handler.create_room(*data)
#         room = opportunity_response_handler.calculate_profit(segment, room)
#         rooms.append(room)
#     return rooms


# def extract_data_from_sql_type(data):
#     """
#     Extract the data from the pysql type to list
#     :param data: the sql data
#     :return: the data by list type
#     """
#     return [list(item) for item in data]


# def get_last_year():
#     """
#     Get the last year
#     :return: the last year
#     """
#     return datetime.now().year - 1


def check_if_segment(city):
    """
    Check if the given city is a segment which is under surveillance
    :param city: the city to check
    :return: True if the city is under surveillance, False otherwise
    """
    search_settings = sql_select_queries.select_search_setting()

    for search_setting in search_settings:
        if city.lower() in search_setting[1].lower():
            return True

    return False


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


# def check_correctness_of_the_hotel_name(hotel_name, hotel_name_to_check):
#     """
#     Check if the hotel name is correctly the same that given
#     :param hotel_name: the given hotel name
#     :param hotel_name_to_check: the database hotel name to check
#     :return: True if the hotel name is correctly the same that given
#     """
#     return hotel_name in hotel_name_to_check


# def bePro_search_one(search_id, hotel_name, stars, check_in, check_out, segment, arbitrage):
#     """
#     The main function of the search one hotel date by bePro
#     :param search_id: the db table id of the hotel city
#     :param hotel_name: the hotel name to search
#     :param stars: the number of stars of the hotel to search
#     :param check_in: the check-in date
#     :param check_out: the check-out date
#     :param segment: the city of the hotel to search
#     :param arbitrage: the profit of the hotel to search
#     :return: all opportunities
#     """
#     try:
#         hotel_name = hotel_name + " " + segment
#         rooms_ids = search_one_hotel(search_id, hotel_name, stars, check_in, check_out, radius=1)
#
#         if rooms_ids:
#             rooms_ids = list(set(rooms_ids))
#             prices = get_rooms_prices_from_db(rooms_ids)
#             last_year = get_last_year()
#             segment = {"Id": search_id, "Name": segment}
#
#             if arbitrage == 0:
#                 oppo = rooms_ids
#             else:
#                 oppo = calculate_opportunities(prices, segment, last_year, arbitrage)
#
#             if isinstance(oppo, list) and len(oppo) > 0:
#                 oppo_data = get_rooms_data_from_db(oppo)
#                 hotel_data = select_hotel_data(oppo_data[0])
#                 oppo_data = extract_data_from_sql_type(oppo_data)
#                 item = fill_hotel_data(hotel_data)
#                 if check_correctness_of_the_hotel_name(hotel_name, hotel_data[0][1]):
#                     rooms = fill_room_data(segment, oppo_data)
#                     hotel = ResponseOpportunityHotel(item, rooms)
#                     return {"Hotels": [hotel.body]}
#
#                 else:
#                     "No opportunities exist for this hotel"
#             else:
#                 return "No opportunities exist for these values"
#         else:
#             return "No information exists for these values"
#     except Exception as e:
#         return Exception(f"Something went wrong in 'bePro_search_one' function.\n {e}")


def process_hotels_data(segment, rooms_id, hotel_name):
    """
        Process a segment of data related to opportunities and extract relevant hotel information.
        :param: segment (str): A segment of data containing information about opportunities.
        :return list: A list of hotels extracted from the segment data.
        """
    hotels = []
    opportunities_ids = rooms_id

    if not isinstance(opportunities_ids, int) and len(opportunities_ids) > 0:
        opportunities = sql_select_queries.select_data_of_opportunities(list(set(opportunities_ids)))
        hotels_ids = opportunitiesFinder.group_opportunities_hotels(opportunities)
        hotels_data = opportunitiesFinder.get_opportunities_hotels(hotels_ids)
        grouped_hotels = opportunitiesFinder.group_hotels_by_id(hotels_data)
        unique_hotels = opportunitiesFinder.remove_duplicate_data(grouped_hotels)
        if hotel_name != "":
            unique_hotels = [get_specific_hotel(unique_hotels, hotel_name)]
        opportunities_list = opportunity_response_handler.extract_opportunities_from_db_type(opportunities)
        hotels_with_rooms = opportunitiesFinder.match_room_hotel(unique_hotels, opportunities_list)
        for hotel_data in hotels_with_rooms.values():
            hotel = opportunity_response_handler.process_hotel_data(segment, hotel_data)
            if len(hotel.get("Rooms")) > 0:
                hotels = opportunity_response_handler.check_hotel_is_exists(hotel, hotels)
    return hotels


def get_specific_hotel(hotels, hotel_name):
    for hotel in hotels:
        if hotel[1] == hotel_name:
            return hotel


def get_opportunities_response(segment, rooms_id, hotel_name):
    """
    This function gets the opportunities and organizes them into a response object
    :return: The response object
    """

    hotels = process_hotels_data(segment, rooms_id, hotel_name)
    response = {"Hotels": hotels}

    return response


def bePro_manual_search(hotel_name, stars, check_in, check_out, segment, radius, arbitrage):
    if not check_if_segment(segment):
        return "This city is not under surveillance"
    segment = segment.lower()
    segment = segment.capitalize()
    search_id = get_search_settings_id(segment)
    #if hotel_name != "":
    rooms_ids = search_one_hotel(search_id, segment, stars, check_in, check_out, radius)
    segment = {"Name": segment}
    return get_opportunities_response(segment, rooms_ids, hotel_name)
    # else:
    #     return bePro_search_one(search_id, hotel_name, stars, check_in, check_out, segment, arbitrage)
