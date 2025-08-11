"""
提供Base64加解密方法、PBEWithMD5AndDES加解密方法
cmd> python key_pass.py -f=b -T="Pkt2eyw2J3I="
"""
import argparse
import base64
from Crypto.Hash import MD5
from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF1

from Crypto.Util.Padding import pad
import os

import sys


class KeyPass(object):
    """ pmd 默认key """
    pmd_key = "Pkt2eyw2J3I="


def base64_encode(plaintext):
    """Base64加密"""
    encode_bytes = base64.b64encode(plaintext.encode('utf-8'))
    encode_str = encode_bytes.decode('utf-8')
    return encode_str


def base64_decode(encode_str):
    """Base64解密"""
    decode_bytes = base64.b64decode(encode_str.encode('utf-8'))
    decode_str = decode_bytes.decode('utf-8')
    return decode_str


def pmd_encrypt(plaintext, pkey):
    """基于PBEWithMD5AndDES加密"""
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


def pmd_decrypt(encrypted_b64, pkey):
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


def help():
    print("usage: edtool [-h] [-e] [-b] [key] text \r\n"
          "字符加解密工具 \r\n"
          "positional arguments: \r\n"
          "  text\t\t需要加解密的文本 \r\n"
          "  key\t\tPBEWithMd5AndDES自定义Key \r\n"
          "optional arguments: \r\n"
          "  -h, --help\t\tshow this help message and exit \r\n"
          "  -e ENCRYPT\t\t加密，默认为解密 \r\n"
          "  -b BASE64\t\t使用Base64，默认为PBEWithMd5AndDES")

def main():
    """接收参数"""
    parser = argparse.ArgumentParser(description='字符加解密工具')
    parser.add_argument('-t', '--type', help='加解密类型：e:加密/d:解密（默认：d）', default='d')
    parser.add_argument('-f', '--func', help='加解密方法：b:Base64/p:PBEWithMd5AndDES（默认：p）', default='p')
    parser.add_argument('-k', '--key', help='PBEWithMd5AndDES自定义Key', default=base64_decode(KeyPass.pmd_key))
    parser.add_argument('text', help='需要加解密的文本')
    args = parser.parse_args()

    if args.text == '':
        print("请输入需要加解密的文本")
        return

    print(f"=== 原文本：{args.text}")

    if args.func == 'b' or args.func == 'base64':
        if args.type == 'e' or args.type == 'encode':
            print(f"=== Base64加密结果：{base64_encode(args.text)}")
        elif args.type == 'd' or args.type == 'decode':
            print(f"=== Base64解密结果：{base64_decode(args.text)}")
        else:
            print("暂无此类型处理")
    elif args.func == 'p' or args.func == 'pmd':
        if args.type == 'e' or args.type == 'encode':
            print(f"=== PMD加密结果：{pmd_encrypt(args.text, args.key)}")
        elif args.type == 'd' or args.type == 'decode':
            print(f"=== PMD解密结果：{pmd_decrypt(args.text, args.key)}")
        else:
            print("暂无此类型处理")
    else:
        print("暂无此类型方法")


if __name__ == '__main__':
    # main()
    text = '7777^7'
    key =  '123456'

    en_text = pmd_encrypt(text, key)
    print(f"=== PMD加密结果：{en_text}")

    print(f"=== PMD解密结果：{pmd_decrypt(en_text, key)}")