#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/28/2018"

import json

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