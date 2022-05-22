---
title: 使用django构建网页 
date: 2022-05-22 19:45:20
tags: Django
---

## 使用django搭建网页

本笔记中，django项目的文件模型为
-mainproject
 --app=snippets
 
1. 定义模型以及如何使用模型：
```python
class Snippet(models.Model):
    code= models.TextFiled()
    language = models.CharFieild(max_length=20)

#如何使用：
from snippets.models import Snippet
#创建：
Snippet.objects.create(language="sdsd",c0de="sdfsd")

#选择所有
Snippet.objects.all() 

#根据id选择
Snippet.objects.get(pk={number})  #pk就是id

#赋给变量：
snip = Snippet.objects.get(pk=2)

#读取模型的属性
print(snip.id)
print(snip.code)
print(snip.language)

s=Snippet.objects.filter(language='cpp',code="sdfsdf") ##使用与进行搜索

#删除数据
s.delete()

#修改数据并保存！
s.language="sdfsfsdfsdfsdf"
s.save()

#由于模型本来就是一个类，也可以定义类函数处理数据：
def is_cpp(self):
    return self.language = 'cpp'
```

2. 将模型注册起来（可以在网站的admin/中操作）
```python
#enter snippet -> admin.py
from . import models #
admin.site.register(models.Snippet)
```

3. 把网页url交给一个controller处理
django通过`url.py`路由实现url --> controller 的过程

- url分配controller
```python
#enter urls.py
#import 需要的handler
from snippets.views import func1
urlpatterns += [
    path('xxx/yyy/', {func1},name='name1'),
    path('sdcsdc/', {func2}, name='name2'),
]
```

4. 编写controller
controller封装了网站业务逻辑，是一个包装了复杂实现的函数，接受一个request，返回一个reponse

下面展示了不同的情境

- 方法一：返回一个HttpResponse
```python
#enter snippets -> views.py
from django.http import HttpResponse
#basic structure
def func1(request):
    return HttpResponse('<h1>Can be any string</h1>')

# advanced:
def index(request):
    snippet = Snippet.objects.first()
    html=f'<h1>this is your snippet: {snip}, id: {snip.id}</h1>'
    ul=''
    for snip in Snippet.object.all():
        ul += '<li>' + html + '</li>
    newhtml = '<ul>' + ul + '</ul>'
    return HttpResponse(newhtml)
```

- 方法二：使用模板

创建模板：
```html
#enter snippets -> template
#new name.html
use template language + html

<head>
    something
</head>
<body>
    <ul>
        //使用{% %}表示模板，使用{{}}表示数据
        {% for s in snippets %}
        <li> ID: {{s.id}} | Language: {{s.language}}
        </li>
        {% endfor %}
    </ul>
</body>
```

```python
#enter views.py
from django.template import loader
from django.template import loader
from django.shortcuts import render
def index(request):
    #从template目录下获得模板，
    template = loader.get_template('index.html')  
    #获得所要赋给template的数据
    heresnip = Snippet.objects.all()
    使用
    #使用模板渲染的方法返回HttpResponse
    #render接受一个context参数，context就是一个字典，用来接收controller函数里的参数并赋给模板里的变量
    #context={templateVar:controllerVar,...}
    return HttpResponse(template.render(context={'snippets': heresnip}))

    #advance: 直接使用render函数
    return render(request, 'index.html', context={snippets':heresnip})
```


5. 动态确定url并设置对应controller

```python
#enter 主项目 -> urls.py
from snippets.views import details
urlpatterns += [
    #<int:pk>  也可以是 <pk>
    path('<int:pk>' , details,  name='name3')
]
```

如果使用这种格式，python会把url中输入的数字传给pk，同时调用details函数处理这个url，且把pk做为关键字参数传到details这个controller去

```python
#enter views.py
#假设已经制作了对应的details.html模板
#为了显示用户实际输入的格式（空行缩进等），可以使用pre标签
def details(request, pk):
    snip = Snippet.objects.get(pk=pk)

    return render(request, 'details.html',context={'snippets': snip})
```

6. 错误页面处理

解决获取特定页面失败：

先做好对应的controller
```python
#modify previous function details
try:
    snippet= Snippet.objects.get(pk=pk)
    continue...
except:
    #status是返回网页的状态码
    return render(request, '404.html', status=404)
```

制作404.html

```html
......
<body>
    <div> NOT FOUND </div>
</body>
```

便捷版本：
```python
from django.shortcut import get_object_or_404
def details(request, pk):
    snippet = get_object_or_404(Snippet,pk=pk)
```

7. 在每一个app里面也添加一个urlpatterns

为了方便实现层级结构urls映射，我们可以这么做
```python
#enter snippets -> urls.py
urlpatterns = [
    path(),
    path(),
    path(),
    ...
]
```

```python
#enter mainproject -> urls.py
from django.urls import include
urlpatterns= [
    path('', include('snippet.url'))
]
```

8. 模板的模板

为类似的模板创建一个具有其共性的html文件

我们在template目录下建立一个base.html

```html
//enter base.html
<html>
    <head>
        lalala
    </head>
    <body>
        {% block block1 %}
        {$ end block %}
    </body>
</html>
```
block块中是可以让其他html往里面填充东西的地方，其他地方是共同的可以替换的地方

在需要用到base.html的文件里这么写：
```html
//enter new.html
{% extends 'base.html' %}
{% block block1 %}
    <ul>
        <li>dscd</li>
        <li>sdcsdc</li>
    </ul>
{% end block %}
```

这样就可以将其中block1的内容填入base模板的block1中，然后加上base模板中的固定html，从而成为一个完整的new.html文件