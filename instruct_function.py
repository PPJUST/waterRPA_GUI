"""pyautogui的封装"""
import time
from typing import Tuple, Union

import pyautogui

default_duration: float = 0.25  # 默认移动所需时间
max_duration: float = 9999.99  # 移动所需时间的最大值限制
default_presses: int = 1  # 默认重复次数
default_clicks: int = 1  # 默认点击次数
max_clicks: int = 9  # 点击次数的最大值限制
default_interval: float = 0.1  # 默认每次点击间隔时间
max_interval: float = 9999.99  # 每次点击间隔时间的最大值限制
max_x, max_y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）
default_wait_time = 1  # 默认等待时间


class instruct_mouse:
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
    def move_mouse_to_position(x: int, y: int, duration: float = default_duration):
        """移动鼠标至指定坐标轴
        duration 为移动所需时间，0为瞬间移动"""
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def drag_mouse_to_position(x: int, y: int, button: str = 'left', duration: float = default_duration):
        """按下鼠标键，拖拽至指定坐标轴
        button 为指定键，可设置为"left", "middle", right"
        duration 为移动所需时间，0为瞬间移动"""
        pyautogui.dragTo(x, y, button=button, duration=duration)

    @staticmethod
    def mouse_click(x: int, y: int, button: str = 'left', clicks: int = default_clicks,
                    interval: float = default_interval, duration: float = default_duration):
        """在指定位置点击鼠标
        button 为点击的按键，可设置为"left", "middle", right
        clicks 为点击次数
        interval 为点击间隔时间
        duration 为移动所需时间，0为瞬间移动"""
        pyautogui.click(x, y, button=button, clicks=clicks, interval=interval, duration=duration)

    @staticmethod
    def mouse_down(x: int, y: int, button: str = 'left', duration: float = default_duration):
        """在指定位置按下鼠标
        button 为点击的按键，可设置为"left", "middle", right
        duration 为移动所需时间，0为瞬间移动"""
        pyautogui.mouseDown(x, y, button=button, duration=duration)

    @staticmethod
    def mouse_up(x: int, y: int, button: str = 'left', duration: float = default_duration):
        """在指定位置释放鼠标
        button 为点击的按键，可设置为"left", "middle", right
        duration 为移动所需时间，0为瞬间移动"""
        pyautogui.mouseUp(x, y, button=button, duration=duration)

    @staticmethod
    def mouse_scroll(x: int, y: int, distance: int):
        """在指定位置滚动滚轮
        clicks 为滚动格数，正数向上滚动，负数向下滚动"""
        pyautogui.scroll(clicks=distance, x=x, y=y)


class instruct_keyboard:
    """pyautogui的键盘操作的简单封装

    内部变量说明：
    massage 为输入的文本
    keys 为按下的键，有固定名称，传入多个str，不可传入list
    presses 为重复次数
    interval 为间隔时间"""

    @staticmethod
    def press_text(message: str, interval: float = default_interval):
        """输入字符串
        interval为 每次输入的间隔时间"""
        pyautogui.typewrite(message=message, interval=interval)

    @staticmethod
    def press_keys(*keys: str, presses: int = default_presses, interval: float = default_interval):
        """敲击指定键
        keys 传入多个str，不可传入list
        presses 为重复次数
        interval 为每次重复的间隔时间"""
        pyautogui.press(keys=keys, presses=presses, interval=interval)

    @staticmethod
    def press_down_key(key: str):
        """按下指定按键"""
        pyautogui.keyDown(key)

    @staticmethod
    def press_up_key(key: str):
        """释放指定按键"""
        pyautogui.keyUp(key)

    @staticmethod
    def press_hotkey(*hotkeys: Union[str, list]):
        """按下组合键，实现热键操作
        hotkeys 可传入list"""
        pyautogui.hotkey(hotkeys)


class instruct_pic:
    """pyautogui的图像操作的简单封装

    图像的操作调用了PyScreeze库
    参数说明：
    confidence 为定位精度，0~1，越大越精准"""

    @staticmethod
    def screenshot_fullscreen(pic_file: str = 'screenshot.png'):
        """截全屏并保存图片
        pic_file 可指定保存路径与名称"""
        pyautogui.screenshot(pic_file)

    @staticmethod
    def screenshot_area(area: Union[tuple, list], pic_file: str = 'screenshot.png'):
        """指定区域截图并保存图片
        截取区域 area 参数为(左上角X坐标值, 左上角Y坐标值, 右下角X坐标值, 右下角X坐标值)
        pic_file 可指定保存路径与名称"""
        # 转换area参数至pyautogui的格式
        region = (area[0], area[1], area[2] + area[0], area[3] + area[1])
        pyautogui.screenshot(pic_file, region=region)

    @staticmethod
    def _search_pic_first_position(pic_file: str, confidence: float = 0.9) -> Tuple[Union[int, None], Union[int, None]]:
        """获得在屏幕上第一个找到的文件图片的中心点坐标，如果没有找到则返回None
        confidence 为查找精度"""
        position = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence)

        if position:
            x, y = position.x, position.y
        else:
            x, y = None, None
        return x, y

    @staticmethod
    def _search_pic_all_position(pic_file: str, confidence: float = 0.9) -> list:
        """获得在屏幕上所有找到的文件图片的中心点坐标，如果没有找到则返回None
        返回的坐标格式为[(x, y), (x_1, y_2)]
        confidence 为查找精度"""
        result = pyautogui.locateAllOnScreen(pic_file, confidence=confidence)
        all_center_position = []
        for pos in result:
            mid_x = pos.left + pos.width // 2
            mid_y = pos.top + pos.height // 2
            all_center_position.append((mid_x, mid_y))

        return all_center_position

    @staticmethod
    def move_to_pic_position(pic_file, duration=default_duration, find_model: str = '第一个') -> bool:
        """匹配图片并移动指令（两个函数的组合）
        pic_file 为图片文件路径
        duration 为移动所需时间，0为瞬间移动
        find_model 为查找模式，'第一个'或'全部'，用于点击"""
        all_center_position = instruct_pic._search_pic_first_position(pic_file)
        if all_center_position:
            if find_model == '第一个':
                x, y = all_center_position[0]
                instruct_mouse.move_mouse_to_position(x, y, duration=duration)
            elif find_model == '全部':
                for i in range(len(all_center_position)):
                    x, y = all_center_position[i]
                    instruct_mouse.mouse_click(x, y, duration=duration)
        else:  # 重试识别不在本函数内执行，在外部调用时设置
            print('无匹配项')
            return False

    @staticmethod
    def click_pic_position(pic_file, button: str = 'left', clicks: int = default_clicks,
                           interval: float = default_interval, duration=default_duration,
                           find_model: str = '第一个') -> bool:
        """匹配图片并点击指令（两个函数的组合）
        button 为点击的按键，可设置为"left", "middle", right
        pic_file 为图片文件路径
        clicks 为点击次数
        interval 为点击间隔时间
        duration 为移动所需时间，0为瞬间移动
        find_model 为查找模式，'第一个匹配项'或'全部匹配项'，用于点击"""
        all_center_position = instruct_pic._search_pic_first_position(pic_file)
        if all_center_position:
            if find_model == '第一个':
                x, y = all_center_position[0]
                instruct_mouse.mouse_click(x, y, button=button, clicks=clicks, interval=interval, duration=duration)
            elif find_model == '全部':
                for i in range(len(all_center_position)):
                    x, y = all_center_position[i]
                    instruct_mouse.mouse_click(x, y, button=button, clicks=clicks, interval=interval, duration=duration)
        else:  # 重试识别不在本函数内执行，在外部调用时设置
            print("无匹配项")
            return False


class instruct_custom:
    """pyautogui的其他操作的简单封装"""

    @staticmethod
    def wait(wait_time: float):
        """等待指定时间"""
        time.sleep(wait_time)
