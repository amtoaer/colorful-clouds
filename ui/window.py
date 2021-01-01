from tkinter.constants import TOP
from ui.config import Config
from dao.data import Data
from helper.utils import get_images
import tkinter
from tkinter import Button, Frame, Label
import threading


class Window(tkinter.Tk):
    '''程序主窗口'''

    def __init__(self):
        super().__init__()
        self.title('天气预报')
        self.resizable(width=0, height=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Frame
        self.top_frame = Frame(self)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.bottom_frame = Frame(self)
        # 按钮
        self.next = Button(self.top_frame, text='切换')
        self.setting = Button(self.top_frame, text='设置')
        self.refresh = Button(self.top_frame, text="刷新")
        # 数据源
        self.dao = Data()
        self.images = get_images()
        # Label
        self.current_weather_text = tkinter.StringVar()
        self.current_weather_label = Label(self.bottom_frame, image=None)
        self.future_temperature_labels = [
            tkinter.StringVar() for _ in range(7)]
        self.future_weather_labels = [
            Label(self.bottom_frame, image=None, textvariable=self.future_temperature_labels[i], compound=TOP, width=80) for i in range(7)]

    def __draw(self):
        # Label充当占位符
        Label(self.top_frame).grid(row=0, column=0, columnspan=6, sticky='NS')
        self.next.grid(row=0, column=7, sticky='NS', padx=20, pady=20)
        self.refresh.grid(row=0, column=8, sticky='NS', pady=20)
        self.setting.grid(row=0, column=9, sticky='NS', padx=20, pady=20)
        self.current_weather_label.grid(
            row=0, column=0, rowspan=2, columnspan=7)
        Label(self.bottom_frame, textvariable=self.current_weather_text).grid(
            row=0, column=8, columnspan=7, sticky='NWSE')
        for i in range(7):
            self.future_weather_labels[i].grid(row=1, column=7+i)
        self.top_frame.grid(row=0, column=0, sticky='WE')
        self.bottom_frame.grid(row=1, column=0, sticky='WE')

    def __bind_event(self):
        self.refresh.configure(command=self.refresh_in_thread)
        self.next.configure(command=self.__next)
        self.setting.configure(command=self.__setting)

    def __next(self):
        self.dao.increase()
        self.refresh_in_thread()

    def refresh_in_thread(self):
        threading.Thread(target=self.__refresh).start()

    def __setting(self):
        config = self.dao.get_config()
        Config(config, self)

    def __refresh(self) -> bool:
        success = self.dao.refresh()
        if not success:
            print('更新数据失败，可能因为城市列表为空或网络错误，请修正错误后重试')
            return False
        current_data = self.dao.get_current_data()
        future_data = self.dao.get_future_data()
        self.current_weather_label.configure(
            image=self.images[current_data['wea_img']][0])
        self.current_weather_text.set('''
        城市：{}    天气：{}
        温度：{}°C  最高温度：{}°C
        最低温度：{}°C  风向：{}
        风速：{}    pm2.5：{}
        空气质量：{}'''.format(current_data['city'], current_data['wea'], current_data['tem'], current_data['tem1'], current_data['tem2'], current_data['win'], current_data['win_speed'], current_data['air_pm25'], current_data['air_level']))
        for i in range(7):
            data = future_data['data'][i]
            self.future_temperature_labels[i].set(
                '{}~{}'.format(data['tem2'], data['tem1']))
            self.future_weather_labels[i].configure(
                image=self.images[data['wea_img']][1])
        return True

    def __show(self):
        self.mainloop()

    def run(self):
        self.__draw()
        self.__bind_event()
        first_refresh_success = self.__refresh()
        if first_refresh_success:
            self.__show()
