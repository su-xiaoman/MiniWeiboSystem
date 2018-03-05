#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app01.repository.TopicRepository import TopicRepository
from app01.repository.WeiboRepository import WeiboRepository
from app01.repository.UserProfileRepository import UserProfileRepository

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
    username = "root"

    detail_list = WeiboRepository().get_releted_info_by_wbType_Public()

    user_list = UserProfileRepository().get_userBasicInfo_by_username(username=username)

    weibo_num = WeiboRepository().get_weiboNum_by_username(username=username)

    follows_num = UserProfileRepository().get_myFocusNum_by_username(username=username)

    fans_num = UserProfileRepository().get_myFansNum_by_username(username=username)

    topic_info = TopicRepository().get_most_read_topic()

    return render(request, "global_handler_page/index.html", {"detail_list": detail_list,
                                                              "user_list": user_list,
                                                              "weibo_num": weibo_num,
                                                              "follows": follows_num,
                                                              "fans_num": fans_num,
                                                              "topic_info": topic_info,})