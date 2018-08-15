#coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
 
class User(AbstractUser):
    SEX_CHOICES = {
        1: u'男',
        2: u'女',
    }
    ROLE_CHOICES = {
        1: u'学生',
        2: u'老师',
        3: u'班主任',
        4: u'年级主任',
        5: u'校领导',
        6: u'学校管理员',
        7: u'系统管理员',
    }
    location = models.CharField(u'所在地',max_length=30, blank=True)#所在地，省+地市+区县+乡镇或街道
    school_name = models.CharField(u'学校',max_length=30, blank=True)#学校
    class_name = models.CharField(u'班级名称',max_length=30, blank=True)#班级名称
    inschool_date = models.DateField(u'入学年份',blank=True, null=True)#入学年份
    student_id = models.CharField(u'学号',max_length=128, blank=True, null=True)#学号
    role = models.SmallIntegerField(u'角色',default=1, choices=ROLE_CHOICES.items())#角色
    birth_date = models.DateField(u'出生日期',null=True, blank=True)#出生日期
    sex = models.SmallIntegerField(u'性别',default=1, choices=SEX_CHOICES.items())#性别
    qq_number = models.CharField(u'QQ号码',max_length=128, blank=True, null=True)#QQ号码
    wechat_number = models.CharField(u'微信号码',max_length=128, blank=True, null=True)#微信号码
    phone_number = models.CharField(u'手机号码',max_length=128, blank=True, null=True)#手机号码
    bio = models.TextField(u'自我介绍',max_length=500, blank=True)#自我介绍
    personalized_signature = models.CharField(u'个性签名',max_length=128, blank=True, null=True)#个性签名
    picture = models.ImageField(u'头像',upload_to="image/", blank=True,null=True)#头像
    nick_name = models.CharField(u'昵称',max_length=128, blank=True, null=True)#昵称
    real_name = models.CharField(u'真实姓名',max_length=128, blank=True, null=True)#真实姓名
    login_times = models.SmallIntegerField(u'登录次数',blank=True, null=True)#登录次数
    already_toke = models.CharField(u'已经做过的测试',max_length=1280, blank=True, null=True)#已经做过的测试名称

    class Meta:  
        permissions = (
            ('can_view_student', u'可以查看学生'),  #到对象级别则分为可以查看：单个学生（自己）、全班学生（自己所在班）、全年级学生、全校学生
            ('can_view_teacher', u'可以查看教师'), 
            ('can_view_class', u'可以查看班主任'),
            ('can_view_admin', u'可以查看学校管理员'), 
        )

class School(models.Model):
    IF_CHARGED = {
        1: u'余额充足',
        2: u'欠费',
    }
    SCHOOL_STAGE = {
        1: u'幼儿园',
        2: u'小学',
        3: u'初中',
        4: u'高中',
        5: u'大学或其他',
    }
    location = models.CharField(u'所在地',max_length=30, blank=True)#所在地，省+地市+区县+乡镇或街道
    school_name = models.CharField(u'学校名称',max_length=30, blank=True)#学校名称
    school_stage = models.SmallIntegerField(u'昵称',default=5, choices=SCHOOL_STAGE.items())#学校阶段
    class_name = models.CharField(u'班级名称',max_length=30, blank=True)#班级名称
    school_code = models.CharField(u'学校代码',max_length=30, blank=True)#学校代码
    available_time = models.DateField(u'有效截至时间',blank=True, null=True)#有效截至时间
    student_id = models.CharField(u'所有学生id号',max_length=128, blank=True, null=True)#所有学生id号
    teacher_id = models.CharField(u'所有老师id号',max_length=128, blank=True, null=True)#所有老师id号
    admin = models.ForeignKey(User,verbose_name=u'管理员', null=True, blank=True, related_name='school_admins')#管理员
    student_count = models.SmallIntegerField(u'学生数量',blank=True, null=True)#学生数量
    teacher_count = models.SmallIntegerField(u'教师数量',blank=True, null=True)#教师数量
    can_take = models.CharField(u'可以使用的测试名称',max_length=1280, blank=True, null=True)#可以使用的测试名称
    if_charged = models.SmallIntegerField(u'昵称',default=1, choices=IF_CHARGED.items())#学校是否欠费
    creater = models.ForeignKey(User,verbose_name=u'创建者', null=True, blank=True, related_name='school_creater')#创建者
    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)#创建时间；auto_now_add=True，字段在实例第一次保存的时候会保存当前时间，不管你在这里是否对其赋值。但是之后的save()是可以手动赋值的。
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)#更新时间；auto_now=Ture，字段保存时会自动保存当前时间，但要注意每次对其实例执行save()的时候都会将当前时间保存，也就是不能再手动给它存非当前时间的值。

    def __unicode__(self):
        return self.school_name

    class Meta:  
        permissions = (
            ('can_view_all_school', u'查看所有学校'), 
        )

'''
class Province(models.Model):
    province_name = models.CharField(u'省份名称',max_length=30, blank=True)#省份名称
    creater = models.ForeignKey(User,u'创建者', null=True, blank=True, related_name='province_creater')#创建者
    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)#创建时间
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)#更新时间

    def __unicode__(self):
        return self.province_name

    class Meta:  
        permissions = (
            ('can_view_all_province', u'查看所有省份'), 
        )
class City(models.Model):
    city_name = models.CharField(u'地市名称',max_length=30, blank=True)#地市名称
    creater = models.ForeignKey(User,u'创建者', null=True, blank=True, related_name='city_creater')#创建者
    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)#创建时间
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)#更新时间

    def __unicode__(self):
        return self.city_name

    class Meta:  
        permissions = (
            ('can_view_all_city', u'查看所有地市'), 
        )
class District(models.Model):
    district_name = models.CharField(u'区县名称',max_length=30, blank=True)#区县名称
    creater = models.ForeignKey(User,u'创建者', null=True, blank=True, related_name='district_creater')#创建者
    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)#创建时间
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)#更新时间

    def __unicode__(self):
        return self.district_name

    class Meta:  
        permissions = (
            ('can_view_all_district', u'查看所有区县'), 
        )
class Town(models.Model):
    town_name = models.CharField(u'乡镇街道名称',max_length=30, blank=True)#乡镇街道名称
    creater = models.ForeignKey(User,u'创建者', null=True, blank=True, related_name='town_creater')#创建者
    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)#创建时间
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)#更新时间

    def __unicode__(self):
        return self.town_name

    class Meta:  
        permissions = (
            ('can_view_all_town', u'查看所有乡镇街道'), 
        )
'''
