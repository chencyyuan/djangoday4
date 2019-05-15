from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
#继承AbstractUser    修改setting.py文件 权限问题


class UserProfile(AbstractUser):
    mobile=models.CharField(max_length=11,verbose_name='手机号码',unique=True)
    icon=models.ImageField(upload_to='uploads/%Y/%m/%d',default='uploads/mine1.png')
    yunicon=models.CharField(max_length=200,default='')


    class Meta:
        db_table='userprofile'
        verbose_name='用户表'
        verbose_name_plural=verbose_name
