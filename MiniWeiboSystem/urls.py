"""MiniWeiboSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import global_page,user

from django.conf.urls import url
from django.views.generic.base import RedirectView

handler403 = global_page.permission_denied
handler404 = global_page.page_not_found
handler500 = global_page.page_error


urlpatterns = [
    # url(r'^$',global_page.index),

    url(r'^favicon.ico$',RedirectView.as_view(url='/static/img/about_UI/favicon.ico')),

    path('',global_page.index),
    path('admin/', admin.site.urls),
    path('index/',global_page.index),
    path('login/',user.login),
    path('register/',user.register),
    path('send_code/',user.send_code),
    path('check_img_code/',user.check_img_code),
    path('comment/',user.comment),
    path('signup/',user.signup),
    path('post_weibo/',user.post_weibo),
    path('user_profile/',user.user_profile),
    path('upload_file/',user.upload_file),
    path('upload_weibo_img/',user.upload_weibo_img),
    path('like/',user.like),
    path('exit/',user.exit),
    path('delete/',user.delete),




]
