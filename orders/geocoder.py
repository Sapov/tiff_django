import requests, os
from geopy.geocoders import Yandex
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Geocoder:
    '''
    Определите координаты здания по адресу "бул. Мухаммед Бин Рашид, дом 1":
    https://geocode-maps.yandex.ru/1.x/?apikey=YOUR_API_KEY&geocode=бул+Мухаммед+Бин+Рашид,+дом+1&format=json

    '''
    GEOCODER_API_YANDEX = os.getenv('GEOCODER_API_YANDEX')
    user_agent = 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'

    def __init__(self):
        self.get_url = None

    @classmethod
    def geopy_address_to_coordinates(self, address: str) -> tuple:
        '''Геокодер Адрес В координаты'''
        geolocotor = Yandex(api_key=self.GEOCODER_API_YANDEX, user_agent=self.user_agent)
        location = geolocotor.geocode(address)
        return location.latitude, location.longitude

    @classmethod
    def geopy_coordinates_to_address(self, latitude: float, longitude: float) -> str:
        '''Геокодер Кординаты в адрес'''
        geolocator = Yandex(api_key=self.GEOCODER_API_YANDEX, user_agent=self.user_agent)
        location = geolocator.reverse((latitude, longitude))
        return location.address

    def run(self):
        self.geopy_coordinates_to_address(51.704928, 39.168864)

    # Geocoder('г. Воронеж, ул. Лизюкова, 53').run()


if __name__ == '__main__':
    print(Geocoder().geopy_address_to_coordinates('г. Воронеж, Никитинская, 3'))
    # print(Geocoder().geopy_coordinates_to_address(51.669467, 39.202811))

    # ______test_____
    # assert Geocoder().geopy_address_to_coordinates('г. Воронеж, проспект патриотов, 33Б') == (51.64096, 39.126428)
    # assert Geocoder().geopy_coordinates_to_address(51.669467, 39.202811) == 'Никитинская улица, 3, Воронеж, Россия'
