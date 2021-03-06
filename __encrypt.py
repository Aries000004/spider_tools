#!-*- coding:utf-8 -*-
"""
rsa 加密相关及一些爬虫可能会用到的加密方法
"""
import os
import execjs
import codecs
import binascii
import base64
import hashlib
from pyDes import *
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from binascii import b2a_hex

def rsa_encrypt_ne(text, (n, e)):
    """rsa encrypt by n,e"""
    assert isinstance(n, long), "n should be long"
    assert isinstance(e, long), "n should be long"
    rsa_pubkey = RSA.construct((n, e))
    rsakey = rsa_pubkey.publickey()
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(text))
    return cipher_text

def b64tohex(b64_str):
    """base64编码转化为16进制"""
    b64_decode_str = base64.b64decode(b64_str)
    hex_str = binascii.b2a_hex(b64_decode_str) #b64_decode_str.encode('hex')
    return hex_str

def rsa_encrypt_by_pubkey(text, pubkey):
    """rsa encrypt by public key"""
    rsakey = RSA.importKey(pubkey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(text))
    return cipher_text

def rsa_encrypt(text, e, n):
    """rsa no padding加密模式"""
    text = text[::-1]
    rs = int(b2a_hex(text), 16) ** int(e, 16) % int(n, 16)
    return format(rs, 'x').zfill(256)

def md5(str):
    """封装md5处理"""
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def md5hex(word):
     """
     MD5加密算法，返回32位小写16进制符号
     """
     if isinstance(word, unicode):
         word = word.encode("utf-8")
     elif not isinstance(word, str):
         word = str(word)
     m = hashlib.md5()
     m.update(word)
     return m.hexdigest()

def des_encrypt(data):
    """
    des加密
    triple_des()，key Bytes containing the encryption key, must be either 16 or 24 bytes long
    des(), Bytes containing the encryption key, must be exactly 8 bytes
    """
    IV = "01234567"  # 偏转向量
    KEY = "private key"  # 密钥
    k = triple_des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(data))

def des_decrypt(data):
    """des解密"""
    IV = "01234567"     #偏转向量
    KEY = "private key"     #密钥
    k = triple_des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(data))

def des_encrypt_by_js(data, key1="YHXWWLKJYXGS",key2="ZFCHHYXFL10C",key3="DES"):
    """调用javascript封装DES通用加密算法"""
    des_js_filename = './js/des.js'
    assert os.path.isfile(des_js_filename)
    js_content = codecs.open(des_js_filename, encoding='utf-8').read()
    ctx = execjs.compile(js_content)
    en_str = ctx.call('strEnc', str(data), key1, key2, key3)
    return en_str

def enctypt_call_by_js(version, id_card):
    """execjs 执行js函数"""
    import execjs
    js_content = '''function abcMd5(s, s2) {
        s = s.replace(/\./g, "");
        var hhz = "9853398" + s + "7291166723";
        var len = hhz.length;
        var len2 = s2.length;
        if (len2 >= 18) {
            hhz = hhz.substring(6, 9) + s2.substring(4, 7) + hhz.substring(0, 4) + s2.substring(0, 4) + hhz.substring(len - 5) + s2.substring(11, 15) + hhz.substring(3, 7) + s2.substring(11) + hhz.substring(10, 14)
        } else if (len2 >= 10 && len < 18) {
            hhz = hhz.substring(6, 9) + s2.substring(4, 7) + hhz.substring(0, 4) + s2.substring(0, 4) + hhz.substring(len - 5) + s2.substring(11, 15) + hhz.substring(3, 7) + s2.substring(11) + hhz.substring(10, 14)
        }
        return hhz
    }
    '''
    ctx = execjs.compile(js_content)
    en_str = ctx.call('abcMd5', version, id_card)
    return en_str

if __name__ == "__main__":
    k1 = ''
    k2 = ''
    k3 = ''
    data = '41234123412342'
    print des_encrypt_by_js(data, k1, k2, k3)
    modules = long(133577494198148480)
    expotent = long(65537)
    text = 'test'
    print rsa_encrypt_ne(text, (modules, expotent))

    pubkey = """-----BEGIN PUBLIC KEY-----
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdvuIdeVk87qexa'
    'G1p22cSF7ymAwpjpGhiGPGl+wj8414zUR+EXdp0aXvhOS0zknjV/1'
    'VYVe10/YMnuDnyXVQx8owfWor3k+ok+spukUTJn1Vwa1CgiOXabZ1'
    'MbV+ipFTa3sHMaVyBoF3nPYUWPN0XYeP2g/f+GXeWTg7Sgw3q1QIDAQAB'
    -----END PUBLIC KEY-----
    """
    print rsa_encrypt_by_pubkey(text, pubkey)