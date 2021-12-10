'''
File Name: your project
Mail: 1.0
Author: LH
Created Time: Do not edit
'''
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link

# Create your views here.

class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'
