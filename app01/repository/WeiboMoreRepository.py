#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "3/17/2018"

from app01 import models
from app01.models import IWeiboMoreRepository

class WeiboMoreRepository(IWeiboMoreRepository):
    def __init__(self):
        pass

    def upload_weiboIMG_by_weibo_id(self,weibo_id,img_path):
        if models.WeiboMore.objects.create(picture_link_id=weibo_id,
                                        picture_content=img_path):
            return True
        else:
            return False

    #此功能已经被修正
    def get_weibo_info_with_public(self):
        detail_list = models.WeiboMore.objects.filter(picture_link__wb_type=0).values("picture_link__text",
                                                                                      "picture_link_id",
                                                                                      "picture_link__user__username",
                                                                                      "picture_link__user__head_img",
                                                                                      "picture_link__date",
                                                                                      "picture_content").order_by("-picture_link__date")
        return detail_list


    def get_weiboPhoto(self):
        photo_list = models.WeiboMore.objects.all().values("picture_content",
                                                           "picture_link_id")
        return photo_list