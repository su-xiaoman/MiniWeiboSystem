#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2018/2/5"

import CacheSession

class SessionFactory:
    __session = CacheSession()

    @staticmethod
    def get_session():
        return SessionFactory.__session

    @staticmethod
    def set_session(session):
        SessionFactory.__session = session