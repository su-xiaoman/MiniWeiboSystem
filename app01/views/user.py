#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.infrastructure.utilities import check_code, commons, messages
from app01.repository.EmailCodeRepository import EmailCodeRepository
from app01.repository.UserProfileRepository import UserProfileRepository
from app01.repository.CommentRepository import CommentRepository
from app01.infrastructure.utilities.time_for_json import JsonCustomEncoder
import io
import json
import datetime

"""
from app01.repository.WeiboRepository import WeiboRepository
from app01.infrastructure.utilities import build_comment_tree
from django.core import serializers
"""

@csrf_exempt
def login(request):
    if request.method == "POST":
        ret = {'status': False, 'message': '', 'data': None, }
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            result = models.UserProfile.objects.filter(username=username, password=password).values('username', 'email',
                                                                                                    'password')
            if result:
                # result = models.UserProfile.objects.filter(condition).values('username', 'email', 'password')
                #  内部元素字典化
                li = list(result)
                # print(result,type(result))
                ret['status'] = True
                ret['data'] = li
                ret['message'] = "Welcome!"
            else:
                return HttpResponse("该用户不存在或者信息错误！")
        except Exception as e:
            ret['message'] = str(e)
        ret_str = json.dumps(ret)

        return render(request, "others_page/myHomepage.html", {"ret_str": ret_str})

    else:
        return render(request, "user_handler_page/login.html")


@csrf_exempt
def register(request):
    ret_dict = {'status': True, 'data': "", 'error': ""}
    if request.method == "POST":
        """
        邮箱部分的检验可以识别，已经注册过的，正在注册没有成功的，完全没有注册过的
        """
        reg_data = request.POST.get("reg_data")
        # print(reg_data, type(reg_data))
        reg_data = json.loads(reg_data)
        # json化的数据本质上是一个str，如果想要恢复成原有的如字典之类的，则需要用loads重新组成，
        # 同时使用form和ajax，会提交两次
        username = reg_data['username']
        email = reg_data['email']
        password = reg_data['password']
        code = reg_data['email_code']

        print(username,password,email,code)

        #先判断验证码是否合法
        obj = EmailCodeRepository().get_code_validity_by_email(email)
        if obj:
            for item in obj:
                veri_code = item['code']
                validity = item['stime']

                if (datetime.datetime.now() - datetime.timedelta(seconds=60)) <= validity:
                    #如果在有效期之内
                    if veri_code.lower() == code.lower():#验证码(不区分大小写) 一致的情况下
                        UserProfileRepository().register_newUser_with_related_info(username,email,password,datetime.datetime.now(),2)
                        EmailCodeRepository().update_my_register_status_by_email(email=email)
                        messages.email(email, "你已成功注册微博,马上进入。+link")
                    else:
                        ret_dict['status'] = False
                        ret_dict['error'] = "邮箱验证码错误"
                    return HttpResponse(json.dumps(ret_dict))
                else:
                    ret_dict['status'] = False
                    ret_dict['error'] = "验证码已经过期,请重新发送!"
        return HttpResponse(json.dumps(ret_dict))

    else:
        return render(request, "user_handler_page/register.html")


@csrf_exempt
def send_code(request):
    ret_dict = {'status': True, 'data': "", 'error': ""}

    if request.method == "POST":
        register_email = request.POST.get('email')#获取发送而来的邮箱数据

        if register_email:#如果输入的邮箱有效(只能做简单的检验)
            if EmailCodeRepository().find_theRegisteredEmail_by_email(register_email):#里面是否有并且已经处于注册成功状态
                ret_dict['status'] = False
                ret_dict['error'] = "该邮箱已经被注册,请登陆!"
            else:
                code = commons.random_code()  # 产生验证码
                print("code:", code)
                messages.email(register_email, "感谢注册新浪微博，亲爱的用户，您的验证码为：" + code + ",该验证码一分钟内有效")  # 发送验证码

                if EmailCodeRepository().find_theRegisteringEmail_by_email(register_email):#有但是没有注册成功
                    EmailCodeRepository().update_VerifyCode_Validity_by_email(register_email,code,datetime.datetime.now())

                else: #create是无法实现将原有字符串重新写一遍的。
                    EmailCodeRepository().generate_temporaryEmail_by_VerifyCode_Validity(register_email,code,datetime.datetime.now())

            print(ret_dict,type(ret_dict))
            return HttpResponse(json.dumps(ret_dict))

    else:
        ret_dict['status'] = False
        ret_dict['error'] = "Unknowed Error!"
    return HttpResponse(json.dumps(ret_dict))


def check_img_code(request):
    # if request.method == "POST":
    mstream = io.BytesIO()
    img, code = check_code.create_validate_code()
    img.save(mstream, "GIF")

    return HttpResponse(mstream.getvalue())


@csrf_exempt
def signup(request):
    return render(request, "user_handler_page/signup.html")

@csrf_exempt
def comment(request):
    if request.method == "GET":#获取评论

        id = request.GET.get("nid")

        comment_info = CommentRepository().get_all_comments_by_weiboId(id)

        comment_info = list(comment_info)

        return HttpResponse(json.dumps(comment_info,cls=JsonCustomEncoder))


    else:
        comment_date = request.POST.get("comment_related_data")
        comment_related_data = json.loads(comment_date)

        date = datetime.datetime.now()
        comment_type = 0
        comment = comment_related_data['comment']
        user_id = comment_related_data['user_id']
        to_weibo_id = comment_related_data['to_weibo_id']
        p_comment_id = comment_related_data['p_comment_id']

        if CommentRepository().set_one_comment_with_info(date=date,
                                                      comment_type=comment_type,
                                                      comment=comment,
                                                      p_comment_id=p_comment_id,
                                                      to_weibo_id=to_weibo_id,
                                                      user_id=user_id):

            comment_info = CommentRepository().get_all_comments_by_weiboId(to_weibo_id)

            comment_info = list(comment_info)

            return HttpResponse(json.dumps(comment_info, cls=JsonCustomEncoder))

        else:
            return HttpResponse("false")


def user_profile(request):
    return render(request,"user_handler_page/user_profile.html")