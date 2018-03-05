#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "3/1/2018"

import json
from datetime import date
from datetime import datetime
from decimal import Decimal


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        elif isinstance(field,Decimal):
            return str(field)
        else:
            return json.JSONEncoder.default(self, field)

if __name__ == '__main__':

    obj = {'d':datetime.now(),'e':Decimal(12)}
    ds = json.dumps(obj, cls=JsonCustomEncoder)
