from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from . import models
from django.http import JsonResponse
# from . import forms
from fun_package.user_verify import user_verify
# Create your views here.


def login(request):

    # p = models.User.objects.filter(('user_name', 'qwe123'),)
    # print(p)
    if request.method == "POST":
        json_data = dict(jump_url=None, user_error=False)
        post = request.POST
        user_name = post.get('user_name', None)
        password = post.get('password', None)
        if user_name and password:
            user_name = user_name.strip()
            if models.User.objects.filter(user_name=user_name).exists():
                user = models.User.objects.get(user_name=user_name)
                if user.password == user_verify.encrypt_code(password):
                    request.session['is_login'] = True
                    request.session.set_expiry(0)       # 关闭浏览器时过期
                    # request.session.set_expiry(10)    # 10S后过期
                    # request.session.set_expiry(timedelta(days=5))    # 5天后过期
                    # request.session.set_expiry(None)      #永不关闭过期
                    request.session['user_name'] = user.user_name
                    json_data['jump_url'] = '/login/'
                else:
                    json_data['user_error'] = True
            else:
                json_data['user_error'] = True
        return JsonResponse(json_data)
        # return render(request, 'login.html', {'message': message})
    return render(request, 'login.html',)


def logout(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect('/')
    request.session.flush()
    return HttpResponseRedirect('/')


def register(request):
    # if request.method == 'POST':
    #     print(request.POST)
    if user_verify.login_status(request):
        return HttpResponseRedirect('/')
    # 注册页面当存在会话时则自动返回首页
    if request.method == 'POST':
        # message=''
        json_data = dict(jump_url=None)
        post = request.POST
        verify_code = ' '.join(post.get('verify_code')).lower()
        if verify_code == request.session['verification_code']:
            user_name = post.get('user_name')
            password1 = post.get('password1')
            password2 = post.get('password2')
            email = post.get('email')
            sex = post.get('sex')
            count_user_name = models.User.objects.filter(user_name=user_name).count()
            if not count_user_name:
                if password1 == password2:
                    count_email = models.User.objects.filter(email=email).count()
                    if not count_email:
                        new_user = models.User.objects.create(
                            user_name=user_name, password=user_verify.encrypt_code(password1), email=email, sex=sex
                        )
                        new_user.save()
                        json_data['jump_url'] = '/login/'
        return JsonResponse(json_data)
    return render(request, 'register.html',)


def duplicate_check(request):
    """用户名邮箱等字段重复性验证"""
    count = 0
    message = ''
    if request.method == 'GET':
        key = request.GET.get('k1')
        value = request.GET.get('k2')
        if key == 'verify_code':
            value = (' '.join(value)).lower()
            count = 0 if (value == request.session['verification_code']) else 1
        elif key and value:
            count = models.User.objects.filter((key, value),).count()
        else:
            message = "信息不能为空"
    else:
        message = '请求方式错误，请使用get请求'
    return JsonResponse({'count': count, 'error': message})


def captcha_set(request):
    text, image = user_verify.verification_code()
    request.session['verification_code'] = text.lower()
    return HttpResponse(image, content_type='image/png')
