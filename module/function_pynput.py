"""pynput封装"""

import pickle
import time

from pynput import mouse, keyboard

quit_key = keyboard.Key.esc


class ListenerPynput:
    """鼠标事件监听器"""

    def __init__(self):
        self.event_list = []  # 存储事件，格式[[本地时间,事件类型,事件参数{event_data}],...]
        self.event_data = {'x': 1, 'y': 1, 'button': '左键', 'scroll_direction': '向上', 'key': ''}

        self.mouse_listener = mouse.Listener(on_move=None,
                                             on_click=self.mouse_click,
                                             on_scroll=self.mouse_scroll)

        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_press,
                                                   on_release=self.keyboard_release, )

    def listener_event(self, event_type, event_data):
        """存储事件数据"""
        event_time = time.time()
        self.event_list.append([event_time, event_type, event_data])

    def save_to_local(self):
        """保存事件数据至本地，用于主线程与子线程之间的连接"""
        with open("listener.pickle", "wb") as file:
            pickle.dump(self.event_list, file)

    def mouse_move_position(self, x, y):
        """鼠标移动事件"""
        # 不使用
        event_data = self.event_data.copy()
        event_data['x'] = x
        event_data['y'] = y
        self.listener_event('mouse_move', event_data)

    def mouse_click(self, x, y, button, pressed):
        """鼠标点击事件"""
        if button == mouse.Button.left:
            mouse_button = '左键'
        elif button == mouse.Button.middle:
            mouse_button = '中键'
        elif button == mouse.Button.right:
            mouse_button = '右键'
        else:
            mouse_button = None

        if pressed:  # True为按下
            mouse_event = 'mouse_press'
        else:  # False为释放
            mouse_event = 'mouse_release'

        event_data = self.event_data.copy()
        event_data['x'] = x
        event_data['y'] = y
        event_data['button'] = mouse_button
        self.listener_event(mouse_event, event_data)

    def mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮事件"""
        if dy > 0:
            direction = '向上'
        else:
            direction = '向下'

        event_data = self.event_data.copy()
        event_data['x'] = x
        event_data['y'] = y
        event_data['scroll_direction'] = direction
        self.listener_event('mouse_scroll', event_data)

    def get_listener(self):
        return self.mouse_listener, self.keyboard_listener

    def keyboard_press(self, key):
        """键盘按下事件"""
        if key == quit_key:  # 设置退出事件
            self.save_to_local()
            return False

        event_data = self.event_data.copy()
        event_data['key'] = key
        self.listener_event('keyboard_press', event_data)

    def keyboard_release(self, key):
        """键盘释放事件"""
        event_data = self.event_data.copy()
        event_data['key'] = key
        self.listener_event('keyboard_release', event_data)


def test():
    t1, t2 = ListenerPynput().get_listener()
    t1.start()
    t2.start()
    t2.join()


if __name__ == '__main__':
    test()
