import json
import os
import tkinter


def read_config() -> dict:
    '''
    读取程序配置
    '''
    with open('./config.json', 'r') as f:
        return json.loads(f.read())


def increase(current: int, len: int) -> int:
    '''
    城市号递增规则
    '''
    return (current+1) % len


def get_images() -> dict:
    result = dict()
    for image in os.listdir('./img'):
        result[image.split('.')[0]] = tkinter.PhotoImage(
            file='./img/{}'.format(image))
    return result
