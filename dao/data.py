from helper.utils import read_config
import requests


class Data(object):
    def __init__(self):
        self.__config = read_config()
        self.__num = 0
        self.__current_data = None
        self.__future_data = None

    def __get_current_data(self) -> bool:
        if len(self.__config['citys']) == 0:
            return False
        try:
            resp = requests.get(
                'https://tianqiapi.com/api?version=v6&appid={0}&appsecret={1}&city={2}'.format(self.__config['id'], self.__config['secret'], self.__config['citys'][self.__num]))
            self.__current_data = resp.json()
            return True
        except:
            return False

    def __get_future_data(self) -> bool:
        if len(self.__config['citys']) == 0:
            return False
        try:
            resp = requests.get(
                'https://tianqiapi.com/api?version=v1&appid={0}&appsecret={1}&city={2}'.format(self.__config['id'], self.__config['secret'], self.__config['citys'][self.__num]))
            self.__future_data = resp.json()
            return True
        except:
            return False

    def refresh(self) -> bool:
        current = self.__get_current_data()
        future = self.__get_future_data()
        return current and future

    def increase(self) -> None:
        self.__num = (self.__num+1) % len(self.__config['citys'])

    def get_current_data(self) -> dict:
        return self.__current_data

    def get_future_data(self) -> dict:
        return self.__future_data
