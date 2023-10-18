"""设置程序常量"""
import pyautogui

"""
图标
"""
icon_edit = r'icon/edit.png'
icon_process = r'icon/process.png'
icon_complete = r'icon/complete.png'
icon_error = r'icon/error.png'

"""
错误参数ui的提示格式
"""
error_stylesheet_border = 'border: 1px solid red;'

"""
默认参数值设置
"""
# default_duration: float = 0.25  # 默认移动所需时间
# max_duration: float = 9999.99  # 移动所需时间的最大值限制
# default_presses: int = 1  # 默认重复次数
# default_clicks: int = 1  # 默认点击次数
# max_clicks: int = 9  # 点击次数的最大值限制
# default_interval: float = 0.1  # 默认每次点击间隔时间
# max_interval: float = 9999.99  # 每次点击间隔时间的最大值限制
# max_x, max_y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）
# default_wait_time = 1  # 默认等待时间
# default_wait_time_min = 1  # 默认等待时间（区间最小值）
# default_wait_time_max = 1  # 默认等待时间（区间最大值）
# default_button = '左键'  # 默认鼠标按键
# default_direction = '向上'  # 默认滚动方向
# default_distance = 0  # 默认滚动距离
# default_find_model = '第一个'  # 默认寻图模式
# default_pic_file = ''  # 默认图片路径
# default_message = ''  # 默认文本
# default_hotkeys = ''  # 默认热键
# default_keys = ''  # 默认键
# default_key = ''  # 默认键
# default_x = 0  # 默认x轴坐标值
# default_y = 0  # 默认y轴坐标值
# default_confidence = 0.9  # 默认寻图精度
# default_area = (0, 0, 0, 0)  # 默认区域截图范围
# 上述参数转字典
default_args_dict = {'default_duration': 0.25,
                     'max_duration': 9999.99,
                     'default_presses': 1,
                     'default_clicks': 1,
                     'max_clicks': 9,
                     'default_interval': 0.1,
                     'max_interval': 9999.99,
                     'max_x': pyautogui.size()[0],
                     'max_y': pyautogui.size()[1],
                     'default_wait_time': 1,
                     'default_wait_time_min': 1,
                     'default_wait_time_max': 1,
                     'default_button': '左键',
                     'default_direction': '向上',
                     'default_distance': 0,
                     'default_find_model': '第一个',
                     'default_pic_file': '',
                     'default_message': '',
                     'default_hotkeys': '',
                     'default_keys': '',
                     'default_key': '',
                     'default_x': 0,
                     'default_y': 0,
                     'default_confidence': 0.9,
                     'default_area': (0, 0, 0, 0)}
"""
指令对应字典
"""
# 对应字典设计 combox项:{function:对应函数, widget:对应控件}
# 第一个元素留空，用于初始显示
command_link_dict = {'': {'function': '', 'widget': ''},
                    '鼠标操作-移动':{'function':'InstructMouse.move_mouse_to_position(x=x,y=y,duration=duration)','widget':'command_widget_move_mouse_to_position'},
                    '鼠标操作-按下并拖拽':{'function':'InstructMouse.drag_mouse_to_position(x=x,y=y,button=button,duration=duration)','widget':'command_widget_drag_mouse_to_position'},
                    '鼠标操作-点击':{'function':'InstructMouse.mouse_click(button=button,clicks=clicks,interval=interval)','widget':'command_widget_mouse_click'},
                    '鼠标操作-按下(不释放)':{'function':'InstructMouse.mouse_down(button=button)','widget':'command_widget_mouse_down'},
                    '鼠标操作-释放':{'function':'InstructMouse.mouse_up(button=button)','widget':'command_widget_mouse_up'},
                    '鼠标操作-滚动滚轮':{'function':'InstructMouse.mouse_scroll(distance=distance)','widget':'command_widget_mouse_scroll'},
                    '键盘操作-输入文本':{'function':'InstructKeyboard.press_text(message=message,interval=interval)','widget':'command_widget_press_text'},
                    '键盘操作-敲击':{'function':'InstructKeyboard.press_keys(keys=keys,presses=presses,interval=interval)','widget':'command_widget_press_keys'},
                    '键盘操作-使用热键':{'function':'InstructKeyboard.press_hotkey(hotkeys)','widget':'command_widget_press_hotkey'},
                    '键盘操作-按下(不释放)':{'function':'InstructKeyboard.press_down_key(key=key)','widget':'command_widget_press_down_key'},
                    '键盘操作-释放':{'function':'InstructKeyboard.press_up_key(key=key)','widget':'command_widget_press_up_key'},
                    '图像操作-全屏截图':{'function':'InstructPic.screenshot_fullscreen(pic_file=pic_file)','widget':'command_widget_screenshot_fullscreen'},
                    '图像操作-区域截图':{'function':'InstructPic.screenshot_area(pic_file=pic_file,area=area)','widget':'command_widget_screenshot_area'},
                    '图像操作-匹配图片并移动':{'function':'InstructPic.move_to_pic_position(pic_file=pic_file,duration=duration,find_model=find_model)','widget':'command_widget_move_to_pic_position'},
                    '图像操作-匹配图片并点击':{'function':'InstructPic.click_pic_position(clicks=clicks,button=button,pic_file=pic_file,interval=interval,duration=duration,find_model=find_model)','widget':'command_widget_click_pic_position'},
                    '其他-等待时间':{'function':'InstructCustom.wait(wait_time=wait_time)','widget':'command_widget_wait'},
                    '其他-等待时间（区间随机）':{'function':'InstructCustom.wait(wait_time=wait_time)','widget':'command_widget_wait_random'}}

"""
pyautogui支持的快捷键字典
"""
pyautogui_keyboard_keys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
                           '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                           '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                           'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback',
                           'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch',
                           'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal',
                           'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                           'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22',
                           'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul',
                           'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2',
                           'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                           'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9',
                           'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print',
                           'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select',
                           'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                           'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command',
                           'option', 'optionleft', 'optionright']
