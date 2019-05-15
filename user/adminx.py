from xadmin import views

import xadmin
from user.models import UserProfile

# xadmin.site.register(UserProfile)

class BaseSettings(object):
    enable_themes=True     #主题是否可用
    use_bootswatch=True

class GlobalSetting(object):   #全局设置
    site_title='博客后台管理'
    site_footer='CHEN的博客公司'

#注册
xadmin.site.register(views.BaseAdminView,BaseSettings)  #父模板样式
xadmin.site.register(views.CommAdminView,GlobalSetting)  #全局样式