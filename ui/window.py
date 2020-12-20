import tkinter
from tkinter import Button, Frame


class Window(tkinter.Tk):
    '''程序主窗口'''

    def __init__(self):
        super().__init__()
        self.title('天气预报')
        self.geometry('800x600')

    def __draw(self):
        top_frame = Frame(self, height=80)
        self.help = Button(top_frame, text='帮助')
        self.setting = Button(top_frame, text='设置')
        self.refresh = Button(top_frame, text="刷新")
        self.help.pack(side='right', padx=20, pady=20)
        self.setting.pack(side='right', pady=20)
        self.refresh.pack(side='right', padx=20, pady=20)
        top_frame.pack(fill='x', side='top')
        bottom_frame = Frame(self)
        bottom_frame.pack(fill='both', side='bottom')

    def __bind_event(self):
        pass

    def __show(self):
        self.mainloop()

    def run(self):
        self.__draw()
        self.__bind_event()
        self.__show()
