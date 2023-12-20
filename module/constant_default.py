"""设置常量"""
import pyautogui

"""
图标
"""
icon_edit = r'icon/edit.png'
icon_wait_run = r'icon/wait_run.png'
icon_complete = r'icon/complete.png'
icon_error = r'icon/error.png'
icon_add = r'icon/add.png'
icon_copy = r'icon/copy.png'
icon_del = r'icon/del.png'

"""
错误参数的ui格式
"""
error_stylesheet_border = 'border: 1px solid red;'

"""
录制键鼠相关
"""
listener_file = 'listener.pickle'  # 保存的文件名

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
                           'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                           'widget_command',
                           'option', 'optionleft', 'optionright']

"""
设置文件相关常量
"""
configs_folder = 'configs'  # 存放配置文件的文件夹
command_config = 'widget_command.ini'  # 配置文件名
screenshot_folder = 'screenshot_temp'  # 临时截图文件存放文件夹
global_config = 'global.ini'  # 全局设置文件名

"""
命令参数相关常量
"""
default_duration: float = 0.25  # 默认移动所需时间
max_duration: float = 9999.99  # 移动所需时间的最大值限制
default_presses: int = 1  # 默认重复次数
default_clicks: int = 1  # 默认点击次数
max_clicks: int = 9  # 点击次数的最大值限制
default_interval: float = 0.1  # 默认每次点击间隔时间
max_interval: float = 9999.99  # 每次点击间隔时间的最大值限制
max_x, max_y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）
default_wait_time = 1.00  # 默认等待时间
default_wait_time_min = 1.00  # 默认等待时间（区间最小值）
default_wait_time_max = 1.00  # 默认等待时间（区间最大值）
default_button = '左键'  # 默认鼠标按键
default_scroll_direction = '向上'  # 默认滚动方向
default_scroll_distance = 50  # 默认滚动距离
default_mode_find_image = '第一个'  # 默认寻图模式
default_screenshot_image_path = ''  # 默认图片路径
default_message = ''  # 默认文本
default_hotkey = ''  # 默认热键
default_keys = ''  # 默认键
default_key = ''  # 默认键
default_x = 1  # 默认x轴坐标值
default_y = 1  # 默认y轴坐标值
default_confidence = 0.9  # 默认寻图精度
default_area = (0, 0, 0, 0)  # 默认区域截图范围
default_move_direction = '向左'  # 默认鼠标移动方向
default_move_distance = 100  # 默认鼠标移动距离
max_move_distance = max(max_x, max_y)  # 默认最大鼠标移动距离

default_args_dict = {
    'command_type': '',
    'args_all_right': True,
    'wait_time': default_wait_time,
    'wait_time_min': default_wait_time_min,
    'wait_time_max': default_wait_time_max,
    'button': default_button,
    'clicks': default_clicks,
    'interval': default_interval,
    'key': default_key,
    'keys': default_keys,
    'hotkey': default_hotkey,
    'presses': default_presses,
    'message': default_message,
    'scroll_direction': default_scroll_direction,
    'scroll_distance': default_scroll_distance,
    'move_direction': default_move_direction,
    'move_distance': default_move_distance,
    'duration': default_duration,
    'screenshot_image_path': default_screenshot_image_path,
    'mode_find_image': default_mode_find_image,
    'x': default_x,
    'y': default_y,
    'other': ''
}
"""args_dict参数说明
key:value 键值对
command_type:str 命令类型：对应的子控件名
args_all_right:bool 参数是否都可行:bool值
wait_time:float 等待时间：两位浮点数
wait_time_min:float 等待时间（区间最小值）：两位浮点数
wait_time_max:float 等待时间（区间最大值）：两位浮点数
button:str 鼠标按键：字符串
clicks:int 鼠标点击次数：整数
interval:float 每次间隔：一位浮点数
key:str 键盘单键：对应的键名
keys:str 键盘多键：对应的键名
hotkey:str 键盘快捷键组合：对应的键名
presses:int 重复次数：整数
message:str 输入的文本：字符串
scroll_direction:str 滚轮滚动方向：字符串
scroll_distance:int 滚轮滚动距离：整数
move_direction:str 鼠标移动方向：字符串
move_distance:int 鼠标移动距离：整数
duration:float 移动耗时：两位浮点数
screenshot_image_path:str 保存截图路径：字符串
mode_find_image:str 寻图模式：字符串
x:int x轴坐标：整数
y:int y轴坐标：整数
other:str 占位
"""

"""
命令控件名中英互换参数
"""
command_chs_to_en_dict = {'': '',
                          '---鼠标---': '',
                          '鼠标操作-移动(相对)': 'command_mouse_move_relative',
                          '鼠标操作-移动(绝对)': 'command_mouse_move_absolute',
                          '鼠标操作-点击': 'command_mouse_click',
                          '鼠标操作-按下(不释放)': 'command_mouse_press',
                          '鼠标操作-释放': 'command_mouse_release',
                          '鼠标操作-滚动滚轮': 'command_mouse_scroll',
                          '---键盘---': '',
                          '键盘操作-模拟输入': 'command_key_in_keys',
                          '键盘操作-粘贴文本': 'command_paste_text',
                          '键盘操作-使用热键': 'command_key_in_hotkey',
                          '键盘操作-按下(不释放)': 'command_key_press',
                          '键盘操作-释放': 'command_key_release',
                          '---寻图---': '',
                          '图像操作-全屏截图': 'command_screenshot_fullscreen',
                          '图像操作-搜寻图片并移动': 'command_move_to_image_position',
                          '图像操作-搜寻图片并点击': 'command_click_image_position',
                          '---等待---': '',
                          '其他-等待时间': 'command_wait_time',
                          '其他-等待时间(区间随机)': 'command_wait_time_random'}

# for key, value in command_chs_to_en.items():
#     command_en_to_chs_dict[value] = key
command_en_to_chs_dict = {'': '',
                          'command_mouse_move_relative': '鼠标操作-移动(相对)',
                          'command_mouse_move_absolute': '鼠标操作-移动(绝对)',
                          'command_mouse_click': '鼠标操作-点击',
                          'command_mouse_press': '鼠标操作-按下(不释放)',
                          'command_mouse_release': '鼠标操作-释放',
                          'command_mouse_scroll': '鼠标操作-滚动滚轮',
                          'command_key_in_keys': '键盘操作-模拟输入',
                          'command_paste_text': '键盘操作-粘贴文本',
                          'command_key_in_hotkey': '键盘操作-使用热键',
                          'command_key_press': '键盘操作-按下(不释放)',
                          'command_key_release': '键盘操作-释放',
                          'command_screenshot_fullscreen': '图像操作-全屏截图',
                          'command_move_to_image_position': '图像操作-搜寻图片并移动',
                          'command_click_image_position': '图像操作-搜寻图片并点击',
                          'command_wait_time': '其他-等待时间',
                          'command_wait_time_random': '其他-等待时间(区间随机)'}
