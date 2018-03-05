from django.shortcuts import render, HttpResponse
from app01 import models


# from app01.forms import RegisterForm


# Create your views here.





def homepage(request):
    return HttpResponse('i am homepage!')



def messageShow(request):
    detail_list = models.Weibo.objects.filter(wb_type=0).values_list("user__username",
                                                                     "text",
                                                                     "date", ).order_by("date")
    print(detail_list, type(detail_list))
    return HttpResponse("hahahahhah")