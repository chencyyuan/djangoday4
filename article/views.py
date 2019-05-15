from django.contrib.auth.decorators import login_required
from django.core.checks import Tags
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from article.forms import ArticleForm
from article.models import Article, Tag, Comment, Message
from user.models import UserProfile


def index(request):
    articles = Article.objects.all().order_by('-click_num')
    # print(articles)
    darticles = Article.objects.all().order_by('-date')[:8]
    # print((darticles))
    return render(request, 'index.html', context={'figure_articles': articles[:3], 'darticles': darticles})

#文章详情
def article_detail(request):
    id=request.GET.get('id')
    article=Article.objects.get(pk=id)
    article.click_num+=1
    article.save()
    #上一篇，下一篇 将文章传到前台
    pre_article=Article.objects.filter(id__lt=id).order_by('-id').first()
    next_article=Article.objects.filter(id__gt=id).order_by('id').first()
    # print(article.tags.all())
    #查询相关文章
    tags_list=article.tags.all()  #在views里写要加()    查询当前文章的所有标签
    list_about=[]   #存放文章的列表
    for tag in tags_list:
        # print(tag.article_set.all())
        for article1 in tag.article_set.all():  #根据标签找相关的文章
            if article1 not in list_about and len(list_about)<6:
                list_about.append(article1)

    #查询评论数
    comments=Comment.objects.filter(article_id=id)

    return render(request,'article/info.html',context={'article':article,'list_about':list_about,'pre_article':pre_article,'next_article':next_article,'comments':comments})

#学无止境
def article_show(request):
    tags=Tag.objects.all()[:6]
    tid=request.GET.get('tid',"")
    if tid:      #根据标签筛选文章
        tag=Tag.objects.get(pk=tid)
        articles=tag.article_set.all().order_by('-date')
    else:
        articles=Article.objects.all().order_by('-date')

    paginator=Paginator(articles,3)  #Paginator(对象列表，每页显示几条)
    # print(paginator.count)  #总的条目数  总的记录数
    # print(paginator.num_pages) #可以分页的数量
    # print(paginator.page_range) #页面的范围

    # 方法： get_page()
    page = request.GET.get('page', 1)
    page = paginator.get_page(page)  # 返回的是page对象  获取当前(页码)
    page_list = [x for x in range(page.number - 2, page.number + 3) if x in paginator.page_range]
    # print(page_list)

    # 添加省略号

    if page_list[0] - 1 >= 2:  # 判断当前第一个元素减1是否大于2
        page_list.insert(0, "...")  # 则插入该数组成为第一个元素 ...
    if paginator.num_pages - page_list[-1] >= 2:  # 判断最大页码数-最后一个元素相减是否大于2
        page_list.append("...")  # 则添加一个元素
    # print(page_list)

    # 添加首尾页
    if page_list[0] == "...":
        page_list.insert(0, 1)  # 则插入该数组成为第一个元素(首页)
    if page_list[-1] != paginator.num_pages:  # 判断是否不等于最大页码
        page_list.append(paginator.num_pages)  # 不等于则插入到最后一个元素(尾页)
    # print(page_list)

    # page.has_next()  # 有没有下一页
    # page.has_previous()  # 判断是否存在前一页
    # page.next_page_number() # 获取下一页的页码数
    # page.previous_page_number() # 获取前一页的页码数

    # 属性：
    # object_list   当前页的所有对象
    #  number       当前的页码数
    # paginator     分页器对象

    return render(request,'article/learn.html',context={'tags':tags,'page':page,'tid':tid,'page_list':page_list})

#写博客
@login_required
def article_write(request):
    if request.method=='GET':
        aform=ArticleForm()
        return render(request,'article/write.html',context={'form':aform})
    else:
        aform=ArticleForm(request.POST,request.FILES)
        # print(aform)
        if aform.is_valid():
            data=aform.cleaned_data
            # print(data)
            article=Article()
            article.title=data.get('title')
            article.desc=data.get('desc')
            article.content=data.get('content')
            article.image=data.get('image')
            article.user=request.user  #1对多 直接赋值
            article.save()
            #文章和标签多对多，先保存文章生成id,再保存标签
            article.tags.set(data.get('tags'))
            return redirect(reverse('index'))
        # else:
            # print('----->校验失败')
    return render(request,'article/write.html',context={'form':aform})

#文章评论
def article_comment(request):
    nickname=request.GET.get('nickname')
    content=request.GET.get('saytext')
    aid=request.GET.get('aid')
    comment=Comment.objects.create(nickname=nickname,content=content,article_id=aid)

    if comment:
        data={'status':1}
    else:
        data={'status':0}
    return JsonResponse(data)

#留言
def blog_message(request):
    messages = Message.objects.all().order_by('-date')
    paginator = Paginator(messages, 8)
    # 获取页码数
    page = request.GET.get('page', 1)
    # 得到page对象
    page = paginator.get_page(page)
    page_list = [x for x in range(page.number - 2, page.number + 3) if x in paginator.page_range]

    # 添加省略号
    if page_list[0] - 1 >= 2:  # 判断当前第一个元素减1是否大于2
        page_list.insert(0, "...")  # 则插入该数组成为第一个元素 ...
    if paginator.num_pages - page_list[-1] >= 2:  # 判断最大页码数-最后一个元素相减是否大于2
        page_list.append("...")  # 则添加一个元素
    # 添加首尾页
    if page_list[0] == "...":
        page_list.insert(0, 1)  # 则插入该数组成为第一个元素(首页)
    if page_list[-1] != paginator.num_pages:  # 判断是否不等于最大页码
        page_list.append(paginator.num_pages)  # 不等于则插入到最后一个元素(尾页)

    if request.method=='GET':
        return render(request,'article/message.html',context={'messages':messages,'page':page,'page_list':page_list})
    else:
        name=request.POST.get('name')
        mycall=request.POST.get('mycall')
        lytext=request.POST.get('lytext')
        if name and lytext:
            message=Message.objects.create(nickname=name,icon=mycall,content=lytext)
            if message:
                return redirect(reverse('article:message'))
        return render(request,'article/message.html',context={'page':page,'page_list':page_list,'error':'必须输入用户昵称'})

#点赞
def article_like(request):
    if not request.user.id:
        data = {'status': 2}
    else:
        uid=request.user.id
        aid=request.GET.get('aid')
        article = Article.objects.get(pk=int(aid))
        ulist = UserProfile.objects.get(pk=int(uid))
        if request.user:
            #该文章是否被收藏
            ulike = article.collect.filter(id=uid)
            if ulike: #已收藏 点赞数量-1， 删除关联表中的数据
                article.love_num -= 1
                article.save()
                article.collect.remove(ulist)
                data = {'status': 0}
            else: #未收藏 点赞数量+1， 增加关联表中的数据
                article.love_num += 1
                article.save()
                article.collect.add(ulist)
                data = {'status': 1}
    return JsonResponse(data)

@login_required
def article_collection(request):
    user = UserProfile.objects.get(id=request.user.id)
    user_like=user.article_user.all()
    return render(request, 'article/collection.html', context={'user_like': user_like})
