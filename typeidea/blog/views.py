'''
File Name: your project
Mail: 1.0
Author: LH
Created Time: Do not edit
'''
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from silk.profiling.profiler import silk_profile

from config.models import SideBar

from .models import Category, Post, Tag


class CommonViewMixin:
    @silk_profile(name='get_context_data')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()  # The data source
    paginate_by = 5 # How much data to show on one page
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)
    

class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()  # The data source
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context
    
    # Control data source
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # Q is a conditional expression
        # Note that there are two underscores for fuzzy matching
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
