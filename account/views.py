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
#组成一个json样式的字符串，包含所有单位的id和名称，样例如下：
#[{"ID":"1","NAME":"北京","ITEMS":[{"ID":"1","NAME":"北京市","ITEMS":[{"ID":"1","NAME":"南城区","ITEMS":[{"ID":"1","NAME":"第1中学","ITEMS":[{"ID":"1","NAME":"初一（1）班"},{"ID":"2","NAME":"初一（2）班"}]},{"ID":"2","NAME":"第2中学","ITEMS":[{"ID":"3","NAME":"初一（2）班"},{"ID":"4","NAME":"初一（2）班1"}]}]}]}]},{"ID":"2","NAME":"上海","ITEMS":[{"ID":"2","NAME":"上海市","ITEMS":[{"ID":"2","NAME":"黄浦区","ITEMS":[{"ID":"3","NAME":"第2中学","ITEMS":[{"ID":"5","NAME":"初一（2）班"},{"ID":"6","NAME":"初一（1）班"}]},{"ID":"4","NAME":"第1中学","ITEMS":[{"ID":"7","NAME":"初一（1）班"},{"ID":"8","NAME":"初一（2）班"}]}]}]}]}]
#命名为proStr的字符变量，传到前端，前端解析为json
def make_proStr():
    items_str = '['   
    for obj in Province.objects.all():
        id_str = str(obj.id)
        name_str = str(obj.province_name)
        items_str += '{"ID":"'+ id_str +'","NAME":"'+ name_str +'","ITEMS":[' + make_cityStr(str(obj.id)) + ']},'
    items_str = items_str[:-1]
    items_str = items_str + ']'
    return items_str
def make_cityStr(province_id):
    items_str = ''   
    for obj in City.objects.filter(province_foreign_id=province_id):
        id_str = str(obj.id)
        name_str = str(obj.city_name)
        items_str += '{"ID":"'+ id_str +'","NAME":"'+ name_str +'","ITEMS":[' + make_disStr(str(obj.id)) + ']},'
    items_str = items_str[:-1]
    return items_str
def make_disStr(city_id):
    items_str = ''   
    for obj in District.objects.filter(city_foreign_id=city_id):
        id_str = str(obj.id)
        name_str = str(obj.district_name)
        items_str += '{"ID":"'+ id_str +'","NAME":"'+ name_str +'","ITEMS":[' + make_schStr(str(obj.id)) + ']},'
    items_str = items_str[:-1]
    return items_str
def make_schStr(dis_id):
    items_str = ''   
    for obj in School.objects.filter(district_foreign_id=dis_id):
        id_str = str(obj.id)
        name_str = str(obj.school_name)
        items_str += '{"ID":"'+ id_str +'","NAME":"'+ name_str +'","ITEMS":[' + make_claStr(str(obj.id)) + ']},'
    items_str = items_str[:-1]
    return items_str
def make_claStr(sch_id):
    items_str = ''   
    for obj in Class.objects.filter(school_foreign_id=sch_id):
        id_str = str(obj.id)
        name_str = str(obj.class_name)
        items_str += '{"ID":"'+ id_str +'","NAME":"'+ name_str +'"},'
    items_str = items_str[:-1]
    return items_str


@permission_required('user.is_staff')
def add_school(request):
    provinces_recent = Province.objects.all().order_by('province_name','-create_time')
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
    pros_before = make_proStr()
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
        #生成js文件，包含所有单位名称proStr     
        pros_after = "var proStr= '" + make_proStr()+"'"
        f2 = open('account/static/js/jquery-1.9.9.js','wb')#打开一个文件，用于写入，后面的'wb'表示每次写入前格式化文本，如果此文件不存在，则创建一个此文件名的文件
        f2.write(pros_after.encode(' utf-8 '))#字符串写入需要编码，https://blog.csdn.net/u014453898/article/details/53537118
        f2.close()#执行完毕关闭文件
    return render(request, 'account/add_school.html',{'msg': msg,'form1': province_form,'form2': city_form,'form3': district_form,'form4': school_form,'form5': class_form,
                    'province': provinces_recent,'city': citys_recent,'district': districts_recent,'school': schools_recent,'class': classes_recent,
                    'pros_str':pros_before,})
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




#注册第一步，选择学校
def select_school3(request):
    #pros_json = serializers.serialize("json",sheng)
    return render(request,'account/select_school3.html', {})

#弹出注册第二步页面，填写个人信息
def confirm_school(request):
    if request.method == 'POST':
        regform = RegisterForm()
        #<!--  此处的input一定要有name ，因为后台获取数据要靠name而不是id-->
        #<!--  name和id的区别：多数情况用id；个别情况用name。参考 https://blog.csdn.net/qq_35038153/article/details/70215356 -->
        sheng = request.POST.get('pro', '').strip()
        shi = request.POST.get('cit', '').strip()
        qu = request.POST.get('dis', '').strip()
        xiao = request.POST.get('sch', '').strip()
        ban = request.POST.get('cla', '').strip() 
        msg = ''
        reg_code = request.POST.get('regCode', '').strip() 
        if reg_code == '':
            msg = '您输入的注册码为空！请重新输入。'
        return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg':msg,'sheng': sheng,'shi': shi,'qu': qu,'xiao': xiao,'ban': ban,})) 


#对注册信息进行验证
def register(request):
    #已经提交数据
    if request.method == 'POST':
        if 'pro' in request.POST:
            sheng = request.POST['pro']
            shi = request.POST['cit']
            qu = request.POST['dis']
            xiao = request.POST['sch']
            ban = request.POST['cla'] 
            regform = RegisterForm(request.POST)
            if regform.is_valid():
                location = sheng + '-' + shi + '-' + qu 
                school_name = xiao
                school = get_object_or_404(School,location=location,school_name=school_name)
                classname = ban
                #inschool_date = request.POST.get('gradename', '')
                username = request.POST.get('username', '')
                password1 = request.POST.get('password1', '')
                password2 = request.POST.get('password2', '')
                email = ''
                '''
                #用户名是否被占用
                user = User.objects.filter(username=username)
                if user.count():
                    return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': '用户名已存在','sheng': sheng,'shi': shi,'qu': qu,'xiao': xiao,'ban': ban,}))
                '''
                #注册成功
                user = User.objects.create_user( username, email, password1 )
                #用户扩展信息   
                user.location = location + '-' + xiao+ '-' + ban
                user.school = school
                user.classname = classname
                #user.inschool_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%I:%S') #'' value has an invalid date format. It must be in YYYY-MM-DD format.
                user.save()

                #自动登录
                user = auth.authenticate(username=username, password=password1)#登录前需要先验证  
                if user is not None and user.is_active:
                    auth.login(request, user) 
                    return render_to_response('index.html', RequestContext(request, {'msg':'注册成功', }))          
            else:
                return render_to_response('account/register.html', RequestContext(request, {'form': regform,'msg': '注册失败','sheng': sheng,'shi': shi,'qu': qu,'xiao': xiao,'ban': ban,}))    
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

