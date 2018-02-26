#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/19/2018"

from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        # error_messages={'required': '用户名不能为空',},
        widget=forms.TextInput(attrs={
            'class': "form-control",
            "placeholder": "Username"
        }),
    )

    email = forms.EmailField(
        required=True,
        # error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        widget=forms.EmailInput(attrs={
            'class': "form-control",
            'placeholder': "Email",
        }),
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=64,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "email",
        }),
    )
    veri_code = forms.CharField(
        required=True,
        # error_messages={'required': "请输入验证码", },
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Verification Code",
            'style': "width: 280px;margin-right: 4px;",
        }),
    )

