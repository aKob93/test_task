# -*- coding: utf-8 -*-
import requests
from PIL import Image


URL_PLASHKA = 'http://alitair.1gb.ru/test_prog_plashki/benefit.png'  # плашка
URL_IMAGE = 'http://alitair.1gb.ru/test_prog_plashki/106044_benefit.jpg'  # картинка

def print():
    raw_plashka = requests.get(URL_PLASHKA, stream=True).raw
    raw_image = requests.get(URL_IMAGE, stream=True).raw
    Image.open(raw_plashka).save('plashka.png', 'PNG')
    Image.open(raw_image).save('image.png', 'PNG')

    image = Image.open('image.png')
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту.
    image.resize((100, 100)) #Изменение размера
    img_to_paste = Image.open('plashka.png')
    img_to_paste.paste(image, (width // 2 - 400, height // 2 - 50))
    img_to_paste.save('mm_paste.png', 'png')

