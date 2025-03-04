import json
import threading
import time
from datetime import datetime, timedelta
from .reply import sendMessage
from SignIn.process import signIn  # 导入签到函数
from .message_store import add_message, is_repeated

# 存储定时提醒的列表
reminders = []

def add_reminder(user_id, group_id, message, remind_time):
    reminders.append({
        "user_id": user_id,
        "group_id": group_id,
        "message": message,
        "remind_time": remind_time
    })

def check_reminders():
    while True:
        now = datetime.now()
        for reminder in reminders:
            if now >= reminder["remind_time"]:
                sendMessage('group', reminder["user_id"], reminder["group_id"], f"提醒：{reminder['message']}")
                reminders.remove(reminder)
        time.sleep(60)  # 每分钟检查一次

# 启动检查提醒的线程
threading.Thread(target=check_reminders, daemon=True).start()

thread_local_data = threading.local()

def parse_time(time_str):
    now = datetime.now()
    remind_time = now

    if "明天" in time_str:
        remind_time += timedelta(days=1)
    elif "后天" in time_str:
        remind_time += timedelta(days=2)

    if "早上" in time_str:
        hour = int(time_str.split("早上")[1].replace("点", ""))
        remind_time = remind_time.replace(hour=hour, minute=0, second=0, microsecond=0)
    elif "中午" in time_str:
        remind_time = remind_time.replace(hour=12, minute=0, second=0, microsecond=0)
    elif "下午" in time_str:
        hour = int(time_str.split("下午")[1].replace("点", "")) + 12
        if hour >= 24:
            hour -= 12  # 修正小时数，确保在0到23之间
        remind_time = remind_time.replace(hour=hour, minute=0, second=0, microsecond=0)
    elif "晚上" in time_str:
        hour = int(time_str.split("晚上")[1].replace("点", "")) + 18
        if hour >= 24:
            hour -= 12  # 修正小时数，确保在0到23之间
        remind_time = remind_time.replace(hour=hour, minute=0, second=0, microsecond=0)

    return remind_time

def handleMessage(data):
    data = json.loads(data)
    thread_local_data.post_type = data["post_type"]

    if thread_local_data.post_type != 'message':
        return

    thread_local_data.message_type = data['message_type']
    thread_local_data.time = data['time']
    thread_local_data.raw_message = data["raw_message"]
    thread_local_data.nickname = data["sender"]["nickname"]
    thread_local_data.user_id = data["sender"]["user_id"]

    if thread_local_data.message_type == 'private':
        print(f"私聊消息 [{thread_local_data.time}] {thread_local_data.nickname}({thread_local_data.user_id}): {thread_local_data.raw_message}")

    elif thread_local_data.message_type == 'group':
        thread_local_data.group_id = data["group_id"]
        print(f"群聊消息 [{thread_local_data.time}] [群号: {thread_local_data.group_id}] {thread_local_data.nickname}({thread_local_data.user_id}): {thread_local_data.raw_message}")

        # 记录消息
        add_message(thread_local_data.group_id, thread_local_data.user_id, thread_local_data.raw_message)

        # 检测重复消息
        if is_repeated(thread_local_data.group_id, thread_local_data.raw_message):
            sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, thread_local_data.raw_message)

        # 自动回复特定消息
        if thread_local_data.raw_message == 'hi':
            print("小")
            message = 'o/'
            sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, message)

        # 触发签到功能
        if thread_local_data.raw_message == '签到':
            success, message = signIn(thread_local_data.user_id)
            if success:
                sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, message)

        # 计算器功能
        if thread_local_data.raw_message.startswith('计算'):
            expression = thread_local_data.raw_message[2:].strip()
            try:
                # 替换乘法符号
                expression = expression.replace('×', '*').replace('x', '*')
                result = eval(expression)
                sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, f"结果是: {result}")
            except Exception as e:
                sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, f"计算错误: {e}")

        # 定时提醒功能
        if thread_local_data.raw_message.startswith('提醒我'):
            try:
                parts = thread_local_data.raw_message.split(maxsplit=2)
                if len(parts) < 3:
                    raise ValueError("输入格式错误，请使用'提醒我 [时间] [内容]'格式")

                time_part = parts[1]
                message_part = parts[2]

                # 调试信息
                print(f"解析时间部分: {time_part}")
                print(f"提醒内容: {message_part}")

                # 解析时间部分，支持全时间格式
                remind_time = parse_time(time_part)

                # 调试信息
                print(f"解析后的提醒时间: {remind_time}")

                add_reminder(thread_local_data.user_id, thread_local_data.group_id, message_part, remind_time)
                sendMessage('group', thread_local_data.user_id, thread_local_data.group_id,
                            f"提醒已设置：{message_part}，时间：{remind_time}")
            except Exception as e:
                sendMessage('group', thread_local_data.user_id, thread_local_data.group_id, f"设置提醒失败：{e}")
                print(f"设置提醒失败：{e}")