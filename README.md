# SNSWeiboSystem(社交微博系统)#
	A project that shows how to build a WeiboSystem with Django
	一个展示怎样用Django建立微博系统的工程
## 基本说明 ##
* 这个项目用来展示怎样用**Django**建立一个基本的微博系统，因此我称它**MiniWeiboSystem**
* 整体采用更大型的三层架构， 分离接口和实现
* 使用的平台和工具包括： **Linux+Django+uwsgi+Nginx+Redis+RabbitMQ+Mysql** 
* 插件包括：**JQuery+Bootstrap+Font-Awesome。**
* 实现过程：基于B/S架构,结合数据库与服务器，交互前端和后端。
> 关于相关的配置和说明参考,点击：[Django在Linux上的部署的相关说明](https://github.com/lyamango/DeployDjangoOnLinux)
		
		
## 目录说明
	+ .idea            PyCharm自动生成的配置文件
	+ MiniWeiboSystem  Django自动生成的配置文件
	+ app01            应用文件
	+ static           静态文件(包括font,js,css,plugins)
	+ templates        模板文件(html)
	+ manage.py        Django启动文件
	+ miniweibo.sql    Mysql生成的数据库结构
	+ db.sqlite3       Django自带数据库的文件(可不使用)
### app01目录说明 
	+ forms            关于表单验证的相关功能实现
	+ infrastructure   一些在views中被使用的基础设施
	+ migrations       Django自动生成的相关数据库迁移表
	+ repository       模仿Java风格对领域模型models中定义接口的实现
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

####关于app01->infrastructure下提供的几个小功能说明
``` 
<pre><code>
<span>check_code.py</span><span>&nbsp;&nbsp;&nbsp;生成包含数字和验证码，位数可以调整</span>
<span>commons.py</span><span>&nbsp;&nbsp;&nbsp;生成随机数和md5值</span>
<span>decrator.py</span><span>&nbsp;&nbsp;&nbsp;生成包含数字和验证码</span>
<span>messages.py</span><span>&nbsp;&nbsp;&nbsp;关于邮件发送的python实现</span>
<span>time_for_json.py</span><span>&nbsp;&nbsp;&nbsp;解决HttpResponse和前台Ajax交互序列化相关的问题</span>
</code></pre>

```
	
