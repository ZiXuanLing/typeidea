'''
File Name: your project
Mail: 1.0
Author: LH
Created Time: Do not edit
'''
from datetime import date

from django.core.cache import cache

from django.http import request
from django.shortcuts import redirect
from django.views.generic import TemplateView

from comment.forms import CommentForm
from comment.models import Comment
from blog.views import CommonViewMixin, DetailView
from blog.models import Post

from django.db.models import Q, F

# Create your views here.
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # def get(self, request, *args, **kwargs):
    #     resposne = super().get(request, *args, **kwargs)
    #     Post.objects.filter(pk=self.objects.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
    
    def get(self, request, *args, **kwargs):
        resposne = super().get(request, *args, **kwargs)
        self.handle_visited()
        return resposne

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60) # 1分钟有效
        
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60) # 24小时有效
               
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'
    print(template_name)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        
        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
