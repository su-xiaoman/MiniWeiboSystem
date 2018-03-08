# SNSWeiboSystem(社交微博系统) #
	A project that shows how to build a WeiboSystem with Django
	一个展示怎样用Django建立微博系统的工程
## 基本说明 ##
* 这个项目用来展示怎样用**Django**建立一个基本的微博系统，因此我称它**MiniWeiboSystem**
* 整体采用更大型的三层架构， 分离接口和实现
* 使用的平台和工具包括： **Linux+Django+uwsgi+Nginx+Redis+RabbitMQ+Mysql** 
* 插件包括：**JQuery+Bootstrap+Font-Awesome。**
* 实现过程：基于B/S架构,结合数据库与服务器，交互前端和后端。
* 整个项目会是一个很棒的Django练习和设计的平台
> jQuery &nbsp;[中文使用教程](http://jquery.cuishifeng.cn/) </br>
> Bootstrap &nbsp;[中文使用教程](https://v3.bootcss.com/) </br>
> Font-Awesome &nbsp;[中文使用教程](http://fontawesome.dashgame.com/) </br>
> 关于uwsgi+Nginx+Redis+RabbitMQ+Mysql相关的配置和说明参考,点击：[Django在Linux上的部署的相关说明](https://github.com/lyamango/DeployDjangoOnLinux)
		
		
## 目录说明
	+ .idea            PyCharm自动生成的配置文件
	+ MiniWeiboSystem  Django自动生成的配置文件
	+ app01            应用文件
	+ static           静态文件(包括font,js,css,plugins)
	+ templates        模板文件(html)
	+ manage.py        Django启动文件
	+ miniweibo.sql    Mysql生成的数据库结构
	+ db.sqlite3       Django自带数据库的文件(可不使用)
	+ .gitattributes   解决git系统无法有效识别项目所用工程语言的必要生成
	+ LICENSE          许可文件，为Mozilla Public License 2.0标准
### app01目录说明 
	+ forms            关于表单验证的相关功能实现
	+ infrastructure   一些在views中被使用的基础设施
	+ migrations       Django自动生成的相关数据库迁移表
	+ repository       模仿Java风格对领域模型models中定义接口的实现
	+ templatetags     simple_tag功能支持必要的文件目录，如分页等
	+ test             自动生成的test文件，移动到此目录
	+ views            Django中MTV三大部分之views(V)
	+ admin.py         自带的admin管理views
	+ apps.py          自动的apps配置注册views
	+ Config.py        全局的相关辅助设置，辅助settings.py配置
	+ Mapper.py        依赖注入的方式等相关基础定义
	+ models.py        Django的ORM，实现了模型定义和相关伪接口定义

## 实现功能 
1. 用户功能： 
	> 注册 &nbsp;
	> 登陆 &nbsp;
	> 发贴 &nbsp;
	> 点赞 &nbsp;
	> 收藏 &nbsp;
	> 评论 &nbsp;
	> 网页分享
2. 管理员功能：
	> 形成Topic &nbsp; 
	> 热贴置顶 &nbsp;  	
	> 违规贴删除 &nbsp;
	> 注册人员管理

#### 关于utilities包提供的三个实用小功能展示说明，具体代码参见源码部分
```python
#此为邮件发送代码功能

def email(email_list,content,subject="新浪微博用户注册"):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(content, 'plain', 'utf-8')

    msg['From'] = formataddr(["新浪科技","你的用户邮箱填写在这里"])
    msg['to'] = formataddr(["You",email_list])
    msg['Subject'] = subject

    try:
        print("正在尝试发送邮件")
        server = smtplib.SMTP()
        server.connect("smtp.163.com", 25)

        server.login("你的用户邮箱填写在这里","你的用户密码填写在这里") #两个参数，账号和密码
        server.sendmail('你的用户邮箱填写在这里',email_list,msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error：无法发送邮件")
```
```python
#此为密码加密等所用功能

def random_code():
	"""
	生成4位数随机码，发送到邮箱
	"""
    code = ""
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90)) #参数是[0,255]的一个整数，返回值是当前整数对应的ascii字符。
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code

def generate_md5(value):
	"""
	用户密码等所用的md5加密功能
	"""
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()
```
```python
#此为验证码的Python实现过程

_letter_cases = "abcdefghijklmnopqrstuvwxyz"  # 小写字母
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(1, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

def create_validate_code(size=(129, 39),
                         chars=init_chars,
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(245, 245, 245),
                         # fg_color=(105, 105, 105),
                         fg_color=(139, 126, 102),
                         font_size=20,
                         font_type="arial.ttf",
                         length=4,
                         draw_lines=False,
                         n_line=(1, 2),
                         draw_points=True,
                         draw_pointes=False,
                         point_chance = 1):

    width, height = size # 宽， 高
    img = Image.new(mode, size, bg_color) # 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line) # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            #结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                    strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

    return img, strs
```

	
