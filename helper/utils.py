import json
import os
from PIL.ImageTk import PhotoImage
from PIL import Image


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
    for filename in os.listdir('./img'):
        image = Image.open('./img/{}'.format(filename))
        weather = filename.split('.')[0]
        result[weather] = [PhotoImage(image), PhotoImage(
            image.resize((40, 40), Image.ANTIALIAS))]
    return result
