# -*- coding=utf-8 -*-

from django.db import models
# import datetime

# Create your models here.

# 接口
class IUserProfileRepository:
    """
    定义用户的仓库接口,用来获取与用户相关的信息
    """
    def set_login_imgcode_by_username(self, username,code):
        """

        :return:
        """
    def fetch_one_by_user_pwd(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        raise Exception('此接口必须被实现')

    def fetch_one_by_email_pwd(self, email, password):
        """

        :param email:
        :param password:
        :return:
        """
        raise Exception('此接口必须被实现')

    def get_userBasicInfo_by_username(self,username):
        """
        通过用户名去获取用户基本信息
        :param username:
        :return:
        """

    def get_myFocusNum_by_username(self,username):
        """

        :param username:
        :return:
        """

    def get_myFansNum_by_username(self, username):
        """

        :param username:
        :return:
        """

    def register_newUser_with_related_info(self,username,email,password,registration_date,user_type):
        """

        :return:
        """

class IEmailCodeRepository:
    """
    定义用户注册时的邮箱与验证码接口
    """
    def get_code_validity_by_email(self,email):
        """

        :param email:
        :return:
        """

    def find_theRegisteredEmail_by_email(self,email):
        """

        :param email:
        :return:
        """

    def find_theRegisteringEmail_by_email(self,email):
        """

        :param email:
        :return:
        """

    def update_VerifyCode_Validity_by_email(self,email,code,stime):
        """

        :param email:
        :return:
        """

    def update_my_register_status_by_email(self, email):
        """

        :param email:
        :return:
        """

    def generate_temporaryEmail_by_VerifyCode_Validity(self,email,code,stime):
        """

        :param email:
        :return:
        """

class ITopicRepository:
    """
    定义话题相关的接口
    """
    def get_most_read_topic(self):
        """

        :return:
        """

class IWeiboRepository:
    """
    定义与微博表相关的数据访问
    """
    def get_weiboNum_by_username(self,username):
        """

        :param username:
        :return:
        """
    def get_releted_info_by_wbType_Public(self):
        """

        :return:
        """
    def set_one_weibo_with_info(self,*args,**kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

class ICommentRepository:
    def get_all_comments_by_weiboId(self,id):
        """

        :return:
        """
    def set_one_comment_with_info(self,*args,**kwargs):
        # date id comment_type comment p_comment_id to_weibo_id user_id
        """

        :param id:
        :return:
        """

class ITagsRepository:
    pass

class ICategoryRepository:
    pass



# 领域模型
class EmailCode(models.Model):
    login_status = (
        (0, "未成功"),
        (1, "已成功"),

    )
    email = models.EmailField(verbose_name="邮箱", unique=True)
    code = models.CharField(verbose_name="验证码", max_length=4)
    stime = models.DateTimeField(verbose_name="生效时间", auto_now=True)
    status = models.IntegerField(verbose_name="注册状态", choices=login_status, default=0)

    class Meta:
        db_table = "EmailCode"
        verbose_name_plural = "临时邮箱验证码"

class Weibo(models.Model):
    '''所有微博'''
    wb_type_choices = (
        (0, '发布'),
        (1, '转发'),
        (2, '收藏'),
    )
    wb_type = models.IntegerField(verbose_name="微博类型", choices=wb_type_choices, default=0)
    forward_or_collect_from = models.ForeignKey('self',
                                                related_name="forward_or_collects",
                                                blank=True,
                                                null=True,
                                                on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    text = models.CharField("微博内容", max_length=140)
    pictures_link_id = models.CharField(verbose_name="图片连接id", max_length=128, blank=True, null=True)
    video_link_id = models.CharField(verbose_name="视频链接id", max_length=128, blank=True, null=True)
    perm_choice = (
        (0, '公开'),
        (1, '仅自己可见'),
        (2, '好友圈'),
    )
    perm = models.IntegerField(verbose_name="微博权限", choices=perm_choice, default=0)
    date = models.DateTimeField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "Weibo"
        verbose_name_plural = "微博表"

    def __str__(self):
        return self.text

class Topic(models.Model):
    '''话题'''
    name = models.CharField(verbose_name="话题名称", max_length=140)
    readers = models.IntegerField(verbose_name="阅读数量", default=1)
    date = models.DateTimeField()

    class Meta:
        db_table = "Topic"
        verbose_name_plural = "话题"

    def __str__(self):
        return self.name

class Category(models.Model):
    '''微博分类'''
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "Category"
        verbose_name_plural = "微博分类"

    def __str__(self):
        return self.name

class Comment(models.Model):
    '''评论'''
    to_weibo = models.ForeignKey(Weibo, verbose_name="评论的微博", on_delete=models.CASCADE)
    p_comment = models.ForeignKey('self', null=True,blank=True,verbose_name="父级评论", related_name="child_comments", on_delete=models.CASCADE)
    user = models.ForeignKey('UserProfile', verbose_name="评论的人", on_delete=models.CASCADE)
    comment_type_choices = ((0, '评论'), (1, '点赞'))  # 将评论点赞 整合在同样一张表里
    comment_type = models.IntegerField(choices=comment_type_choices, default=0)
    comment = models.CharField(verbose_name="评论内容", max_length=140, blank=True, null=True)
    date = models.DateTimeField(verbose_name="评论日期",auto_created=True)

    class Meta:
        db_table = "Comment"
        verbose_name_plural = "评论表"

    def __str__(self):
        return self.comment

class Tags(models.Model):
    '''标签'''
    name = models.CharField(verbose_name="标签名", max_length=64, unique=True)

    class Meta:
        db_table = "Tags"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    '''用户信息'''

    user_type = (
        (1, "管理员"),
        (2, "普通用户"),
        (3, "VIP用户"),
    )

    user = models.IntegerField(verbose_name="用户类型", choices=user_type, default=2)

    username = models.CharField(verbose_name="用户名", max_length=64, unique=True)
    brief = models.CharField(verbose_name="个人简历", max_length=140, blank=True, null=True)

    sex_type = ((1, '男'), (0, '女'))
    sex = models.IntegerField(verbose_name="性别", choices=sex_type, default=1)
    age = models.PositiveSmallIntegerField(verbose_name="年龄", blank=True, null=True)
    email = models.EmailField(verbose_name="邮箱", unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)

    head_img = models.ImageField(verbose_name="头像", upload_to="./static/img/user_pic", blank=True, null=True)
    registration_date = models.DateTimeField(verbose_name="创建时间", auto_created=True)

    followed_list = models.ManyToManyField('self', verbose_name="我的关注", blank=True, related_name="my_fans",
                                           symmetrical=False)
    # login_img_code = models.CharField(verbose_name="登陆验证码",max_length=4,null=True)
    # followers = models.ManyToManyField('self',verbose_name="我的关注",blank=True,null=True,related_name="my_watch",symmetrical=False

    class Meta:
        db_table = "UserProfile"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username


# 协调者
class UserService:
    def __init__(self, user_repository):
        self.userRepository = user_repository

    def check_login(self, username=None, email=None, password=None):
        if username:
            user_model = self.userRepository.fetch_one_by_user_pwd(username, password)
        else:
            user_model = self.userRepository.fetch_one_by_email_pwd(email, password)

        return user_model
