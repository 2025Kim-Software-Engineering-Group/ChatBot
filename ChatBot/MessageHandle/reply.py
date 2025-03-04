
import requests

def sendMessage(message_type, user_id, group_id, message):
    # 发送HTTP请求
    http_url = f'http://127.0.0.1:3000/send_msg'
    payload = {
        'message_type': message_type,
        'user_id': user_id,
        'group_id': group_id,
        'message': message
    }
    response = requests.post(http_url, json=payload)
    print(response.text)

    # 打印消息
    if message_type == 'group':
        print(f"发送群消息到 [群号: {group_id}] 用户 {user_id}: {message}")
    elif message_type == 'private':
        print(f"发送私聊消息到 用户 {user_id}: {message}")






