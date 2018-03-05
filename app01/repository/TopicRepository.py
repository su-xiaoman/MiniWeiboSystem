#!/usr/bin/env python
# -*- coding: utf-8 -*-
__time__ = "2/26/2018"

from app01.models import ITopicRepository
from app01 import models

class TopicRepository(ITopicRepository):
    def __init__(self):
        pass

    def get_most_read_topic(self):
        topic_info = models.Topic.objects.filter(readers__gte=1).values('name', 'readers').order_by('-readers')

        return topic_info

if __name__ == '__main__':
    a = TopicRepository()
    a.get_most_read_topic()