# coding:utf-8
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group,Permission 
from django.contrib import messages
from django.template.context import RequestContext
from django.utils import timezone
import time
import os
import xlrd,xlwt
import numpy as np
import re

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#from bootstrap_toolkit.widgets import BootstrapUneditableInput
from .models import *
from .forms import *



# Create your views here.

def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')

def home(request):
    #初次访问
    if request.method == 'GET':
        loginform = LoginForm()
        return render_to_response('index.html', RequestContext(request, {'form': loginform,'msgbox': False,}))
    #已经post提交数据
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if not user.count():
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msgbox': True,'msg': '登录失败:用户不存在',})) 
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                #登录成功
                auth.login(request, user)
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msgbox': True,'msg': '登录成功',}))
            else:
                #登录失败
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msgbox': True,'msg': '登录失败:密码错误',}))
        else:
            #form无效
            return render_to_response('index.html', RequestContext(request, {'form': loginform,'msgbox': True,'msg': '登录失败:请完整填写信息',}))

 
from django.http import HttpResponse,JsonResponse
import json

def add(request):
    if 'a' in request.GET:
        a = request.GET['a']
        b = request.GET['b']
        a = int(a)
        b = int(b)
        return HttpResponse(str(a+b))
    return render(request, 'account/ajax.html')

from django.core import serializers #导入serializers模块
from datetime import datetime
def select_school(request):
    c = []
    if 'a' in request.GET:
        a = request.GET['a']
        b = School.objects.filter(location=a)
        if b.count():
            c.append(str("查询时间："+datetime.now().strftime('%Y-%m-%d %H:%I:%S')))
            for sch in b:
                c.append(str(sch.school_name)) 
        # 当使用表单请求方式的时候将下一行注释，由于表单是请求一整个页面，需用render返回页面，而ajax请求的是json数据，需要json的dump转换
        return HttpResponse(json.dumps(c), content_type="application/json")
    return render(request,'account/select_school.html')

def select_school_ajax_check(request):
    if request.method == 'POST':
        if 'school' in request.POST:
            a = request.POST['location']
            b = request.POST['school']
            c = ' 您选择的学校是：'+ a + b
            regform = RegisterForm()   
            return render(request, 'account/register.html',{'form': regform,'msgbox': True,'msg': c,'location': a,'school': b,}) 
        else:
            return HttpResponse('您没有选择学校，请返回选择学校！')

def register(request):
    #已经提交数据
    if request.method == 'POST':
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            truename = request.POST.get('truename', '')
            gradename = request.POST.get('gradename', '')
            classname = request.POST.get('classname', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            birthday = request.POST.get('birthday', '')
            gender = request.POST.get('gender', '')
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if user.count():
                return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msgbox': True,'msg': '注册失败:用户名已存在',}))
            #注册成功
            user = User.objects.create_user( username, email, password1 )
            #用户扩展信息   
            user.truename=truename 
            user.gradename=gradename 
            user.classname=classname 
            user.phone=phone 
            user.gender=gender 
            user.birthday=birthday
            user.schoolname = request.session.get('logined_user_school','') 
            user.districtname = request.session.get('logined_user_district','')
            user.cityname = request.session.get('logined_user_city','')
            user.provincename = request.session.get('logined_user_province','')
            user.usergroup = 'group_student' #默认以学生角色注册 
            user.creator = 'register'  
            user.save()  
            request.session['logined_user_truename']= truename  #写入session 

            #自动登录
            user = auth.authenticate(username=username, password=password1)#登录前需要先验证  
            if user is not None and user.is_active:
                auth.login(request, user) 
                return render_to_response('index.html', RequestContext(request, {'form': regform,'msgbox': True,'msg':'注册成功', }))          
        else:
            return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msgbox': True,'msg': '注册失败:请完整填写信息',}))        
#管理员添加学校
def add_school(request):
    if request.method == 'POST':
        if 'b' in request.POST:
            a = request.POST['a']
            b = request.POST['b']
            d = School.objects.filter(location=a)
            dd = School.objects.filter(location=a, school_name=b)
            if not d.count():#无该地区
                e = School()
                e.location = a
                e.school_name = b
                #e.admin = request.user
                c = a + ',' + b +' 为该地区首所学校，增加成功！ '
                e.save()
            elif not dd.count():#有该地区，无该学校
                e = School()
                e.location = a
                e.school_name = b
                #e.admin = request.user      
                c = a + ',' + b +' 增加成功！该地区有 '+ str(d.count() +1 )+' 所学校！'
                e.save() 
            else:
                c = ' 增加失败！ 该地区已有此校'
            return HttpResponse(str(c))
    return render(request, 'account/add_school.html')



 


def fgtpwd(request):
    	return render(request, 'account/changepassword.html')

def chgpwd(request):
    	return render(request, 'account/changepassword.html')

def self_info(request):
    	return render(request, 'account/userinfo.html')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

