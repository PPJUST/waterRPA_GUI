"""通用方法"""
import random
import string
from typing import Union

from PySide6.QtCore import *


def check_filename_feasible(filename: str, replace: bool = False) -> Union[str, bool]:
    """检查文件名是否符合Windows规范
    传参:
    filename 仅文件名（不含路径）
    replace 是否替换非法字符"""
    # 官方文档：文件和文件夹不能命名为“.”或“..”，也不能包含以下任何字符: # % & * | \ : " < > ?/
    except_word = [':', '#', '%', '&', '*', '|', '\\', ':', '"', '<', '>', '?', '/']
    if not replace:  # 不替换时，仅检查
        # 检查.
        if filename[0] == '.':
            return False

        # 检查# % & * | \ : " < > ?/

        for key in except_word:
            if key in filename:
                return False
        return True
    else:
        for word in except_word:
            filename = filename.replace(word, '')
        while filename[0] == '.':
            filename = filename[1:]

        return filename.strip()


def create_random_string(length: int = 16) -> str:
    """生成一个指定长度的随机字符串（小写英文+数字）
    传参：length 字符串的长度
    返回值：生成的str"""
    """
    小写英文 string.ascii_lowercase
    大写英文 string.ascii_uppercase
    数字 string.digits
    """
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=length))

    return random_string


def calculate_resize(qsize_main: QSize, qsize_compare: QSize) -> QSize:
    """传入两个QSize大小，计算新的QSize
    用于将图片保持纵横比显示在QLabel上"""
    # 备忘录 - 寻找替换方法
    width_main = qsize_main.width()
    height_main = qsize_main.height()
    width_compare = qsize_compare.width()
    height_compare = qsize_compare.height()

    rate_main = width_main / height_main
    rate_compare = width_compare / height_compare

    if rate_main >= rate_compare:  # 符合则按高缩放
        resize_height = height_main
        resize_width = int(width_compare / height_compare * resize_height)
        resize = QSize(resize_width, resize_height)
    else:  # 否则按宽缩放
        resize_width = width_main
        resize_height = int(height_compare / width_compare * resize_width)
        resize = QSize(resize_width, resize_height)
    """
    后续操作说明
    pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
    self.label.setPixmap(pixmap)
    """

    return resize
