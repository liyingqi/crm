from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.plugins.md5 import encryption
from crm.plugins.forms import RegForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        pwd = encryption(user,pwd)
        ret = models.UserProfile.objects.filter(username=user,password=pwd).first()
        if ret:
            request.session['user_id'] = ret.id
            return redirect(reverse('customer_list'))
        else:
            msg = '用户名或密码错误!'
            return render(request,'login.html',locals())

    return render(request, 'login.html', locals())


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            try:
                obj = form_obj.save()
                dep_obj = obj.department
                if dep_obj:
                    dep_obj.count += 1
                    dep_obj.save()
                return redirect(reverse('login'))
            except Exception as e:
                return render(request,'reg.html',{'msg':'用户名已存在','form_obj':form_obj})

    return render(request, 'reg.html', locals())

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))