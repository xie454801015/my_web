# -*- coding:utf-8 -*-
# from django.http import HttpResponse
import hashlib
from captcha.image import ImageCaptcha
import exrex



def login_status(request):
    """会话登入状态判断，并返回用户名"""
    if request.session.get('is_login', None):
        temple = request.session['user_name']
    else:
        temple = None
    return temple


def encrypt_code(s, salt='hello_login'):
    """给字段加密"""
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def verification_code():
    """生成一个4个字符的验证码以及验证码图片"""
    captcha_text = exrex.getone('[a-zA-Z1-9]{4}')
    image = ImageCaptcha()
    captcha_text = ' '.join(captcha_text)
    captcha = image.generate(captcha_text)  # 生成的图片是字节流
    return captcha_text, captcha.getvalue()


