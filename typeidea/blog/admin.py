from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

# from xadmin.layout import Row, Fieldset
# from xadmin.filters import manager
# from xadmin.filters import RelatedFieldListFilter
# import xadmin

# Register your models here.
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

"""SimpleListField
The SimpleListField provides two attributes and two methods to override. 
Title is used to show the title, and parameter_name is the name of the query 
    URL parameter. 
For example, what is the query part after the URL for class ID 1? Owner_category =1, 
now we can get this ID through our filter to filter
"""


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    A custom filter displays only the current user category

    Methods:
        Lookup: Returns the content to be displayed and the ID used for the query
        Queryset: Returns list page data based on the contents of the URL query
    """
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

    # xadmin
    # @classmethod
    # def test(cls, field, request, params, model, admin_view, filed_path):
    #     return field.name == 'category'
    
    
    # def __init__(self, field, request, params, model, admin_view, field_path):
    #     super().__init__(field, request, params, model, admin_view, field_path)
    #     self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


# manager.register(CategoryOwnerFilter, take_priority=True)


@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline, ]

    """__str__

    Returns the name of the corresponding class
    """
    # def __str__(self):
    #     return self.name

    """class CategoryAdmin
    
    This class is mainly used to view articles by category

    Attributes:
        list_display: Fields stored in the database
        fields:Controls which fields are displayed on the page
    """
    list_display = ("name", "status", "is_nav", "created_time")
    fields = ("name", "status", "is_nav")


@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    """__str__

    Returns the name of the corresponding class
    """
    # def __str__(self):
    #     return self.name


    """class TagAdmin
    
    This class displays articles based on tags

    Attributes:
        list_display: Fields stored in the database
        fields:Controls which fields are displayed on the page
    """
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):

    form = PostAdminForm
    """__str__

    Returns the name of the corresponding class
    """
    # def __str__(self):
    #     return self.name
    
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    list_display_links = []

    list_filter   = [CategoryOwnerFilter]
    # list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top    = True
    actions_on_bottom = True

    # edit
    # Save_on_top controls whether the button is displayed at the top of the page
    save_on_top = True

    # Exclude specifies which fields are not to be displayed
    exclude = ('owner', )

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    # form_layout = (
    #     Fieldset(
    #         '基础信息',
    #         Row("title", "category"),
    #         'status',
    #         'tag',
    #     ),
    #     Fieldset(
    #         '内容信息',
    #         'desc',
    #         'content',
    #     ),
    # )

    """Custom methods

    A custom function takes a fixed argument, which is the object in the current row.

    Returns:
        The custom function returns HTML, but with the format_html function processing, 
        reverse resolves the URL based on the name
    """
    def operator(self, obj):
        return format_html(
            '<a href="{}"> 编辑 </a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    # Importing static resources, admin
    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js' ,)

    # @property
    # def media(self):
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     })    
    #     return media


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
