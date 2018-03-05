#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

import collections


def build_tree(comment_list):
    comment_dic = collections.OrderedDict()#

    for comment_obj in comment_list:
        if comment_obj[2] is None:
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            tree_search(comment_dic, comment_obj)
    return comment_dic


def tree_search(d_dic, comment_obj):
    """
    @todo:
    :param d_dic:
    :param comment_obj:
    :return:
    """
    #在comment_dic中一个一个地寻找其回复的评论
    #检查当前评论的reply_id和comment_dic中已有的nid是否相同，
    #   如果相同，表示就是回复的此信息
    #   如果不同，则需要去comment_dic的所有子元素中寻找，一直找，如果一系列中示找到，则继续向下找

    for key, value_dic in d_dic.items():
        if key[0] == comment_obj[2]:
            d_dic[key][comment_obj] = collections.OrderedDict()
            return
        else:
            tree_search(d_dic[key], comment_obj)

if __name__ == '__main__':
    comment_list = [
        (1,"1",None),
        (2, "2", None),
        (3, "3", 2),
        (4, "4", None),
        (5, "5", 2),
        (6, "6", 1),
    ]
    print(build_tree(comment_list),type(build_tree(comment_list)))