# coding:utf-8
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse  
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group,Permission 
from django.contrib import messages
from django.template.context import RequestContext
from django.utils import timezone
import time,datetime
import os
import xlrd,xlwt
import numpy as np
import re
import json

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers #导入serializers模块
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
        return render_to_response('index.html', RequestContext(request, {'form': loginform,}))
    #已经post提交数据
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if not user.count():
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msg': '登录失败:用户不存在',})) 
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                #登录成功
                auth.login(request, user)
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msg': '登录成功',}))
            else:
                #登录失败
                return render_to_response('index.html', RequestContext(request, {'form': loginform,'msg': '登录失败:密码错误',}))
        else:
            #form无效
            return render_to_response('index.html', RequestContext(request, {'form': loginform,'msg': '登录失败:请完整填写信息',}))

def login(request): 
    #已经post提交数据
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #用户名是否存在
            user = User.objects.filter(username=username)
            if not user.count():
                c = ' 登录失败！ 用户名不存在'
                return HttpResponse(str(c))
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                #登录成功
                auth.login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                #登录失败
                return render_to_response('index.html', RequestContext(request, {
                    'form': loginform,
                    'password_is_wrong':True,
                    }))
        else:
            #form无效
            return render_to_response('index.html', RequestContext(request, {
                'form': loginform,
                'password_is_wrong':True,
                }))


@permission_required('user.is_staff')
def add_school(request):
    provinces_recent = Province.objects.all().order_by('province_name','-create_time')[:10]
    citys_recent = City.objects.all().order_by('city_name','-create_time')[:10]
    districts_recent = District.objects.all().order_by('district_name','-create_time')[:10]
    schools_recent = School.objects.values("school_name").distinct() [:10]
    classes_recent = Class.objects.values("class_name").distinct() [:10]
    province_form = add_province_model_form()
    city_form = add_city_model_form()
    district_form = add_district_model_form()
    school_form = add_school_model_form()
    class_form = add_class_model_form()
    msg = ''
    if request.method == 'POST':
        province_form = add_province_model_form(request.POST)
        city_form = add_city_model_form(request.POST)
        district_form = add_district_model_form(request.POST)
        school_form = add_school_model_form(request.POST)
        class_form = add_class_model_form(request.POST)
        if province_form.is_valid():
            province_name = request.POST.get('province_name', '').strip()
            try:
                pro = Province.objects.get(province_name=province_name)
            except:#不重名则新建
                pro = Province()
                pro.province_name = province_name
                pro.creater = request.user
                pro.save()
            if city_form.is_valid():
                city_name = request.POST.get('city_name', '').strip()
                try:
                    city = City.objects.get(province_foreign=pro,city_name=city_name)
                except:#不重名则新建
                    city = City()
                    city.city_name = city_name
                    city.province_foreign = pro
                    city.creater = request.user
                    city.save()
                if district_form.is_valid():
                    district_name = request.POST.get('district_name', '').strip()
                    try:
                        district = District.objects.get(city_foreign = city,district_name=district_name)
                    except:#不重名则新建
                        district = District()
                        district.district_name = district_name
                        district.city_foreign = city
                        district.creater = request.user
                        district.save()
                    if school_form.is_valid():
                        school_name = request.POST.get('school_name', '').strip()
                        try:
                            school = School.objects.get(district_foreign = district,school_name=school_name)
                        except:#不重名则新建
                            school_stage = request.POST.get('school_stage', '').strip()
                            school_code = request.POST.get('school_code', '').strip()
                            location = str(province_name)+'-'+str(city_name)+'-'+str(district_name)
                            # 当前时间
                            now_time = datetime.datetime.now()
                            available_time = datetime.datetime(month=now_time.month, year=now_time.year + 1, day=now_time.day)
                            school = School()
                            school.school_name = school_name
                            school.school_stage = school_stage
                            school.school_code = school_code
                            school.district_foreign = district
                            school.location = location
                            school.available_time = available_time
                            school.creater = request.user
                            school.admin = request.user
                            school.save()

                        if class_form.is_valid():
                            class_name = request.POST.get('class_name', '').strip()
                            try:
                                clas = Class.objects.get(school_foreign = school,class_name=class_name)
                                msg = '添加失败，存在重名班级'
                            except:#不重名则新建
                                clas = Class()
                                clas.class_name = class_name
                                clas.school_foreign = school
                                clas.creater = request.user
                                clas.admin = request.user
                                clas.save()
                                msg = str(province_name)+'-'+str(city_name)+'-'+str(district_name) +'-'+str(school_name)+'-'+str(class_name)+', 添加成功！'       

    return render(request, 'account/add_school.html',{'msg': msg,'form1': province_form,'form2': city_form,'form3': district_form,'form4': school_form,'form5': class_form,
                    'province': provinces_recent,'city': citys_recent,'district': districts_recent,'school': schools_recent,'class': classes_recent,})
@login_required
@permission_required('user.is_staff', login_url="/")
def list_school(request):
    provinces_all = Province.objects.all().order_by('province_name')
    citys_all = City.objects.all().order_by('city_name')
    districts_all = District.objects.all().order_by('district_name')
    schools_all = School.objects.all().order_by('school_name')
    classes_all = Class.objects.all().order_by('class_name')
    

    return render(request, 'account/list_school.html',{
                    'province': provinces_all,'city': citys_all,'district': districts_all,'school': schools_all,'class': classes_all,})





def select_school3(request):
    #pros_json = serializers.serialize("json",sheng)
    return render(request,'account/select_school3.html')


def confirm_school(request):
    regform = RegisterForm(request.POST)
    #已经提交数据
    if request.method == 'POST':
        sheng = request.POST['shengshi']['ss']
        shi = request.POST['shengshi']['sq']
        qu = request.POST['shengshi']['xs']
        xiao = request.POST['shengshi']['xx']
        ban = request.POST['shengshi']['bj']
        msg = '学校选择成功，您选择的学校是：'+ sheng + shi + qu + xiao + ban
        return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': msg,}))  



def register(request):
    #已经提交数据
    if request.method == 'POST':
        regform = RegisterForm(request.POST)
        if 'shengshi' in request.POST:
            sheng = request.POST['shengshi']['ss']
            shi = request.POST['shengshi']['sq']
            qu = request.POST['shengshi']['xs']
            xiao = request.POST['shengshi']['xx']
            ban = request.POST['shengshi']['bj']
            msg = '学校选择成功，您选择的学校是：'+ sheng + shi + qu + xiao + ban
            return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': msg,}))  
        elif 'username' in request.POST:
            location = request.POST.get('location', '')
            school_name = request.POST.get('school', '')
            school = get_object_or_404(School,location=location,school_name=school_name)
            #classname = request.POST.get('classname', '')
            #inschool_date = request.POST.get('gradename', '')
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if user.count():
                return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': '注册失败:用户名已存在',}))
            #注册成功
            user = User.objects.create_user( username, email, password1 )
            #用户扩展信息   
            user.location = location 
            user.school = school
            user.save()

            #自动登录
            user = auth.authenticate(username=username, password=password1)#登录前需要先验证  
            if user is not None and user.is_active:
                auth.login(request, user) 
                return render_to_response('account/register.html', RequestContext(request, {'form': None,'msg':'注册成功', }))          
        else:
            return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': '注册失败:请完整填写信息',}))    
def complete_self_info(request):
    #已经提交数据
    if request.method == 'POST':
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            user = request.user
            #classname = request.POST.get('classname', '')
            #inschool_date = request.POST.get('gradename', '')
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            real_name = request.POST.get('truename', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            birthday = request.POST.get('birthday', '')
            gender = request.POST.get('gender', '')
            #用户名是否被占用
            user = User.objects.filter(username=user.username)
            if user.count():
 
                #用户扩展信息   
                user.location = location 
                user.school = school 
                user.classname = classname 
                user.inschool_date = inschool_date
                user.study_id = ""
                user.role =  ""
                user.birthday = birthday
                user.gender = gender
                user.qq_number =  ""
                user.wechat_number =  ""
                user.phone_number = phone  
                user.bio =  ""
                user.personalized_signature =  ""
                user.picture =  ""
                user.nick_name = ""
                user.real_name = truename  

                user.provincename = request.session.get('logined_user_province','')
                user.usergroup = 'group_student' #默认以学生角色注册 
                user.creator = 'register'  
                user.save()  
                return render_to_response('index.html', RequestContext(request, {'form': None,'msg':'注册成功', }))          
        else:
            return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': '注册失败:请完整填写信息',}))      



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

