import random
import string

import re
import os
from datetime import datetime


def gen_password(length = 12):
    """ 生成随机密码 """
    # 字符集
    characters = ''

    # 大小写英文
    # characters += string.ascii_letters
    # 大写
    characters += string.ascii_uppercase
    # 小写
    characters += string.ascii_lowercase
    # 数字
    characters += string.digits
    # 特殊字符
    characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    # 确保密码包含所有要求的字符类型
    if not any(c.isupper() for c in password):
        # 确保至少有一个大写字母
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.ascii_uppercase) + password[pos + 1:]

    if not any(c.islower() for c in password):
        # 确保至少有一个小写字母
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.ascii_lowercase) + password[pos + 1:]

    if not any(c.isdigit() for c in password):
        # 确保至少有一个数字
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.digits) + password[pos + 1:]

    if not any(c in string.punctuation for c in password):
        # 确保至少有一个特殊字符
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.punctuation) + password[pos + 1:]

    pwd_strength = assess_password_strength(password)
    score = pwd_strength['score']
    break_time = pwd_strength['break_time']
    strength = pwd_strength['strength']

    print(f"===> 生成密码:\t{password}\t[{strength} {score}], 估计需要破解时间: {break_time}")

    return password


def assess_password_strength(password):
    """评估密码强度"""
    # 计算密码长度得分
    length_score = min(len(password) * 4, 40)

    # 计算字母得分
    upper_count = sum(1 for c in password if c.isupper())
    lower_count = sum(1 for c in password if c.islower())
    letter_count = upper_count + lower_count

    if letter_count == 0:
        letter_score = 0
    else:
        if upper_count == 0 or lower_count == 0:
            letter_score = letter_count * 2
        else:
            letter_score = letter_count * 4

    # 计算数字得分
    digit_count = sum(1 for c in password if c.isdigit())

    if digit_count == 0:
        digit_score = 0
    elif digit_count == len(password):
        digit_score = digit_count * 2
    else:
        digit_score = digit_count * 4

    # 计算特殊字符得分
    special_count = sum(1 for c in password if c in string.punctuation)
    special_score = special_count * 6

    # 计算额外加分
    extra_score = 0

    # 字母和数字混合
    if letter_count > 0 and digit_count > 0:
        extra_score += 2

    # 字母、数字和特殊字符混合
    if letter_count > 0 and digit_count > 0 and special_count > 0:
        extra_score += 3

    # 大小写字母和数字混合
    if upper_count > 0 and lower_count > 0 and digit_count > 0:
        extra_score += 3

    # 大小写字母、数字和特殊字符混合
    if upper_count > 0 and lower_count > 0 and digit_count > 0 and special_count > 0:
        extra_score += 5

    # 计算总分
    total_score = length_score + letter_score + digit_score + special_score + extra_score

    # 根据总分评估强度
    if total_score >= 80:
        strength = "非常强"
    elif total_score >= 60:
        strength = "强"
    elif total_score >= 40:
        strength = "中等"
    else:
        strength = "弱"

    return {
        "score": total_score,
        "strength": strength,
        "break_time": estimate_break_time(total_score)
    }


def estimate_break_time(score):
    """估计破解密码所需时间"""
    seconds = 10 ** (score / 10)

    if seconds < 60:
        return f"{seconds:.2f} 秒"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} 分钟"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} 小时"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} 天"
    else:
        return f"{seconds / 31536000:.2e} 年"


if __name__ == '__main__':
    length = 8
    print(f'===> 开始生成密码，长度：{length} ===')
    for _ in range(10):
        # print(gen_password(length))
        gen_password(length)