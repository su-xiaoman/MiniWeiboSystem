#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from app01.models import IUserProfileRepository
from app01 import models
from django.db.models import Count

class UserProfileRepository(IUserProfileRepository):
    def __init__(self):
        pass

    def set_login_imgcode_by_username(self, username,code):
        models.UserProfile.objects.filter(username=username).update(login_img_code=code)

    def fetch_one_by_user_pwd(self,username,password):
        pass

    def fetch_one_by_email_pwd(self,email,password):
        pass

    def get_userBasicInfo_by_username(self,username):

        user_list = models.UserProfile.objects.filter(username=username).values('id',
                                                                            'head_img',
                                                                            'username',
                                                                            'sex',
                                                                            'brief',)
        return user_list


    def get_myFocusNum_by_username(self,username):
        follows_num = models.UserProfile.objects.filter(username=username).aggregate(follows=Count('followed_list'), )
        return follows_num


    def get_myFansNum_by_username(self,username):
        # 用户通常只知道自己关注了谁，却不知道谁关注了自己,而这种反向查很明显存在这种问题,目前的解决方法就是这样
        obj = models.UserProfile.objects.get(username=username).my_fans.select_related()
        return len(obj)


    def register_newUser_with_related_info(self,username,email,password,registration_date,user_type):
        models.UserProfile.objects.create(username=username,
                                          email=email,
                                          password=password,
                                          registration_date=registration_date,
                                          user=user_type, )

    def get_detail_person_info_by_username(self,username):
        personal_info = models.UserProfile.objects.filter(username=username).values("user",
                                                                                    "username",
                                                                                    "brief",
                                                                                    "sex",
                                                                                    "email",
                                                                                    "password",
                                                                                    "head_img",
                                                                                    "registration_date")
        return personal_info

    def change_person_info_by_username(self,username,brief,sex,password):

        if models.UserProfile.objects.filter(username=username).update(brief=brief,
                                                                    sex=sex,
                                                                    password=password):
            return True
        else:
            return False
    def change_person_headImg_by_username(self,username,head_img):
        if models.UserProfile.objects.filter(username=username).update(head_img=head_img):
            return True
        else:
            return False
