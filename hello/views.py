from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

#from .models import Choice,Question


    # https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.COOKIES
    # HttpResponse.set_cookie(key, value='', max_age=None, expires=None, path='/',
    #     domain=None, secure=None, httponly=False, samesite=None)
    # def cookie(request):
    #     print(request.COOKIES)
    #     oldval = request.COOKIES.get('zap', None)
    #     resp = HttpResponse('In a view - the zap cookie value is '+str(oldval))
    #     if oldval :
    #         resp.set_cookie('zap', int(oldval)+1) # No expired date = until browser close
    #     else :
    #         resp.set_cookie('zap', 42) # No expired date = until browser close
    #     resp.set_cookie('sakaicar', 42, max_age=1000) # seconds until expire
    #     return resp

def myview(request) :
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4 : del(request.session['num_visits'])
    resp = HttpResponse('view count='+str(num_visits))
    resp.set_cookie('dj4e_cookie', '38a647f5', max_age=1000)
    return resp
