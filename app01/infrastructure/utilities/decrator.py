#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/28/2018"

import json
from django.contrib.sessions.backends import db

"""
这里面有一个版本的session
1.是tornado版本的，不知道能不能用？？
2.参考django版本的，修改下面的代码并设置相关的sesssion,在登陆页面
request.session.clear_expired()
"""


def auth_login_redirect(func):
    def inner(self, *args, **kwargs):
        if not self.session["is_login"]:
            self.redirect(config.LOGIN_URL)
            return
        func(self, *args, **kwargs)
    return inner

def auth_login_json(func):
    def inner(self,*args,**kwargs):
        if not self.session['is_login']:
            rep = BaseResponse()
            rep.summary = "auth failed"
            self.write(json.dumps(rep.__dict__))
            return
        func(self,*args,**kwargs)
    return inner