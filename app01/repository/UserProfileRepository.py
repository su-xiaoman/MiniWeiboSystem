#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/24/2018"

from app01.models import IUserProfileRepository

class UserRepository(IUserProfileRepository):
    def __init__(self):
        pass

    def fetch_one_by_user_pwd(self,username,password):
        pass

    def fetch_one_by_email_pwd(self,email,password):
        pass

