#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import IEmailCodeRepository
from app01 import models

class EmailCodeRepository(IEmailCodeRepository):
    def __init__(self):
        pass

    def get_code_validity_by_email(self,email):
        obj = models.EmailCode.objects.filter(email=email).values('code', 'stime','status')
        return obj

    def find_theRegisteredEmail_by_email(self,email):
        if models.EmailCode.objects.filter(email=email, status=1):
            return True
        else:
            return False

    def find_theRegisteringEmail_by_email(self,email):
        if models.EmailCode.objects.filter(email=email, status=0):
            return True
        else:
            return False

    def update_VerifyCode_Validity_by_email(self,email,code,stime):

        models.EmailCode.objects.filter(email=email).update(code=code, stime=stime,)

    def update_my_register_status_by_email(self,email):
        models.EmailCode.objects.filter(email=email).update(status=1)

    def generate_temporaryEmail_by_VerifyCode_Validity(self,email,code,stime):

        models.EmailCode.objects.create(email=email, code=code, stime=stime, )




