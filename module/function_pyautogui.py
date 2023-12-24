"""pyautogui的封装"""
import random
import time
from typing import Tuple, Union

import numpy
import pyautogui
import pyperclip
from PIL import Image

"""
参数默认设置
"""
_default_duration: float = 0.25  # 默认移动所需时间
_default_clicks: int = 1  # 默认点击次数
_default_interval: float = 0.1  # 默认每次点击间隔时间
_default_presses: int = 1  # 默认重复次数
_default_confidence = 0.9  # 默认寻图精度
_default_move_direction = '向左'  # 默认移动方向
_default_move_distance = 100  # 默认移动距离
_default_X = 1  # 默认x坐标轴
_default_Y = 1  # 默认y坐标轴
_max_x, _max_y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）


def image_read_from_chinese_path(image_file_name):
    # 将路径对应的图片转换为numpy图片对象（pyautogui库不支持中文名图片，需要通过numpy库中转）
    image_numpy_data = numpy.array(Image.open(image_file_name))

    return image_numpy_data


class PyautoguiMouse:
    """pyautogui的鼠标操作的简单封装

    内部变量说明：
    x 为x坐标轴
    y 为y坐标轴
    duration 为移动所需时间，0为瞬间移动
    button 为对应的鼠标按键，可设置为"left", "middle", right"
    clicks 为点击次数
    interval 为多次点击时的点击间隔时间
    tween 为移动鼠标时的速率函数，默认为线性速度移动"""

    @staticmethod
    def _get_mouse_position() -> Tuple[int, int]:
        """获取鼠标当前位置"""
        current_mouse_x, current_mouse_y = pyautogui.position()

        return current_mouse_x, current_mouse_y

    @staticmethod
    def move_mouse_to_position(x: int, y: int, duration: float = _default_duration):
        """移动鼠标至指定坐标轴
        duration 为移动所需时间，0为瞬间移动"""
        if x == 0 and y == 0:
            x, y = 1, 1
        pyautogui.moveTo(x, y, duration=duration)

        return x, y

    @staticmethod
    def drag_mouse_to_position(x: int, y: int, button: str = 'left', duration: float = _default_duration):
        """按下鼠标键，拖拽至指定坐标轴
        button 为指定键，可设置为"left", "middle", right"
        duration 为移动所需时间，0为瞬间移动"""
        if x == 0 and y == 0:
            x, y = 1, 1
        pyautogui.dragTo(x, y, button=button, duration=duration)

        return x, y

    @staticmethod
    def move_mouse_relative(duration: float = _default_duration, move_direction: str = _default_move_direction,
                            move_distance: int = _default_move_distance):
        """向指定方向移动鼠标"""
        x, y = pyautogui.position()
        if move_direction in ['向左', 'left']:
            x -= move_distance
        elif move_direction in ['向右', 'right']:
            x += move_distance
        elif move_direction in ['向上', 'up']:
            y -= move_distance
        elif move_direction in ['向下', 'down']:
            y += move_distance

        if x < 0:
            x = 1
        if x > _max_x:
            x = _max_x

        if y < 0:
            y = 1
        if y > _max_x:
            y = _max_x

        if x == 0 and y == 0:
            x, y = 1, 1
        pyautogui.moveTo(x, y, duration=duration)

        return x, y

    @staticmethod
    def move_mouse_absolute(duration: float = _default_duration, x: int = _default_X,
                            y: int = _default_Y):
        """移动鼠标至指定坐标轴"""
        if x == 0 and y == 0:
            x, y = 1, 1
        pyautogui.moveTo(x, y, duration=duration)

        return x, y

    @staticmethod
    def mouse_click(button: str = 'left', clicks: int = _default_clicks,
                    interval: float = _default_interval):
        """点击鼠标
        button 为点击的按键，可设置为"left", "middle", right
        clicks 为点击次数
        interval 为点击间隔时间"""
        pyautogui.click(button=button, clicks=clicks, interval=interval)

        return button

    @staticmethod
    def mouse_down(button: str = 'left'):
        """按下鼠标
        button 为点击的按键，可设置为"left", "middle", right"""
        pyautogui.mouseDown(button=button)

        return button

    @staticmethod
    def mouse_up(button: str = 'left'):
        """释放鼠标
        button 为点击的按键，可设置为"left", "middle", right"""
        pyautogui.mouseUp(button=button)

        return button

    @staticmethod
    def mouse_scroll(distance: int):
        """滚动滚轮
        distance 为滚动格数，正数向上滚动，负数向下滚动"""
        pyautogui.scroll(clicks=distance)

        return distance


class PyautoguiKeyboard:
    """pyautogui的键盘操作的简单封装

    内部变量说明：
    massage 为输入的文本
    keys 为按下的键，有固定名称，传入多个str，不可传入list
    presses 为重复次数
    interval 为间隔时间"""

    @staticmethod
    def press_text(message: str, presses: int = _default_presses, interval: float = _default_interval):
        """输入字符串
        presses 为重复次数
        interval为 每次输入的间隔时间"""
        for _ in range(presses):
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(interval)

        return message

    @staticmethod
    def press_keys(keys: Union[list, str], presses: int = _default_presses, interval: float = _default_interval):
        """敲击指定键
        keys 可传入list
        presses 为重复次数
        interval 为每次重复的间隔时间"""
        if type(keys) is str:
            keys = keys.split(' ')
        pyautogui.press(keys=keys, presses=presses, interval=interval)

        return keys

    @staticmethod
    def press_down_key(key: str):
        """按下指定按键"""
        pyautogui.keyDown(key)

        return key

    @staticmethod
    def press_up_key(key: str):
        """释放指定按键"""
        pyautogui.keyUp(key)

        return key

    @staticmethod
    def press_hotkey(hotkeys: Union[list, str]):
        """按下组合键，实现热键操作
        hotkeys 传入list"""
        if type(hotkeys) is str:
            hotkeys = hotkeys.split(' ')
        pyautogui.hotkey(hotkeys)

        return hotkeys


class PyautoguiImage:
    """pyautogui的图像操作的简单封装

    图像的操作调用了PyScreeze库
    参数说明：
    confidence 为定位精度，0~1，越大越精准"""

    @staticmethod
    def screenshot_fullscreen(pic_file: str = 'screenshot.png'):
        """截全屏并保存图片
        pic_file 可指定保存路径与名称"""
        pyautogui.screenshot(pic_file)

        return pic_file

    @staticmethod
    def screenshot_area(area: Union[tuple, list], pic_file: str = 'screenshot.png'):
        """指定区域截图并保存图片
        截取区域 area 参数为(左上角X坐标值, 左上角Y坐标值, 右下角X坐标值, 右下角X坐标值)
        pic_file 可指定保存路径与名称"""
        # 转换area参数至pyautogui的格式
        region = (area[0], area[1], area[2] + area[0], area[3] + area[1])
        pyautogui.screenshot(pic_file, region=region)

        return pic_file

    @staticmethod
    def _search_pic_first_position(pic_file: str,
                                   confidence: float = _default_confidence
                                   ) -> Tuple[Union[int, None], Union[int, None]]:
        """获得在屏幕上第一个找到的文件图片的中心点坐标，如果没有找到则返回None
        confidence 为查找精度"""
        pic_file_to_image = image_read_from_chinese_path(pic_file)  # 转换为image对象，以处理中文名图片
        position = pyautogui.locateCenterOnScreen(pic_file_to_image, confidence=confidence)

        if position:
            x, y = position.x, position.y
        else:
            x, y = None, None
        return x, y

    @staticmethod
    def _search_pic_all_position(pic_file: str, confidence: float = _default_confidence, timeout: int = 60) -> list:
        """获得在屏幕上所有找到的文件图片的中心点坐标，如果没有找到则返回None
        返回的坐标格式为[(x, y), (x_1, y_2)]
        confidence 为查找精度
        timeout 为超时时间"""
        pic_file_to_image = image_read_from_chinese_path(pic_file)  # 转换为image对象，以处理中文名图片
        time_start = time.time()
        all_center_position = []
        while True:
            result = pyautogui.locateAllOnScreen(pic_file_to_image, confidence=confidence)
            for pos in result:
                mid_x = pos.left + pos.width // 2
                mid_y = pos.top + pos.height // 2
                all_center_position.append((mid_x, mid_y))
            if all_center_position:
                break

            time_current = time.time()
            run_time = time_start - time_current
            if run_time >= timeout:
                break
            else:
                time.sleep(0.1)

        return all_center_position

    @staticmethod
    def move_to_pic_position(pic_file, duration=_default_duration, find_model: str = '第一个',
                             timeout: int = 60) -> bool:
        """匹配图片并移动指令（两个函数的组合）
        pic_file 为图片文件路径
        duration 为移动所需时间，0为瞬间移动
        find_model 为查找模式，'第一个'或'全部'，用于点击
        timeout 超时时间"""
        all_center_position = PyautoguiImage._search_pic_all_position(pic_file, timeout=timeout)
        if all_center_position:
            if find_model in ['第一个', 'first']:
                x, y = all_center_position[0]
                PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
            elif find_model in ['全部', 'all']:
                for i in range(len(all_center_position)):
                    x, y = all_center_position[i]
                    PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
            return True
        else:
            return False

    @staticmethod
    def click_pic_position(pic_file, duration=_default_duration,
                           find_model: str = '第一个', button: str = 'left', clicks: int = _default_clicks,
                           interval: float = _default_interval, timeout: int = 60) -> bool:
        """匹配图片并点击指令（两个函数的组合）
        button 为点击的按键，可设置为"left", "middle", right
        pic_file 为图片文件路径
        clicks 为点击次数
        interval 为点击间隔时间
        duration 为移动所需时间，0为瞬间移动
        find_model 为查找模式，'第一个匹配项'或'全部匹配项'，用于点击
        timeout 超时时间"""
        all_center_position = PyautoguiImage._search_pic_all_position(pic_file, timeout=timeout)
        if all_center_position:
            if find_model in ['第一个', 'first']:
                x, y = all_center_position[0]
                PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
                PyautoguiMouse.mouse_click(button=button, clicks=clicks, interval=interval)
            elif find_model in ['全部', 'all']:
                for i in range(len(all_center_position)):
                    x, y = all_center_position[i]
                    PyautoguiMouse.move_mouse_to_position(x=x, y=y, duration=duration)
                    PyautoguiMouse.mouse_click(button=button, clicks=clicks, interval=interval)
            return True
        else:
            return False


class PyautoguiCustom:
    """pyautogui的其他操作的简单封装"""

    @staticmethod
    def wait_time(wait_time: float):
        """等待指定时间，传入float"""
        if wait_time == 0:
            wait_time = 0.01

        time.sleep(wait_time)

        return wait_time

    @staticmethod
    def wait_time_random(wait_time_min: int, wait_time_max: int):
        wait_time_random = round(random.uniform(wait_time_min, wait_time_max), 2)

        if wait_time_random == 0:
            wait_time_random = 0.01

        time.sleep(wait_time_random)

        return wait_time_random
