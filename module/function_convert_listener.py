"""将pynput方法获取的数据转换为args_dict格式"""

import pickle

from pynput import keyboard

from module.constant_default import default_args_dict, listener_file

"""
2023.12.10：
1.转换说明：
暂时只转换录制的关键点操作（鼠标点击，鼠标滚轮，键盘点击），不转换鼠标的移动操作（只会做两点间的直线移动）
2.事件说明：
mouse_press 转换为 鼠标移动+按下
mouse_release 转换为 鼠标移动+释放
mouse_scroll 转换为 鼠标移动+滚轮滚动

keyboard_press 转换为 键盘按下
keyboard_release 转换为 键盘释放

不同关键点之间的间隔用wait替代
"""

pynput_key_convert = {keyboard.Key.alt: 'alt', keyboard.Key.alt_l: 'altleft', keyboard.Key.alt_r: 'altright',
                      keyboard.Key.alt_gr: None, keyboard.Key.backspace: 'backspace',
                      keyboard.Key.caps_lock: 'capslock',
                      keyboard.Key.cmd: 'win', keyboard.Key.cmd_l: 'winleft', keyboard.Key.cmd_r: 'winright',
                      keyboard.Key.ctrl: 'ctrl',
                      keyboard.Key.ctrl_l: 'ctrlleft', keyboard.Key.ctrl_r: 'ctrlright', keyboard.Key.delete: 'delete',
                      keyboard.Key.down: 'down', keyboard.Key.end: 'end', keyboard.Key.enter: 'enter',
                      keyboard.Key.esc: 'esc', keyboard.Key.f1: 'f1', keyboard.Key.f2: 'f2', keyboard.Key.f3: 'f3',
                      keyboard.Key.f4: 'f4', keyboard.Key.f5: 'f5', keyboard.Key.f6: 'f6', keyboard.Key.f7: 'f7',
                      keyboard.Key.f8: 'f8', keyboard.Key.f9: 'f9', keyboard.Key.f10: 'f10',
                      keyboard.Key.f11: 'f11', keyboard.Key.f12: 'f12', keyboard.Key.f13: 'f13',
                      keyboard.Key.f14: 'f14',
                      keyboard.Key.f15: 'f15', keyboard.Key.f16: 'f16', keyboard.Key.f17: 'f17',
                      keyboard.Key.f18: 'f18',
                      keyboard.Key.f19: 'f19', keyboard.Key.f20: 'f20', keyboard.Key.home: 'home',
                      keyboard.Key.left: 'left',
                      keyboard.Key.page_down: 'pagedown', keyboard.Key.page_up: 'pageup', keyboard.Key.right: 'right',
                      keyboard.Key.shift: 'shift', keyboard.Key.shift_l: 'shiftleft',
                      keyboard.Key.shift_r: 'shiftright',
                      keyboard.Key.space: 'space', keyboard.Key.tab: 'tab', keyboard.Key.up: 'up',
                      keyboard.Key.media_play_pause: 'playpause', keyboard.Key.media_volume_mute: 'volumemute',
                      keyboard.Key.media_volume_down: 'volumedown', keyboard.Key.media_volume_up: 'volumeup',
                      keyboard.Key.insert: 'insert', keyboard.Key.menu: None,
                      keyboard.Key.num_lock: 'numlock', keyboard.Key.pause: 'pause',
                      keyboard.Key.print_screen: 'printscreen', keyboard.Key.scroll_lock: 'scrolllock',
                      '0': '96', '1': '97', '2': '98', '3': '99', '4': '100', '5': '101', '6': '102', '7': '103',
                      '8': '104', '9': '105',
                      }


def convert_pynput_key(key):
    """转换pynput的键为一般键"""
    if key in pynput_key_convert:
        return pynput_key_convert[key]
    else:
        return key


def get_original_data():
    """获取原始数据"""
    with open(listener_file, 'rb') as file:
        data_dict = pickle.load(file)

    return data_dict


def convert_to_ad():
    """转换为args_dict格式"""
    command_data = []  # [{args_dict}, ...]
    data = get_original_data()
    last_time = 0
    for d_list in data:
        time_local = d_list[0]
        event_type = d_list[1]
        event_args = d_list[2]
        # 提取数据
        time_difference = time_local - last_time
        if time_difference > 10000:  # 处理第一个时间差值
            time_difference = 0.25
        last_time = time_local
        x = int(event_args['x'])
        y = int(event_args['y'])
        button = event_args['button']
        direction = event_args['direction']
        key = event_args['key']

        if event_type == 'mouse_press':  # 拆分为移动+按下
            # 移动
            command_move = default_args_dict.copy()
            command_move['command_type'] = 'command_mouse_move_absolute'
            command_move['x'] = x
            command_move['y'] = y
            command_move['duration'] = time_difference
            command_data.append(command_move)
            # 按下
            command_press = default_args_dict.copy()
            command_press['command_type'] = 'command_mouse_press'
            command_press['button'] = button
            command_data.append(command_press)
        elif event_type == 'mouse_release':  # 拆分为移动+释放
            # 移动
            command_move = default_args_dict.copy()
            command_move['command_type'] = 'command_mouse_move_absolute'
            command_move['x'] = x
            command_move['y'] = y
            command_move['duration'] = time_difference
            command_data.append(command_move)
            # 释放
            command_release = default_args_dict.copy()
            command_release['command_type'] = 'command_mouse_release'
            command_release['button'] = button
            command_data.append(command_release)
        elif event_type == 'mouse_scroll':  # 拆分为鼠标移动+滚轮滚动
            # 移动
            command_move = default_args_dict.copy()
            command_move['command_type'] = 'command_mouse_move_absolute'
            command_move['x'] = x
            command_move['y'] = y
            command_move['duration'] = time_difference
            command_data.append(command_move)
            # 滚轮
            command_scroll = default_args_dict.copy()
            command_scroll['command_type'] = 'command_mouse_scroll'
            if direction == 'up':  # 两个库滚轮操作不同，滚动距离暂定50像素
                distance = 50
            else:
                distance = -50
            command_scroll['distance'] = distance
            command_data.append(command_scroll)
        elif event_type == 'keyboard_press':  # 等待时间+键盘按下
            # 等待
            command_wait = default_args_dict.copy()
            command_wait['command_type'] = 'command_wait_time'
            command_wait['wait_time'] = time_difference
            command_data.append(command_wait)
            # 按下
            command_press = default_args_dict.copy()
            command_press['command_type'] = 'command_key_press'
            command_press['key'] = convert_pynput_key(key)
            command_data.append(command_press)
        elif event_type == 'keyboard_release':  # 等待时间+键盘释放
            # 等待
            command_wait = default_args_dict.copy()
            command_wait['command_type'] = 'command_wait_time'
            command_wait['wait_time'] = time_difference
            command_data.append(command_wait)
            # 释放
            command_release = default_args_dict.copy()
            command_release['command_type'] = 'command_key_release'
            command_release['key'] = convert_pynput_key(key)
            command_data.append(command_release)

    return command_data
