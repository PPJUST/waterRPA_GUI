import time
from typing import Tuple, Union

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


"""
1. 鼠标操作

内部变量说明：
x 为x坐标轴
y 为y坐标轴
duration 为移动所需时间，0为瞬间移动
button 为对应的鼠标按键，可设置为"left", "middle", right"
clicks 为点击次数
interval 为多次点击时的点击间隔时间
tween 为移动鼠标时的速率函数，默认为线性速度移动
"""


def get_mouse_position() -> tuple[int, int]:
    """获取鼠标当前位置"""
    current_mouse_x, current_mouse_y = pyautogui.position()

    return current_mouse_x, current_mouse_y


def move_mouse_to_position(x: int, y: int, duration: float = 0.25):
    """移动鼠标至指定坐标轴
    duration 为移动所需时间，0为瞬间移动"""
    pyautogui.moveTo(x, y, duration=duration)


def drag_mouse_to_position(x: int, y: int, button: str = 'left', duration: int = 0.25):
    """按下鼠标键，拖拽至指定坐标轴
    button 为指定键，可设置为"left", "middle", right"
    duration 为移动所需时间，0为瞬间移动"""
    pyautogui.dragTo(x, y, button=button, duration=duration)


def mouse_click(x: int, y: int, button: str = 'left', clicks: int = 1, interval: float = 0.1):
    """在指定位置点击鼠标
    button 为点击的按键，可设置为"left", "middle", right
    clicks 为点击次数
    interval 为点击间隔时间"""
    pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)


def mouse_down(x: int, y: int, button: str = 'left'):
    """在指定位置按下鼠标
    button 为点击的按键，可设置为"left", "middle", right"""
    pyautogui.mouseDown(x, y, button=button)


def mouse_up(x: int, y: int, button: str = 'left'):
    """在指定位置释放鼠标
    button 为点击的按键，可设置为"left", "middle", right"""
    pyautogui.mouseUp(x, y, button=button)


def mouse_scroll(x: int, y: int, clicks: int):
    """在指定位置滚动滚轮
    clicks 为滚动格数，正数向上滚动，负数向下滚动"""
    pyautogui.scroll(clicks=clicks, x=x, y=y)


"""
2. 键盘操作

内部变量说明：
massage 为输入的文本
keys 为按下的键，有固定名称，可以传入list
presses 为重复次数
interval 为每次敲击的间隔时间
"""


def press_text(message: str, interval: float = 0.25):
    """输入字符串
    interval为 每次输入的间隔时间"""
    pyautogui.typewrite(message=message, interval=interval)


def press_keys(*keys: Union[str, list], presses: int = 1, interval: float = 0.1):
    """敲击指定键
    keys 可传入list
    presses 为重复次数
    interval 为每次敲击的间隔时间"""
    pyautogui.press(keys=keys, presses=presses, interval=interval)


def press_down_key(key: str):
    """按下指定按键"""
    pyautogui.keyDown(key)


def press_up_key(key: str):
    """释放指定按键"""
    pyautogui.keyUp(key)


def press_hotkey(*hotkeys: Union[str, list]):
    """按下组合键，实现热键操作
    hotkeys 可传入list"""
    pyautogui.hotkey(hotkeys)


"""
3. 图像操作

图像的操作调用了PyScreeze库
参数说明：
confidence 为定位精度，0~1，越大越精准
"""


def screenshot_fullscreen(pic_file: str = 'screenshot.png'):
    """截全屏并保存图片"""
    pyautogui.screenshot(pic_file)


def screenshot_area(region: Union[tuple, list], pic_file: str = 'screenshot.png'):
    """指定区域截图并保存图片
    截取区域region参数为(左上角X坐标值, 左上角Y坐标值, 宽度, 高度)"""
    pyautogui.screenshot(pic_file, region=region)


def search_pic_first_position(pic_file: str, confidence: float = 0.9) -> Tuple[Union[int, None], Union[int, None]]:
    """获得在屏幕上第一个找到的文件图片的中心点坐标，如果没有找到则返回None
    confidence 为查找精度"""
    position = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence)

    if position:
        x, y = position.x, position.y
    else:
        x, y = None, None
    return x, y


def search_pic_all_position(pic_file: str, confidence: float = 0.9):
    """获得在屏幕上所有找到的文件图片的中心点坐标，如果没有找到则返回None
    confidence 为查找精度"""
    result = pyautogui.locateAllOnScreen(pic_file, confidence=confidence)
    all_center_pos = []
    for pos in result:
        mid_x = pos.left + pos.width // 2
        mid_y = pos.top + pos.height // 2
        all_center_pos.append((mid_x, mid_y))

    return all_center_pos
