#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.infrastructure.utilities import check_code, commons, messages
from app01.repository.EmailCodeRepository import EmailCodeRepository
from app01.repository.UserProfileRepository import UserProfileRepository
from app01.repository.CommentRepository import CommentRepository
from app01.repository.WeiboRepository import WeiboRepository
from app01.repository.WeiboMoreRepository import WeiboMoreRepository
from app01.infrastructure.utilities.time_for_json import JsonCustomEncoder
import io
import os
import json
import datetime
import logging
#import pytz


"""
from app01.repository.WeiboRepository import WeiboRepository
from app01.infrastructure.utilities import build_comment_tree
from django.core import serializers
"""
def exit(request):
    request.session.clear()#['username'] = ""
    return HttpResponseRedirect("/signup/")

@csrf_exempt
def login(request):

    if request.method == "POST":
        ret = {'status': False, 'message': '', 'data': None, }
        try:
            login_data = request.POST.get("login_data")
            login_info = json.loads(login_data)

            username = login_info['username']
            password = login_info['password']
            email_code = login_info['email_code']

            print(username,password,email_code)

            check_img_code = request.session.get("check_img_code")

            print("check_img_code:",check_img_code)
            #首先判断验证码是否匹配，如果不匹配直接出局
            if check_img_code.lower() != email_code.lower():
                ret['message'] = "验证码错误，请重新输入"
                return HttpResponse(json.dumps(ret))
            else:
                #目前只去写使用用户名登陆，之后再去修改
                result = models.UserProfile.objects.filter(username=username, password=password).values('username',
                                                                                                        'email',
                                                                                                        'password')
                print("------------------------------")
                print(result,type(result))

                if result:
                    # 1、生成随机字符串（sessionID）
                    # 2、通过cookie发送给客户端
                    # 3、服务端保存{随机字符串:{'name':'zhanggen'.'email':'zhanggen@le.com'}}

                    for item in result:
                        email = item['email']
                        username = item['username']
                        password = item['password']

                    request.session['username'] = username
                    request.session['email'] = email
                    request.session['password'] = password
                    request.session['is_login'] = True

                    li = list(result)
                    ret['status'] = True
                    ret['data'] = li
                    ret['message'] = "Welcome!"

                    logging.basicConfig(
                        filename=os.path.join("static/log/", "%s_login.log" % username),
                        format='%(asctime)s-%(name)s-%(levelname)s-%(module)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        level=10,
                    )
                    logging.info("Using login function!")

                    return HttpResponse(json.dumps(ret))
                else:
                    ret['message'] = "用户名不存在或密码错误"
                    return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret['message'] = str(e)

        ret_str = json.dumps(ret)
        return render(request, "user_handler_page/signup.html", {"ret_str": ret_str})

    else:
        return render(request, "user_handler_page/signup.html")


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

        #先判断验证码是否合法，即此里面有没有相应的值
        obj = EmailCodeRepository().get_code_validity_by_email(email)
        if obj:
            for item in obj:
                veri_code = item['code']
                validity = item['stime']
                status = item['status']

            if status==1:#当已经注册成功的时候
                ret_dict['status'] = False
                ret_dict['error'] = "该邮箱已经被注册，请登陆"
                return HttpResponse(json.dumps(ret_dict))
            else:#当暂未注册成功或者根本没有注册过的时候
                if (datetime.datetime.now() - datetime.timedelta(seconds=60)) <= validity:
                    #如果在有效期之内
                    print(validity,type(validity))
                    print(type(datetime.datetime.now() - datetime.timedelta(seconds=60)))

                    if veri_code.lower() == code.lower():#验证码(不区分大小写) 一致的情况下
                        UserProfileRepository().register_newUser_with_related_info(username,email,password,datetime.datetime.now(),2)
                        EmailCodeRepository().update_my_register_status_by_email(email=email)
                        messages.email(email, "你已成功注册微博,马上进入。+link")
                        #设置session,以便于系统确定是谁在登陆
                        request.session['username'] = username
                        request.session['is_login'] = True

                        logging.basicConfig(
                            filename=os.path.join("static/log/", "%s_register.log" % username),
                            format='%(asctime)s-%(name)s-%(levelname)s-%(module)s:%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S %p',
                            level=10,
                        )
                        logging.info("Using register function!")
                    else:
                        ret_dict['status'] = False
                        ret_dict['error'] = "邮箱验证码错误"
                    return HttpResponse(json.dumps(ret_dict))
                else:#验证码已经过期
                    ret_dict['status'] = False
                    ret_dict['error'] = "验证码已经过期,请重新发送!"
        return HttpResponse(json.dumps(ret_dict))

    else:
        return render(request, "user_handler_page/signup.html")


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
    """
    1.生成验证码
    2.写入到session中
    3.制作成图片传入到前台（防止网站抓取）
    4.用户判断验证码并且 输入验证码（如果替换验证码则重新写入到session中）
    5.后台获取用户输入的验证码，并与session中的比较。一样通过，不一样返回错误信息
    """
    if request.method == "GET":
        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, "GIF")

        request.session["check_img_code"] = code
        print("code is:",code)

        return HttpResponse(mstream.getvalue())


@csrf_exempt
def signup(request):
    return render(request, "user_handler_page/signup.html")

@csrf_exempt
def like(request):
    if request.method == "GET":
        #获取微博的点赞状态需要哪些信息？
        #1.微博编号（点赞哪个微博）   2.哪个用户点赞的（因为这被认为是评论行为的一种）

        weibo_id = request.GET.get("weibo_id")
        username = request.session.get("username")
        print("weiboId:",weibo_id)
        print("username:",username)
        # #信息是可以成功获取到的

        likeStatus = CommentRepository().get_likeInfo_by_weiboId(weibo_id,username)
        #通过这种方式可以获取用户是否点赞

        print("likeStatus is:",likeStatus)

        return HttpResponse(json.dumps(likeStatus, cls=JsonCustomEncoder))

        #通过以上代码可以判断出某个用户是否已经点过赞


    else:
        if request.method == "POST":
            username = request.session.get("username")
            likeStatus = int(request.POST.get("status"))

            print(likeStatus,type(likeStatus))
            print(username,type(username))

            CommentRepository().changeLikeStatus_with_info(likeStatus,username)

            return HttpResponse("success")
        #通过给出需求从而将数据库数据按照相应的方法

@csrf_exempt
def comment(request):

    if request.method == "GET":#获取评论

        id = request.GET.get("nid")

        comment_info = CommentRepository().get_all_comments_by_weiboId(id)
        comment_info = list(comment_info)

        return HttpResponse(json.dumps(comment_info,cls=JsonCustomEncoder))


    else:#postComments
        #目前有一个bug，当评论的人是自己的时候，不能像评论其他人一样立刻刷新出来。

        # 记录着用户的评论过程，如次数等从而补充数据库等因为评论出错等问题引起的无法记录问题
        username = request.session.get("username")

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

@csrf_exempt
def delete(request):

    ret_dict = {'status': True, 'message': "", 'error': ""}
    if request.method == "POST":

        username = request.session.get("username")

        weibo_data = request.POST.get("weibo_data")
        weibo_data = json.loads(weibo_data)

        postMan = weibo_data['postMan']
        weiboId = weibo_data['weiboId']

        print(weiboId,postMan,username)#可以正确的打印
        #1.在数据库中删除掉，第二将相应信息提示出来
        if(postMan == username):
            if WeiboRepository().delete_an_item_by_id(weiboId):
                ret_dict['message'] = "微博删除成功"
            else:
                ret_dict['status'] = False
                ret_dict['error'] = "请检查网络问题或其它问题"
        else:
            ret_dict['status'] = False
            ret_dict['error'] = "无法完成删除，因为这并非你的微博"

        return HttpResponse(json.dumps(ret_dict))


@csrf_exempt
def post_weibo(request):
    if request.method == "POST":
        ret = {"status":False,"messages":None,"data":None}

        weibo_data = json.loads(request.POST.get("weibo_data"))
        text = weibo_data['text']
        user_id = weibo_data['user_id']
        wb_type = weibo_data['wb_type']
        permission = weibo_data['permission']

        print(text,user_id,wb_type,permission)

        #生成相关主键
        id = commons.generate_primaryKey()
        flag = True
        while flag:
            if WeiboRepository().judge_an_item_exists_by_id(id=id):
                id = commons.generate_primaryKey()
            else:
                flag = False

        if WeiboRepository().set_one_weibo_with_info(id=id,
                                                     date=datetime.datetime.now(),
                                                     text=text,
                                                     user_id=user_id,
                                                     wb_type=wb_type,
                                                     permission=permission,):
            ret['status'] = True
            ret['message'] = "微博创建成功"
            ret['data'] = {"id":id}
            return HttpResponse(json.dumps(ret))
        else:
            ret['message'] = "微博创建失败"
            return HttpResponse(json.dumps(ret))

@csrf_exempt
def user_profile(request):
    ret_dict = {'status': True, 'data': "", 'error': ""}
    if request.method == "GET":

        username = request.session['username']

        user_info = UserProfileRepository().get_userBasicInfo_by_username(username=username)
        follows_num = UserProfileRepository().get_myFocusNum_by_username(username=username)
        weibo_num = WeiboRepository().get_weiboNum_by_username(username=username)
        fans_num = UserProfileRepository().get_myFansNum_by_username(username=username)
        my_weibo = WeiboRepository().get_weibo_info_by_username(username=username)
        personal_info = UserProfileRepository().get_detail_person_info_by_username(username=username)


        return render(request,"user_handler_page/user_profile.html",{"user_info":user_info,
                                                                     "follows_num":follows_num,
                                                                     "weibo_num":weibo_num,
                                                                     "fans_num":fans_num,
                                                                     "my_weibo":my_weibo,
                                                                     "personal_info":personal_info})
    else:
        user_update_info = request.POST.get("user_update_info")
        user_update_info = json.loads(user_update_info)
        # print(user_update_info,type(user_update_info))
        #表明上面的数据已经通过某种方式从前台提交到后台了，接下来则进行数据库写入
        brief = user_update_info["brief"]
        sex = user_update_info["sex"]
        password = user_update_info["password"]
        # username = request.session.get["username"]
        username = request.session['username']
        if UserProfileRepository().change_person_info_by_username(username=username,
                                                               brief=brief,
                                                               sex=sex,
                                                               password=password):
            return HttpResponse(json.dumps(ret_dict))
        else:
            ret_dict['status'] = False
            ret_dict['error'] = "无法完成信息修改,请刷新重试"
            return HttpResponse(json.dumps(ret_dict))

@csrf_exempt
def upload_file(request):

    if request.method == 'POST':
        ret = {"status": False, "messages": None, "data": None}

        obj = request.FILES.get('head_img_change')
        filename = os.path.join("static/img/user_pic/", obj.name)
        username = request.session["username"]
        try:
            if UserProfileRepository().change_person_headImg_by_username(username=username,
                                                                  head_img=filename):
                print(filename)

                f = open(filename, 'wb')
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()

                ret['status'] = True
                ret['message'] = "上传成功"
            else:

                ret['message'] = "上传失败"
            return HttpResponse(json.dumps(ret))

        except Exception as e:
            ret['message'] = str(e)
            return HttpResponse(json.dumps(ret))

@csrf_exempt
def upload_weibo_img(request):
    if request.method == 'POST':
        ret = {"status": False, "messages": None, "data": None}

        pictures = request.FILES.get('weiboImg')
        weibo_id = request.POST.get("weibo_id")
        print(pictures.name,weibo_id)
        # return HttpResponse("ok");
        filename = os.path.join("static/img/user_pic/", pictures.name)

        try:
            if WeiboMoreRepository().upload_weiboIMG_by_weibo_id(weibo_id=weibo_id,
                                                                 img_path=filename):
                print(filename)

                f = open(filename, 'wb')
                for chunk in pictures.chunks():
                    f.write(chunk)
                f.close()

                ret['status'] = True
                ret['message'] = "上传成功"
            else:

                ret['message'] = "上传失败"
            return HttpResponse(json.dumps(ret))

        except Exception as e:
            ret['message'] = str(e)
            return HttpResponse(json.dumps(ret))


