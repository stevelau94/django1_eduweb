# edu网站业务分析
创建多个app models

### user app model设计
1. 用户信息UserProfile  
    首先分析django自带的user表是否满足项目需求,若不满足项目需求则需要自定义。
    首先from django.contrib.auth.models import AbstractUser 继承django自带的user表。

    然后再models文件着那个创建新user表，并进行覆盖

1. 邮箱验证 EmailVerifyRecord
    ```python
    send_time = models.DateTimeField(default=datetime.now)
    ```
    这里的datetime.now**一定不要**写成datetime.now(),会导致时间生成为表创建时间

1. 轮播图 Banner
    由于邮箱验证和轮播图不和其他相关联，所以单独列出。
    
### courses app model设计
分析需求得出：
1. 课程表Course
1. 章节表Lesson
1. 小节视频Video表
1. 课程资源CourseResource表
表之间存在一对多的外键关联

### organization app 课程机构model设计
1. CourseOrg课程机构基本信息
1. Teacher教师基本信息
1. CityDict城市信息

### operation app 
1. UserAsk用户咨询
1. CourseComments用户评论
1. UserFavorite用户收藏
1. UserMessage用户消息
1. UserCourse用户学习课程