# Django 在线教育网站开发

最近在跟一个mooc实战课，使用django搭建在线教育网站。
1. 项目相关配置及问题解决
1. Django业务分析和数据库设计
    [tips]项目中存在多个app,可以新建apps文件夹存储这些app,然后将apps目录加载settings文件中，设置成根目录

1. 后台管理系统的搭建，使用xadmin以及将项目各张表注册进后台管理系统,以及一些xadmin的个性化定制
    [tips]项目中存在多个第三方拓展，可以新建extra_apps文件夹存储这些拓展,然后将extra_apps目录加载settings文件中，设置成根目录
    
1. 前台页面的配置，主要是基于前端已经完成的页面配置和修改后台django  
    用户注册功能  
    验证码以及邮箱激活
    修改密码功能