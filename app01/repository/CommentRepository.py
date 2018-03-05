#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import ICommentRepository
from app01 import models


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
