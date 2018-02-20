from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q
from django.db.models import Count
from app01 import models
from app01.infrastructure import messages, commons
# from app01.forms import RegisterForm

import json
import datetime


# Create your views here.
@csrf_exempt
def page_not_found(request):
    return render(request, "404.html")


@csrf_exempt
def page_error(request):
    return render(request, "500.html")


@csrf_exempt
def permission_denied(request):
    return render(request, '403.html')


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

    return render(request, "index.html", {"detail_list": detail_list,
                                          "user_list": user_list,
                                          "weibo_num": weibo_num,
                                          "follows": follows,
                                          "fans_num": fans_num,
                                          "topic_info": topic_info, })


def homepage(request):
    return HttpResponse('i am homepage!')


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

        return render(request, "myHomepage.html", {"ret_str": ret_str})

    return HttpResponse("error page!")


@csrf_exempt
def register(request):
    ret_dict = {'status': True, 'data': "", 'error': ""}
    if request.method == "POST":
        """
        username = request.POST.get('username',None)
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)

        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors,type(form.errors))
            #错误信息是一个ul>li的方式展现。

        return HttpResponse("404")
        return render(request,"register.html",{'error':form.errors,'form':form})
        """

        reg_data = request.POST.get("reg_data")
        # print(reg_data, type(reg_data))
        reg_data = json.loads(reg_data)
        # json化的数据本质上是一个str，如果想要恢复成原有的如字典之类的，则需要用loads重新组成，
        # 同时使用form和ajax，会提交了两次

        username = reg_data['username']
        password = reg_data['password']
        email = reg_data['email']
        code = reg_data['email_code']

        print(username,password,email,code)


        #先判断验证码是否合法
        obj = models.EmailCode.objects.filter(email=email).values('code', 'stime')
        if obj:
            for item in obj:
                veri_code = item['code']
                send_veri_time = item['stime']

                if (datetime.datetime.now() - datetime.timedelta(seconds=60)) <= send_veri_time:
        #             print(datetime.datetime.now() - datetime.timedelta(seconds=60))
                    if veri_code.lower() == code.lower():#验证码(不区分大小写) 一致的情况下
                        models.UserProfile.objects.create(username=username,
                                                          email=email,
                                                          password=password,
                                                          registration_date=datetime.datetime.now(),
                                                          user=2, )
                        models.EmailCode.objects.filter(email=email).update(status=1)
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
        return render(request,"register.html",{"ret_dict":ret_dict, })


@csrf_exempt
def send_code(request):
    ret_dict = {'status': True, 'data': "", 'error': ""}

    if request.method == "POST":
        register_email = request.POST.get('email')#获取发送而来的邮箱数据
        # print("send_code_page!!")

        if register_email:#如果输入的邮箱有效(只能做简单的检验)
            if models.EmailCode.objects.filter(email=register_email,status=1):#里面是否有并且已经处于注册成功状态
                ret_dict['status'] = False
                ret_dict['error'] = "该邮箱已经被注册,请登陆!"
            else:
                code = commons.random_code()  # 产生验证码
                print("code:", code)
                messages.email(register_email, "感谢注册新浪微博，亲爱的用户，您的验证码为：" + code+",该验证码一分钟内有效")  # 发送验证码

                if models.EmailCode.objects.filter(email=register_email,status=0):#有但是没有注册成功
                    models.EmailCode.objects.filter(email=register_email).update(code=code,stime=datetime.datetime.now(),)
                else:
                    #create是无法实现将原有字符串重新写一遍的。
                    models.EmailCode.objects.create(email=register_email,code=code,stime=datetime.datetime.now(),)

            print(ret_dict,type(ret_dict))
            return HttpResponse(json.dumps(ret_dict))
            # return render(request, "register.html", {"ret_dict": ret_dict, })
        # else:
        #     return HttpResponse("Unknowed Error!")
    else:
        ret_dict['status'] = False
        ret_dict['error'] = "Unknowed Error!"
    return HttpResponse(json.dumps(ret_dict))


def messageShow(request):
    detail_list = models.Weibo.objects.filter(wb_type=0).values_list("user__username",
                                                                     "text",
                                                                     "date", ).order_by("date")
    print(detail_list, type(detail_list))
    return HttpResponse("hahahahhah")
