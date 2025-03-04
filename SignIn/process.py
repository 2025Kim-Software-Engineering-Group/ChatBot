# SignIn/process.py (需要创建)
import random
import datetime

from .models import UserSignIn


def signIn(user_id):
    user, created = UserSignIn.objects.get_or_create(user_id=user_id)

    point = user.point

    date = datetime.date.today()
    if date == user.last_signin and not created:
        return True, f"你已经签到过了！当前拥有{point}点。"

    point_add = random.randint(1, 10)
    point += point_add
    user.point = point
    user.save()

    return True, f"签到成功！当前拥有{point}点。"
