"""mindbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from account import views

urlpatterns = [
    #url(r'^login/$',views.login, name='login'),
    url(r'^add_school$', views.add_school, name='add_school'),#管理员添加学校页面
    url(r'^add$', views.add, name='add'),
    url(r'^select_school/$', views.select_school, name='select_school'),#显示ajax择校页面
    url(r'^sel_sch_ajax_check/$', views.select_school_ajax_check, name='select_school_ajax_check'),#显示ajax择校校验
    url(r'^register/$',views.register, name='register'),
    url(r'^fgtpwd/$',views.fgtpwd, name='fgtpwd'),
    url(r'^chgpwd/$',views.chgpwd, name='chgpwd'),
    url(r'^self/$',views.self_info, name='self'),
    url(r'^logout/$',views.logout, name='logout'),
]
