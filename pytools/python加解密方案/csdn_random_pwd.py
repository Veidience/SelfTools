import random
import string
import pyperclip  # 用于复制到剪贴板
import re
import os
from datetime import datetime

def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                      include_digits=True, include_special=True):
    """生成随机密码"""
    # 初始化字符集
    characters = ''
    
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special:
        characters += string.punctuation
    
    # 检查是否至少选择了一种字符类型
    if not characters:
        raise ValueError("至少选择一种字符类型")
    
    # 生成密码
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # 确保密码包含所有要求的字符类型
    if include_uppercase and not any(c.isupper() for c in password):
        # 确保至少有一个大写字母
        pos = random.randint(0, length-1)
        password = password[:pos] + random.choice(string.ascii_uppercase) + password[pos+1:]
    
    if include_lowercase and not any(c.islower() for c in password):
        # 确保至少有一个小写字母
        pos = random.randint(0, length-1)
        password = password[:pos] + random.choice(string.ascii_lowercase) + password[pos+1:]
    
    if include_digits and not any(c.isdigit() for c in password):
        # 确保至少有一个数字
        pos = random.randint(0, length-1)
        password = password[:pos] + random.choice(string.digits) + password[pos+1:]
    
    if include_special and not any(c in string.punctuation for c in password):
        # 确保至少有一个特殊字符
        pos = random.randint(0, length-1)
        password = password[:pos] + random.choice(string.punctuation) + password[pos+1:]
    
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
        return f"{seconds/60:.2f} 分钟"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} 小时"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} 天"
    else:
        return f"{seconds/31536000:.2e} 年"

def save_password(password, service=""):
    """保存密码到文件"""
    try:
        # 创建保存密码的目录（如果不存在）
        if not os.path.exists("passwords"):
            os.makedirs("passwords")
        
        # 确定文件名
        filename = "passwords/passwords.txt"
        
        # 添加密码到文件
        with open(filename, "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {service}: {password}\n")
        
        return filename
    except Exception as e:
        print(f"保存密码时出错: {e}")
        return None

def advanced_password_generator():
    """高级密码生成器主函数"""
    print("欢迎使用高级密码生成器！")
    
    try:
        while True:
            print("\n=== 菜单 ===")
            print("1. 生成单个密码")
            print("2. 批量生成密码")
            print("3. 退出")
            
            choice = input("请选择操作 (1-3): ")
            
            if choice == '3':
                print("感谢使用密码生成器，再见！")
                break
            
            try:
                length = int(input("请输入密码长度 (默认16): ") or "16")
            except ValueError:
                print("错误: 请输入有效的整数")
                continue
            
            # 确认是否包含各种字符类型
            include_uppercase = input("包含大写字母? (y/n, 默认y): ").lower() != 'n'
            include_lowercase = input("包含小写字母? (y/n, 默认y): ").lower() != 'n'
            include_digits = input("包含数字? (y/n, 默认y): ").lower() != 'n'
            include_special = input("包含特殊字符? (y/n, 默认y): ").lower() != 'n'
            
            if choice == '1':
                # 生成单个密码
                password = generate_password(
                    length, include_uppercase, include_lowercase, include_digits, include_special
                )
                
                # 评估密码强度
                strength = assess_password_strength(password)
                
                print(f"\n生成的随机密码: {password}")
                print(f"密码强度: {strength['strength']} (得分: {strength['score']})")
                print(f"估计破解时间: {strength['break_time']}")
                
                # 提供复制选项
                copy_choice = input("是否复制密码到剪贴板? (y/n): ").lower()
                if copy_choice == 'y':
                    pyperclip.copy(password)
                    print("密码已复制到剪贴板！")
                
                # 提供保存选项
                save_choice = input("是否保存密码到文件? (y/n): ").lower()
                if save_choice == 'y':
                    service = input("请输入服务名称 (可选): ")
                    filename = save_password(password, service)
                    if filename:
                        print(f"密码已保存到 {filename}")
            
            elif choice == '2':
                # 批量生成密码
                try:
                    count = int(input("请输入要生成的密码数量 (默认5): ") or "5")
                except ValueError:
                    print("错误: 请输入有效的整数")
                    continue
                
                print("\n生成的随机密码:")
                passwords = []
                
                for i in range(count):
                    password = generate_password(
                        length, include_uppercase, include_lowercase, include_digits, include_special
                    )
                    passwords.append(password)
                    print(f"{i+1}. {password}")
                
                # 提供复制选项
                copy_choice = input("是否复制某个密码到剪贴板? (输入编号, 或按回车跳过): ")
                if copy_choice and copy_choice.isdigit() and 1 <= int(copy_choice) <= count:
                    index = int(copy_choice) - 1
                    pyperclip.copy(passwords[index])
                    print(f"密码 {copy_choice} 已复制到剪贴板！")
                
                # 提供保存选项
                save_choice = input("是否保存这些密码到文件? (y/n): ").lower()
                if save_choice == 'y':
                    service = input("请输入服务名称 (可选): ")
                    for password in passwords:
                        save_password(password, f"{service} (自动生成)")
                    print(f"所有密码已保存到 passwords/passwords.txt")
            
            else:
                print("无效选择，请重新输入！")
    
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

# 启动密码生成器
advanced_password_generator()

