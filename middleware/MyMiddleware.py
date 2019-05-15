from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

'''
        # print(request.META)
        # remote_host=request.META['REMOTE_HOST']
        # print(remote_host)
        print(request.path)
        #request对象 ----》就是view function函数的request
        print(request.url)
'''
login_list=['/user/center',]

class MiddleWare1(MiddlewareMixin):
    #重写方法
    # 处理的是request请求
    def process_request(self,request):
        print('---------->1')
        print(request.META['REMOTE_ADDR'])
        path=request.path
        if path in login_list:
            if not request.user.is_authenticated:   #未登录
                return redirect(reverse('user:login'))
    #进入view之前调用的函数
    def process_view(self,request,callback,callback_args,callback_kwargs):
        print('callback_args',callback_args)
        print('callback_kwargs',callback_kwargs)
        print('----------->view',callback)

    #render(request,'xxx.html'
    def process_template_response(self):
        pass

    #进入页面之前报异常
    def process_exception(self):
        pass


    def process_response(self,request,response):
        print('------------>response')
        return response

class MiddleWare2(MiddlewareMixin):
    #重写方法
    def process_request(self,request):
        print('---------->2')