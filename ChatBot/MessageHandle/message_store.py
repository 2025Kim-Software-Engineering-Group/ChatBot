from collections import defaultdict, deque

# 存储消息及其发送者
message_store = defaultdict(lambda: deque(maxlen=3))

def add_message(group_id, user_id, message):
    message_store[(group_id, message)].append(user_id)

def is_repeated(group_id, message, threshold=3):
    if len(message_store[(group_id, message)]) == threshold:
        return True
    return False