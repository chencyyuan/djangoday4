from django.urls import path

from article.views import *

app_name='article'

urlpatterns=[
    path('detail',article_detail,name='detail'),
    path('show',article_show,name='show'),
    path('write',article_write,name='write'),
    path('comment',article_comment,name='comment'),
    path('message',blog_message,name='message'),
    path('like',article_like,name='like'), #收藏
    path('collection',article_collection,name='collection'), #我的收藏
]