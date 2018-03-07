#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import random

def random_code():
    code = ""
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90)) #参数是[0,255]的一个整数，返回值是当前整数对应的ascii字符。
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code


def generate_md5(value):
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


if __name__ == '__main__':
    #r = random_code()
    r = generate_md5("abc")
    print(r)


