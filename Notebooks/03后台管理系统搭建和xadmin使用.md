# 后台管理系统搭建和xadmin使用

### 原生admin管理系统
django有自带的后台管理系统，使用createsuperuser可以创建超级用户。
在每个app下的admin中，可以将本app的model关联成admin显示在后台管理页面.

### Xadmin
1. xadmin的安装
[python3安装xadmin出现错误]
```python
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa4 in position 3444: illegal multibyte sequence
```
经查询，是由于README.rst这个文件的编码有问题，可以内容没什么重要的，可以直接到github上下载安装包，然后新建一个txt空文件，把文件名改成README.rst，替换原来的文件

[xadmin的github](https://github.com/sshwsfc/xadmin)

然后再本地使用Pip install安装就好

将'xadmin','crispy_forms'注册到setting.INSTALLED_APPS中

并将urls内的管理路由修改成    url(r'^xadmin/', xadmin.site.urls)  
然后运行项目，可以直接进入xadmin后台管理页面。

[推荐源码安装方式]  
从github下载xadmin的源码，然后将解压的文件直接粘贴进项目目录中，新建extra_apps并存放在其中，为了方便我们更好的对第三方控件个性化进行设计

1. 相关表的xadmin注册
新建adminx.py文件，与原生管理系统注册类似
```python
import xadmin
from .models import EmailVerifyRecord
class EmailVerifyRecordAdmin(object):
    pass
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
```

注册时可定义
list_display 显示表中的哪些列
search_fields 搜索范围(有此字段会自动添加搜索框)
list_filter 筛选字段(有此字段会自动添加过滤器)
过滤器 存在外键的情况，可以直接通过双下划线'__'指定需要的外键表单项目

[django xadmin与其他管理系统的区别]
django后台系统主要是对各张表进行增删改查等功能，而非像其他的后台系统以功能为单位，所以django的后台不依赖具体业务逻辑。

配置xadmin的全局变量以及一些个性化操作
1. 主题  
    将BaseSetting设置配置进user的adminx文件中
    ```python
    import xadmin
    from xadmin import views
    
    class BaseSetting(object):
        enable_themes = True
        use_bootswatch = True
        
    xadmin.site.register(views.BaseAdminView,BaseSetting)
    ```
1. 图标，注脚以及页面收缩  
    将GlobalSettings设置配置进user的adminx文件中
    ```python
    import xadmin
    from xadmin import views
    
    class GlobalSettings(object):
        site_title = 'edu后台管理系统'
        site_footer = 'steve lau'
        menu_style = 'accordion'
    
    xadmin.site.register(views.CommAdminView,GlobalSettings)
    ```
1. 菜单显示名称
    在apps.py文件中设置verbose_name  
    在__init__.py文件中设置: default_app_config = 'app名.apps.app名Config'