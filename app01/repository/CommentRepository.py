#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import ICommentRepository
from app01 import models
from django.db.models import Count


class CommentRepository(ICommentRepository):

    def __init__(self):
        pass

    def get_all_comments_by_weiboId(self,weibo_id):

        obj = models.Comment.objects.filter(to_weibo_id=weibo_id).values("id",
                                                                        "comment",
                                                                        "p_comment_id",
                                                                        "p_comment__user_id",
                                                                        "p_comment__user__username",
                                                                        "to_weibo_id",#none表示是根评论,对象的id
                                                                        "user__username",
                                                                        "user__head_img",
                                                                        "date",
                                                                        "comment_type",
                                                                        ).order_by("-date")
        return obj
    def set_one_comment_with_info(self,*args,**kwargs):
        # date id comment_type comment p_comment_id to_weibo_id user_id
        if models.Comment.objects.create(**kwargs):
            return True
        else:
            return False

    def get_likeInfo_by_weiboId(self,weibo_id,username):
        likeStatus = models.Comment.objects.filter(user__username=username,to_weibo_id=weibo_id,#
                                                ).aggregate(likeStatus=Count('comment_type'))
        #返回用户点赞的状态
        #一个用户当然可以多次评论，并且生成总的值
        return likeStatus

    def changeLikeStatus_with_info(self, LikeStatus, Username):
        print("来自数据库的凝视",LikeStatus)

        if(LikeStatus==0):
            models.Comment.objects.filter(user__username=Username).update(comment_type=1)
        else:
            models.Comment.objects.filter(user__username=Username).update(comment_type=0)