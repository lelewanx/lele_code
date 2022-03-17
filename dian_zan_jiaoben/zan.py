#!/usr/bin/python3
# -*- encoding:utf-8 -*-
# Author: lele,wanx
# Date: 2022-03-17 12:36:32
# Last Modified by:   lele,wanx
# Last Modified time: 2022-03-17 12:36:32

import pyautogui


def find_zan_position(zan):
    """
    Find the center of the picture in computer screen
    """
    return pyautogui.locateCenterOnScreen(zan)


def dianzan(center_point):
    """
    Move the mouse to the position and click the left mouse
    """
    if bool(center_point):
        x, y = center_point
        pyautogui.moveTo(x, y, duration=2)
        pyautogui.click(x, y, button="left")
        return True
    else:
        print(f"No Found zan")


def scroll_mouse(direction="down", len_range=500):
    """
    Mouse scrolling
    Args:
        direction (str): Mouse scroll direction. Defaults to "down".
        len_range (int): Rolling amplitude. Defaults to 500.
    """
    if direction in ["D", "down"]:
        pyautogui.scroll(-len_range)
    elif direction in ["U", "up"]:
        pyautogui.scroll(len_range)
    else:
        print("Args error.")


def main():
    print(f"cureent screen: {pyautogui.size()}")
    zan = "zan.png"
    center_point = find_zan_position(zan)
    if bool(center_point):
        if not bool(dianzan(center_point)):
            scroll_mouse("d", 500)


if __name__ == '__main__':
    main()
