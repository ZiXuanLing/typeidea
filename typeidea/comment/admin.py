'''
File Name: your project
Mail: 1.0
Author: LH
Created Time: Do not edit
'''
from django.contrib import admin

# Register your models here.
from .models import Comment
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_distplay = ('target', 'nickname', 'content', 'website', 'created_time')

    """__str__

    Returns the name of the corresponding class
    """
    # def __str__(self):
    #     return self.name
