"""配置文件相关方法
其他说明：
全局设置在一个ini中
一个配置文件为一个文件夹，文件夹名即为配置名，内部一个ini和截图文件"""

import configparser
import os

import send2trash

from module.constant_default import *
from module.function_general import *


def check_default_config():
    """检查初始配置文件"""
    if not os.path.exists(configs_folder):
        os.makedirs(configs_folder)

    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

    if not os.path.exists(global_config):
        with open(global_config, 'w', encoding='utf-8') as gw:
            setting = """[DEFAULT]
loop_time = 1
global_wait_time = 0.5
find_image_timeout = 60
"""
            gw.write(setting)

    config_list = [i for i in os.listdir(configs_folder) if os.path.isdir(os.path.join(configs_folder, i))]
    if not config_list:  # 检查配置文件
        add_config('默认')
    else:
        for config_name in config_list:
            config_path = f'{configs_folder}/{config_name}/{command_config}'
            if not os.path.exists(config_path):
                save_command_config(config_name)


def get_config_find_image_timeout():
    """获取寻图超时时间设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    timeout = int(config.get('DEFAULT', 'find_image_timeout'))

    return timeout


def update_config_find_image_timeout(timeout: int):
    """更新寻图超时时间设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    config.set('DEFAULT', 'find_image_timeout', str(timeout))
    config.write(open(global_config, 'w', encoding='utf-8'))


def update_config_loop_time(loop_time: int):
    """更新总循环次数设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    config.set('DEFAULT', 'loop_time', str(loop_time))
    config.write(open(global_config, 'w', encoding='utf-8'))


def get_config_loop_time():
    """获取总循环次数设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    loop_time = int(config.get('DEFAULT', 'loop_time'))

    return loop_time


def update_config_wait_time(wait_time: float):
    """更新指令间隔设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    config.set('DEFAULT', 'global_wait_time', str(wait_time))
    config.write(open(global_config, 'w', encoding='utf-8'))


def get_config_wait_time():
    """获取指令间隔设置"""
    config = configparser.ConfigParser()
    config.read(global_config, encoding='utf-8')
    wait_time = float(config.get('DEFAULT', 'global_wait_time'))

    return wait_time


def get_config_items():
    """获取所有配置文件项"""
    config_list = [i for i in os.listdir(configs_folder) if os.path.isdir(os.path.join(configs_folder, i))]

    return config_list


def add_config(config_name: str):
    """新建配置文件"""
    config_list = get_config_items()
    checked_config = check_filename_feasible(config_name, replace=True)
    if checked_config in config_list:  # 如果有重复，则添加随机后缀
        random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
        checked_config = f"{checked_config}_{random_string}"
    config_path = f'{configs_folder}/{checked_config}'
    os.makedirs(config_path)

    save_command_config(config_name)  # 添加初始ini

    return checked_config


def delete_config(config_name: str):
    """删除配置文件"""
    config_path = f'{configs_folder}/{config_name}'
    if os.path.exists(config_path):
        send2trash.send2trash(config_path)


def get_command_list(config_name: str):
    """获取配置文件中的参数设置
    command_list结构：[{args_dict字典}, ...]"""
    config_path = f'{configs_folder}/{config_name}/{command_config}'
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')

    command_list = []
    for section in config.sections():
        args_dict = {}
        keys = config.options(section)
        for key in keys:
            value = config.get(section, key)
            try:
                convert_value = eval(value)  # 将str格式的int或float转换为其真实格式
            except NameError:  # 如果真实格式为str，则执行eval会报错
                convert_value = value
            except SyntaxError:  # 如果文本为''，则执行eval会报错
                convert_value = value

            args_dict[key] = convert_value
        command_list.append(args_dict)

    return command_list


def save_command_config(config_name: str, command_list: list = None):
    """保存参数设置到配置文件
    command_list结构：[{args_dict字典}, ...]"""
    config_path = f'{configs_folder}/{config_name}/{command_config}'
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8'):
            pass
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')

    # 清空
    config.clear()

    # 检查
    if command_list is None:
        command_list = [default_args_dict.copy()]

    # 写入
    index = 0
    for args_dict in command_list:
        index += 1
        config.add_section(str(index))
        for key, value in args_dict.items():
            config.set(str(index), key, str(value))
    config.write(open(config_path, 'w', encoding='utf-8'))
