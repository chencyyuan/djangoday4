

import xadmin
from article.models import Article, Tag, Comment, Message


class ArticleAdmin(object):
    list_display=['title','click_num','love_num','user','date'] #页面中显示的列
    search_fields=['id','title'] #检索框
    list_editable=['click_num','love_num']  #可编辑列数据
    list_filter=['date','user']  #过滤



class CommentAdmin(object):
    list_display=['nickname','article','date'] #页面中显示的列
    search_fields=['id','nickname'] #检索框
    list_filter=['date']  #过滤

class MessageAdmin(object):
    list_display=['nickname','content','icon','date'] #页面中显示的列
    search_fields=['id','nickname'] #检索框
    list_filter=['date']  #过滤


#注册
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Tag)
xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(Message,MessageAdmin)

