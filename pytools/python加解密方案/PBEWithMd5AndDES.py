"""
PBEWithMD5AndDES Demo
"""

import base64
from Crypto.Hash import MD5
from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF1

from Crypto.Util.Padding import pad
import os

def decrypt(encrypted_b64, pkey):
    """
    基于PBEWithMD5AndDES解密
    """
    encrypted_data = base64.b64decode(encrypted_b64)
    salt = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    # 生成密钥和IV
    key_iv = PBKDF1(pkey.encode('utf-8'), salt, 16, 1000, MD5)
    key = key_iv[:8]
    iv = key_iv[8:16]

    # 解密
    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(ciphertext)

    # 去除PKCS7填充
    pad_length = decrypted[-1]
    decrypted = decrypted[:-pad_length]

    return decrypted.decode('utf-8')


def encrypt(plaintext, pkey):
    """
    基于PBEWithMD5AndDES加密
    """
    # 生成随机的8字节盐
    salt = os.urandom(8)

    # 使用PBKDF1生成密钥和IV
    key_iv = PBKDF1(pkey.encode('utf-8'), salt, 16, 1000, MD5)
    key = key_iv[:8]
    iv = key_iv[8:16]

    # 使用DES加密
    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    padded_data = pad(plaintext.encode('utf-8'), 8)
    encrypted_data = cipher.encrypt(padded_data)

    # 组合盐和加密数据，并进行Base64编码
    combined = salt + encrypted_data
    encrypted_b64 = base64.b64encode(combined).decode('utf-8')

    return encrypted_b64

if __name__ == '__main__':
    # 配置口令和明文
    # 口令
    pkey = 'fortest'

    my_pwd = '123455'
    encrypted_pwd = encrypt(my_pwd, pkey)
    print(f"原密码为：{my_pwd}")
    print(f"加密后为：{encrypted_pwd}")

    # 解密
    # encrypted_pwd = ''
    decrypted_pwd = decrypt(encrypted_pwd, pkey)
    print(f"解密后为：{decrypted_pwd}")
