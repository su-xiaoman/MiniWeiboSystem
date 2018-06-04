#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import IWeiboRepository
from app01 import models

from django.db.models import Count



class WeiboRepository(IWeiboRepository):
    def __init__(self):
        pass

    def get_weiboNum_by_username(self,username):
        weibo_num = models.Weibo.objects.filter(user__username=username).aggregate(weibo_num=Count('text'), )
        return weibo_num

    def get_releted_info_by_wbType_Public(self):
        detail_list = models.Weibo.objects.filter(wb_type=0).values("id",
                                                      "user__username",
                                                      "user__head_img",
                                                      "text",
                                                      "date",
                                                      ).order_by("-date")
        return detail_list

    def get_weibo_info_by_username(self,username):
        weibo_list = models.Weibo.objects.filter(user__username=username).values("id",
                                                      "user__username",
                                                      "user__head_img",
                                                      "text",
                                                      "date",
                                                      ).order_by("-date")
        return weibo_list

    def set_one_weibo_with_info(self,*args,**kwargs):
        if models.Weibo.objects.create(*args,**kwargs):
            return True
        else:
            return False

    def judge_an_item_exists_by_id(self,id):
        if models.Weibo.objects.filter(id=id):
            return True
        else:
            return False

    def delete_an_item_by_id(self,id):
        if models.Weibo.objects.filter(id=id).delete():
            return True
        else:
            return False