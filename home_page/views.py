# from django.http import HttpResponse
from django.shortcuts import render
from fun_package.user_verify import user_verify
# Create your views here.


def index(request):
    temple = user_verify.login_status(request)
    return render(request, 'index.html', {'username': temple})


def page_not_found(request):
    return render(request, '404.html', {})


def page_error(request):
    return render(request, '500.html', {})
