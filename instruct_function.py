import time

import pyautogui
import pyperclip


def instruct_pic_click(click_time, l_or_r_click, pic_file):
    """图片点击指令"""
    location = pyautogui.locateCenterOnScreen(pic_file, confidence=0.9)
    if location is not None:
        pyautogui.click(location.x, location.y, clicks=click_time, interval=0.2, duration=0.2, button=l_or_r_click)
    else:
        print("未找到匹配图片")


def instruct_input(text):
    """文本输入指令"""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')


def instruct_wait(wait_time):
    """等待指令"""
    time.sleep(wait_time)


def instruct_scroll(direction, distance):
    """滚动滚轮指令"""
    if direction == '向上':
        scroll = distance
    else:
        scroll = -distance
    pyautogui.scroll(scroll)


def instruct_hotkey(hotkey_str):
    """模拟按键指令"""
    hotkey_split = hotkey_str.split(' ')
    hotkey_list = [key for key in hotkey_split if not key.strip()]
    pyautogui.hotkey(hotkey_list)
