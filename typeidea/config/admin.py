'''
File Name: your project
Mail: 1.0
Author: LH
Created Time: Do not edit
'''
from django.contrib import admin
# import xadmin

# Register your models here.
from .models import Link, SideBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    """class CategoryAdmin
    
    This class is mainly used to view articles by category

    Attributes:
        list_display: Fields stored in the database
        fields:Controls which fields are displayed on the page
    """
    list_display = ("title", "href", "status", "weight", "created_time")
    fields = ("title", "href", "status", "weight")

    """__str__

    Returns the name of the corresponding class
    """
    def __str__(self):
        return self.name


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    """class CategoryAdmin
    
    This class is mainly used to view articles by category

    Attributes:
        list_display: Fields stored in the database
        fields:Controls which fields are displayed on the page
    """
    list_display = ("title", "display_type", "content", "created_time")
    fields = ("title", "display_type", "content")

    """__str__

    Returns the name of the corresponding class
    """
    def __str__(self):
        return self.name
