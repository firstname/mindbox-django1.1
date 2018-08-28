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
    url(r'^list_school$', views.list_school, name='list_school'),#查看学校列表页面

    url(r'^select_school/$', views.select_school3, name='select_school'),#显示择校页面
    url(r'^confirm_school/$', views.confirm_school, name='confirm_school'),#显示择校页面
  
    url(r'^register/$',views.register, name='register'),
    url(r'^fgtpwd/$',views.fgtpwd, name='fgtpwd'),
    url(r'^chgpwd/$',views.chgpwd, name='chgpwd'),
    url(r'^self/$',views.self_info, name='self'),
    url(r'^logout/$',views.logout, name='logout'),
]
