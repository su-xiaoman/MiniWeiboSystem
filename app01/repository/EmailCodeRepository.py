#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import IEmailCodeRepository


class UserRepository(IEmailCodeRepository):
    def __init__(self):
        pass

    def fetch_code_by_email(self,email):
        pass



