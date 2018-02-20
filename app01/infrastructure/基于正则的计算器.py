#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "minyi"
__time__ = "2018/2/2"

import re
"""
目前还不完美的bug:
1.由于浮点数的问题，目前还不支持除法？？
2.关于正则匹配的浮点数问题？？
3.关于职能化的问题，实际上并没有真正地按照分离括号，计算乘除，计算加减的方式去做？？

# ret = re.search('\d+\.?\d*','12.5')#用来匹配一个浮点数

"""

def calculate(ex):
    """
    @todo :how to calculate the expression without bracket
    #分离出来1+5*6之类的表达式
    #由于这里的表达式是没有括号的，因此需要把所有的先把所有的乘除全部提取出来
    #事实上这个已经可以提取出来所有的乘除运算
    :param ex:
    :return:
    """
    print(ex)
    while True:
        ret = re.split(r'(\d+[*/]\d+)',ex,maxsplit=1)
        print("-----------------------")
        if len(ret) == 3:
            ret1 = arithmetic(ret[1])
            new_exp = ret[0]+str(ret1)+ret[2]
            ex = new_exp
        else:
            break
    result = ex
    print(result)
    while True:
        ret = re.split(r'(\d+[+-]\d+)',result,maxsplit=1)
        print("-----------------------")
        if len(ret) == 3:
            ret1 = arithmetic(ret[1])
            new_exp = ret[0]+str(ret1)+ret[2]
            result = new_exp
        else:
            break
    print(result)
    return result

def arithmetic(ex):
    """
    @todo :计算基本的加减乘除
    :param ex:
    :return:
    """
    result = 0
    ret = re.split(r'([*/+-])',ex,maxsplit=1)
    if len(ret) == 3:
        #print(ret)
        left,op,right = ret
        print(left,op,right)
        if op == "*":
            result = int(left) * int(right)
        elif op == "/":
            result = int(left) / int(right)
        elif op == "+":
            result = int(left) + int(right)
        elif op == "-":
            result = int(left) - int(right)
        else:
            print('op表达式错误，请重新输入！')
        print(result)
        return result
    else:
        print("op表达式错误，请重新输入！")

def splitBracket(expression):
    print(expression)
    while True:
        ret = re.split(r"\(([^()]+)\)", expression, maxsplit=1)
        if len(ret) == 3:
            before,content,after = ret#一种新的方法当ret是确定的值的时候
            # print(before,content,after)
            r = calculate(content)
            new_exp = before + str(r) + after
            # print(new_exp)
            expression = new_exp
        else:
            final = calculate(expression)
            final = arithmetic(final)
            return final

if __name__ == '__main__':
    # expression = "1 + 6*(9*5+4*3+6*7)*7*(8*6+1*2)"

    # expression = input(">>>")
    expression = "1+3*4-3*(9-4*2+8)"
    result = splitBracket(expression)
    print(result)