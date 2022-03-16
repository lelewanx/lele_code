#!/usr/bin/python3
# -*- encoding:utf-8 -*-
# Author: lele,wanx
# Date: 2022-03-17 10:21:49
# Last Modified by:   lele,wanx
# Last Modified time: 2022-03-17 10:21:49

import pyautogui
from PIL import Image
import time
import os


def my_screenshot(imagefiledirectory):
    """
    Use pyautogui Screen capture of computer screen
    """
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    imagefilename = os.path.join(imagefiledirectory, f"{current_time}.png")
    pyautogui.screenshot(imagefilename)


def compressed_picture(imagefilename, compress_rate=0.5):
    """
    Use PIL resize method to compress the picture.
    """
    image_directory = os.path.dirname(imagefilename)
    filename = os.path.basename(imagefilename)
    img = Image.open(imagefilename)
    width, height = img.size
    resize_width = int(width * compress_rate)
    resize_height = int(height * compress_rate)
    print(
        f"Picture compressed from {width, height} to {resize_width, resize_height}"
    )
    img_resize = img.resize((resize_width, resize_height))
    resize_filename = os.path.join(image_directory, f"result_{filename}")
    img_resize.save(resize_filename)


def main():
    """
    Program execution entry.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    imagefiledirectory = os.path.join(current_directory, "save_screenshot")
    if not os.path.exists(imagefiledirectory):
        os.makedirs(imagefiledirectory)
    my_screenshot(imagefiledirectory)
    imagefilename = os.path.join(imagefiledirectory, f"20220317105044.png")
    compressed_picture(imagefilename)


if __name__ == '__main__':
    main()
