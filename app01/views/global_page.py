#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from django.db.models import Count

@csrf_exempt
def page_not_found(request):
    return render(request, "global_handler_page/404.html")


@csrf_exempt
def page_error(request):
    return render(request, "global_handler_page/500.html")


@csrf_exempt
def permission_denied(request):
    return render(request, 'global_handler_page/403.html')

def index(request):
    user = "root"
    detail_list = models.Weibo.objects.filter(wb_type=0).values("user__username",
                                                                "user__head_img",
                                                                "text",
                                                                "date", ).order_by("-date")
    user_list = models.UserProfile.objects.filter(username=user).values('head_img',
                                                                        'username', )
    weibo_num = models.Weibo.objects.filter(user__username=user).aggregate(weibo_num=Count('text'), )
    follows = models.UserProfile.objects.filter(username=user).aggregate(follows=Count('followed_list'), )

    # 用户通常只知道自己关注了谁，却不知道谁关注了自己,而这种反向查很明显存在这种问题,目前的解决方法就是这样
    obj = models.UserProfile.objects.get(username=user).my_fans.select_related()
    fans_num = len(obj)

    # --------------------------------------------------------------------------------------
    topic_info = models.Topic.objects.filter(readers__gte=1).values('name', 'readers').order_by('-readers')

    return render(request, "global_handler_page/index.html", {"detail_list": detail_list,
                                          "user_list": user_list,
                                          "weibo_num": weibo_num,
                                          "follows": follows,
                                          "fans_num": fans_num,
                                          "topic_info": topic_info, })