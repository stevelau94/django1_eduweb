# Django项目初始配置相关问题及解决
##### 环境 django1.11 python3.6 windows10 pycharm navicat mysql

使用pycharm建立django项目。首先基础配置，需要再pycharm的Tools中Run manage.py Task生成message文件夹，还需要增加static静态文件目录，media用户上传文件目录，log日志文件目录。
为防止生成多个app导致目录环境混乱，设立apps文件，将message转移至其中。  
[pycharm技巧]可以将文件夹mark成sources root,方便项目内导入。

### 配置数据库
在准备文件准备好后，开始配置数据库。
在settings文件的database处，将数据库配置为mysql.
(需要表名，用户名和密码，还有HOST)
然后执行manage.py文件，再执行makemigrations，此时会报错缺少模块。


[解决MySQL_for_python问题]  
安装MySQL_for_python，但是安装时出现问题，可以在[这个网站](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
查找到MySQL-python，然后下载到本地用pip安装，但是，使用pip安装时有一次出现问题。
```python
import pip
print(pip.pep425tags.get_supported())
# [('cp36', 'cp36m', 'win_amd64'), ('cp36', 'none', 'win_amd64'), ('py3', 'none', 'win_amd64'), ('cp36', 'none', 'any'), ('cp3', 'none', 'any'), ('py36', 'none', 'any'), ('py3', 'none', 'any'), ('py35', 'none', 'any'), ('py34', 'none', 'any'), ('py33', 'none', 'any'), ('py32', 'none', 'any'), ('py31', 'none', 'any'), ('py30', 'none', 'any')]

```
发现是下载的MySQL_python-1.2.5-cp27-none-win_amd64.whl文件名不符合pip安装规范，此时强行将文件名修改成符合安装规范的(MySQL_python-1.2.5-cp36-none-win_amd64.whl)就可以使用pip安装了。

[解决py3使用django连接mysql问题]  
但是此时运行manage文件，依旧显示找不到module.
查了一下发现问题是这样的：
>在 python2 中，使用 pip install mysql-python 进行安装连接MySQL的库，使用时 import MySQLdb 进行使用

>在 python3 中，改变了连接库，改为了 pymysql 库，使用pip install pymysql 进行安装，直接导入即可使用

>但是在 Django 中， 连接数据库时使用的是 MySQLdb 库，这在与 python3 的合作中就会报以下错误
>django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'

> 解决方法：在 __init__.py 文件中添加以下代码即可。
```python
import pymysql
pymysql.install_as_MySQLdb()
```
>让 Django 把 pymysql 当成 MySQLdb 来使用  
[文章地址](https://blog.csdn.net/LHYzyp/article/details/70550683)

然后再运行manage，执行makemigrations命令就不会报错了。
再执行migrate，会在数据库自动生成多个表.


### 配置URL

在message.view中，添加getform函数，render html文件
在url文件中，添加url(r'^form/$', getform)配置url
在settings文件中的TEMPLATES中，配置'DIRS': [os.path.join(BASE_DIR, 'templates')]配置templates位置
运行项目应该可以打开静态页面

但是此时静态页面没有style.需要继续在settings文件中配置根目录
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
```
此时可以正常打开页面

### 配置models

需要在message(新建的app)中的models定义ORM模型。
需要将新建的app(message)注册到settings.INSTALLED_APPS中

### 测试页面

在template中准备好HTML页面  
在static中准备好css文件  
在app的view中设置好render，测出可通过ORM操作数据库  
在HTML中设置action="/form/"  
[注意]有表单提交的的情况 需要加上    {% csrf_token %}
