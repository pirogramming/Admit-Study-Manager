import functools

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render

# Create your views here.
from study.models import Membership

def group_required(func):
   """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

   @functools.wraps(func)
   def wrapper(request, group_name):
       # group_name = request.GET['group_name']
       group_name = group_name
       user = request.user
       usergroup_list = [x.group.group_name for x in Membership.objects.filter(person=user)]
       if request.user.is_authenticated and group_name not in usergroup_list:
           return HttpResponse("{}그룹 멤버가 아니므로 글을 쓸 수 없습니다.".format(group_name))

       return func(request, group_name)

   return wrapper

@group_required
def post(request, group_name):
    return HttpResponse("글을 쓸 수 있습니다.")
