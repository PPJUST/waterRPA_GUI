"""将pynput方法获取的数据转换为args_dict格式"""

import pickle

from pynput import keyboard

from module.constant_default import default_args_dict, listener_file

"""
2023.12.20：
1.转换说明：
暂时只转换录制的关键点操作（鼠标点击，鼠标滚轮，键盘点击），不转换鼠标的移动操作（只会做两点间的直线移动）
2.事件说明：
mouse_press 转换为 鼠标移动+按下
mouse_release 转换为 鼠标移动+释放
mouse_scroll 转换为 鼠标移动+滚轮滚动
0.2秒内连续的鼠标按下释放操作替换为点击操作

keyboard_press 转换为 键盘按下
keyboard_release 转换为 键盘释放
连续的键盘操作不进行替换

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
                      '96': '0', '97': '1', '98': '2', '99': '3', '100': '4', '101': '5', '102': '6', '103': '7',
                      '104': '8', '105': '9',
                      }

pynput_keycode_convert = {
    r"'\x01'": ['ctrl', 'a'],
    r"'\x02'": ['ctrl', 'b'],
    r"'\x03'": ['ctrl', 'c'],
    r"'\x04'": ['ctrl', 'd'],
    r"'\x05'": ['ctrl', 'e'],
    r"'\x06'": ['ctrl', 'f'],
    r"'\x07'": ['ctrl', 'g'],
    r"'\x08'": ['ctrl', 'h'],
    r"'\t'": ['ctrl', 'i'],
    r"'\n'": ['ctrl', 'j'],
    r"'\x0b'": ['ctrl', 'k'],
    r"'\x0c'": ['ctrl', 'l'],
    r"'\r'": ['ctrl', 'm'],
    r"'\x0e'": ['ctrl', 'n'],
    r"'\x0f'": ['ctrl', 'o'],
    r"'\x10'": ['ctrl', 'p'],
    r"'\x11'": ['ctrl', 'q'],
    r"'\x12'": ['ctrl', 'r'],
    r"'\x13'": ['ctrl', 's'],
    r"'\x14'": ['ctrl', 't'],
    r"'\x15'": ['ctrl', 'u'],
    r"'\x16'": ['ctrl', 'v'],
    r"'\x17'": ['ctrl', 'w'],
    r"'\x18'": ['ctrl', 'x'],
    r"'\x19'": ['ctrl', 'y'],
    r"'\x1a'": ['ctrl', 'z'],
    r"'\x1f'": ['ctrl', 'shift', '-'],
    r"<186>": ['ctrl', ';'],
    r"<187>": ['ctrl', '='],
    r"<189>": ['ctrl', '-'],
    r"<192>": ['ctrl', '`'],
    r"<222>": ['ctrl', r"'"],
    r"<48>": ['ctrl', '0'],
    r"<49>": ['ctrl', '1'],
    r"<50>": ['ctrl', '2'],
    r"<51>": ['ctrl', '3'],
    r"<52>": ['ctrl', '4'],
    r"<53>": ['ctrl', '5'],
    r"<54>": ['ctrl', '6'],
    r"<55>": ['ctrl', '7'],
    r"<56>": ['ctrl', '8'],
    r"<57>": ['ctrl', '9'],
    r"'~'": ['shift', '`'],
    r"'!'": ['shift', '1'],
    r"'@'": ['shift', '2'],
    r"'#'": ['shift', '3'],
    r"'$'": ['shift', '4'],
    r"'%'": ['shift', '5'],
    r"'^'": ['shift', '6'],
    r"'*'": ['shift', '7'],
    r"'('": ['shift', '8'],
    r"')'": ['shift', '9'],
    r"'_'": ['shift', '-'],
    r"'+'": ['shift', '='],
    r"':'": ['shift', ';'],
    r"'\"'": ['shift', "'"],
    r"'<'": ['shift', ","],
    r"'{'": ['shift', "["],
    r"'}'": ['shift', "]"],
    r"'|'": ['shift', "\\"],
    r"'?'": ['shift', "/"],
}


def convert_pynput_key(key):
    """转换pynput的键为一般键"""
    if key in pynput_key_convert:
        return pynput_key_convert[key]
    elif str(key) in pynput_keycode_convert:
        return pynput_keycode_convert[str(key)]
    else:
        return key


def convert_mouse_event(event_list: list):
    """处理鼠标事件"""

    def convert_mouse_pr_to_click(event_list_1: list):
        """连续的鼠标按下释放操作替换为点击操作"""
        event_list_checked = event_list_1.copy()
        for index, event in enumerate(event_list_1):
            time_local = event[0]
            event_type = event[1]
            event_args = event[2]

            if event_type == 'mouse_release':
                evnet_button = event_args['button']

                last_time_local = event_list_1[index - 1][0]
                last_event_type = event_list_1[index - 1][1]
                last_event_args = event_list_1[index - 1][2]
                last_evnet_button = last_event_args['button']

                time_difference = time_local - last_time_local

                if last_event_type == 'mouse_press' and evnet_button == last_evnet_button and time_difference < 0.2:
                    event_list_checked[index][1] = 'mouse_click'
                    event_list_checked[index][2]['clicks'] = 1
                    event_list_checked[index - 1] = ''
        # 剔除空值
        event_list_checked_2 = [i for i in event_list_checked if i]

        return event_list_checked_2

    def convert_mouse_click_join(event_list_2: list):
        """连续的鼠标点击释放操作替换为点击多次"""
        for index, event in enumerate(event_list_2):
            if index == 0:  # 跳过第一个
                continue

            time_local = event[0]
            event_type = event[1]
            event_args = event[2]

            if event_type == 'mouse_click':
                evnet_button = event_args['button']
                evnet_clicks = event_args['clicks'] if 'clicks' in event_args else 1

                last_time_local = event_list_2[index - 1][0]
                last_event_type = event_list_2[index - 1][1]
                last_event_args = event_list_2[index - 1][2]
                last_evnet_button = last_event_args['button']
                last_evnet_clicks = last_event_args['clicks'] if 'clicks' in last_event_args else 1

                time_difference = time_local - last_time_local

                if last_event_type == 'mouse_click' and evnet_button == last_evnet_button and time_difference < 0.2:
                    event_list_2[index][2]['clicks'] = evnet_clicks + last_evnet_clicks
                    event_list_2.pop(index - 1)
                    return convert_mouse_click_join(event_list_2)

        return event_list_2

    check_1 = convert_mouse_pr_to_click(event_list)
    check_2 = convert_mouse_click_join(check_1)

    return check_2


def get_original_data():
    """获取原始数据"""
    with open(listener_file, 'rb') as file:
        data_list = pickle.load(file)

    return convert_mouse_event(data_list)


def convert_to_pyautogui():
    """转换为args_dict格式"""
    command_data = []  # [{args_dict}, ...]
    event_list = get_original_data()
    event_list_checked = convert_mouse_event(event_list)
    last_time = 0
    for event in event_list_checked:
        time_local = event[0]
        event_type = event[1]
        event_args = event[2]
        # 提取数据
        time_difference = round(time_local - last_time, 2)
        if time_difference > 10000:  # 处理第一个时间差值
            time_difference = 0.25
        last_time = time_local
        x = int(event_args['x'])
        y = int(event_args['y'])
        button = event_args['button']
        scroll_direction = event_args['scroll_direction']
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
        elif event_type == 'mouse_click':  # 拆分为移动+点击
            # 移动
            command_move = default_args_dict.copy()
            command_move['command_type'] = 'command_mouse_move_absolute'
            command_move['x'] = x
            command_move['y'] = y
            command_move['duration'] = time_difference
            command_data.append(command_move)
            # 点击
            command_click = default_args_dict.copy()
            command_click['command_type'] = 'command_mouse_click'
            command_click['button'] = button
            command_click['clicks'] = event_args['clicks']
            command_data.append(command_click)
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
            command_scroll['scroll_direction'] = scroll_direction
            command_data.append(command_scroll)
        elif event_type == 'keyboard_press':  # 等待时间+键盘按下
            # 等待
            command_wait = default_args_dict.copy()
            command_wait['command_type'] = 'command_wait_time'
            command_wait['wait_time'] = time_difference
            command_data.append(command_wait)
            # 按下
            key_convert = convert_pynput_key(key)
            key_list = key_convert if type(key_convert) is list else [key_convert]
            for one_key in key_list:
                command_press = default_args_dict.copy()
                command_press['command_type'] = 'command_key_press'
                command_press['key'] = convert_pynput_key(one_key)
                command_data.append(command_press)
        elif event_type == 'keyboard_release':  # 等待时间+键盘释放
            # 等待
            command_wait = default_args_dict.copy()
            command_wait['command_type'] = 'command_wait_time'
            command_wait['wait_time'] = time_difference
            command_data.append(command_wait)
            # 释放
            key_convert = convert_pynput_key(key)
            key_list = key_convert if type(key_convert) is list else [key_convert]
            for one_key in key_list:
                command_press = default_args_dict.copy()
                command_press['command_type'] = 'command_key_release'
                command_press['key'] = convert_pynput_key(one_key)
                command_data.append(command_press)

    return command_data


def test():
    data = get_original_data()
    for i in data:
        print(i)


if __name__ == '__main__':
    test()
