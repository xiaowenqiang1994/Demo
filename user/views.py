from django.shortcuts import render, redirect
from user.forms import RegisterForm
from django.contrib.auth.hashers import make_password,check_password

from user.models import User

# Create your views here.


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
            if check_password(password, user.password):
                request.session['uid'] = user.id
                request.session['nickname'] = user.nickname
                return redirect('/user/user_info/')
            else:
                return render(request, 'login.html', {'error': '账户密码错误'})

        except User.DoesNotExist as e:
            return render(request, 'login.html', {'error': '账户密码错误'})
    return render(request, 'login.html', {})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # 密码加密
            user.password = make_password(user.password)
            user.save()
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/user_info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')

def user_info(request):
    uid = request.session.get('uid')
    if uid:
        user = User.objects.get(id=uid)
        return render(request, 'user_info.html', {'user': user})


def logout(request):
    request.session.flush()
    return redirect('/')
