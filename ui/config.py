import tkinter
from tkinter.constants import END, EXTENDED
from json import dumps


class Config(tkinter.Toplevel):
    def __init__(self, config: dict, father):
        super().__init__()
        self.title('设置')
        self.resizable(0, 0)
        self.__config = config
        self.appID = tkinter.StringVar(value=self.__config['id'])
        self.appSecret = tkinter.StringVar(value=self.__config['secret'])
        self.city_to_insert = tkinter.StringVar()
        self.city_list = None
        self.add = None
        self.delete = None
        self.save = tkinter.Button(self, text='保存并关闭')
        self.father = father
        self.__draw()
        self.__bind_event()

    def __draw(self):
        api_config = tkinter.LabelFrame(self, text='API设置')
        tkinter.Label(api_config, text='appid:').grid(row=0, column=0)
        tkinter.Entry(api_config, textvariable=self.appID).grid(
            row=0, column=1)
        tkinter.Label(api_config, text='appsecret:').grid(row=1, column=0)
        tkinter.Entry(api_config, textvariable=self.appSecret).grid(
            row=1, column=1)
        api_config.grid(row=0, column=0, sticky='WE')
        city_config = tkinter.LabelFrame(self, text='城市设置')
        tkinter.Label(city_config, text='请输入不带市和区的地区名').grid(
            row=0, column=0)
        tkinter.Entry(city_config, textvariable=self.city_to_insert).grid(
            row=1, column=0)
        self.add = tkinter.Button(city_config, text='+')
        self.delete = tkinter.Button(city_config, text='-')
        self.add.grid(row=1, column=1)
        self.city_list = tkinter.Listbox(
            city_config, width=26, selectmode=EXTENDED)
        for city in self.__config['citys']:
            self.city_list.insert(END, city)
        self.city_list.grid(row=2, column=0)
        self.delete.grid(row=2, column=1)
        city_config.grid(row=1, column=0)
        self.save.grid(row=2, column=0)

    def __bind_event(self):
        self.add.configure(command=self.__add)
        self.delete.configure(command=self.__delete)
        self.save.configure(command=self.__save)

    def __delete(self):
        for index in reversed(self.city_list.curselection()):
            self.city_list.delete(index)

    def __add(self):
        city_to_insert = self.city_to_insert.get()
        if not city_to_insert.isspace():
            self.city_list.insert(END, city_to_insert)

    def __save(self):
        self.__config['id'] = self.appID.get()
        self.__config['secret'] = self.appSecret.get()
        citys = []
        for city in self.city_list.get(0, self.city_list.size()):
            citys.append(city)
        self.__config['citys'] = citys
        with open('./config.json', 'w') as f:
            f.write(dumps(self.__config, ensure_ascii=False))
        # 重新加载配置文件
        self.father.dao.re_init()
        # 刷新数据
        self.father.refresh_in_thread()
        self.destroy()
