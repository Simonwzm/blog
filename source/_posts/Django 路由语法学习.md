---
title: Django 中的路由语法学习
date: 2022-05-22 21:05:56
tags: Django
---

## Django 中的路由语法学习

### 在 Django 模板中使用 url 路由

当我们同样需要在 django app 中使用到动态路由的功能的时候，我们可以在 `urls.py` 中，使用 `<int:pk>` 的方法将 url 里面的变量传入对应的 controller 手中。

如果要在模板中这样写，我们可能需要对应的模板语言

-  方法一：静态语言

    在一个模板中使用 `<a>` 标签跳转的时候，直接写出需要跳转到的 url

    ```html
    {% for s in snippets %}
    <div>
        // 转到/s.id目录
        <a href="/{{s.id}}"> Visit -> </a>
    <div>
    <div>
        <a href="/about"> About Page </a>
    <div>
    ```

    缺点就是必须手动更改许多内容，无法实现同步


-  方法二：使用url 方法

    在对应的模板中，使用 url 方法，跳转到指定的网页

    ```html
    {% for s in snippets %}
    <div>
        //表达需要填充的url为：类型是name对应的url类型，需要传入的参数是 s.id
        <a href = "{% url 'name_of_path' s.id %}"> Visit -> </a>
    </div>
    ```

    为了防止其他app中也会有相同的details页面，需要分开处理逻辑，我们可以这样改进

    ```python
    #enter urls.py in snippets
    app_name = 'snippets'
    urlpatterns = [
        path('example/pk', detail, name='detail'),
    ]
    ```

    然后在需要用这个 app 里的 details 处理页面的，我们这么修改链接
    ```html
    ...
    <div>
        <a href="{% url 'snippets:details' s.id %}"> Visit here again! -> </a>
    </div>
    ```

### 使用 form 发送请求

用户点击 form 中的 submit 按钮的时候，浏览器负责将 form 中的数据传给服务器。可以理解 form 为一个容器

我们可以这么写一个 form

```html
<form
    action="target_url"
    method="POST" //可以用除了DELETE之外的任何方法
    //stylehere
    class="sdf"
>
    <div>
        <label
            for="language"
            //指定谁的label
            class="sdfs"
            //stylehere
        >scription text </label>

        <input type="text" name="xx" style="" class="".../>
        <textarea />
        ...
    </div>
    <div>
        <label
            for="language"
            //指定谁的label
            class="sdfs"
            //stylehere
        >scription text </label>

        <input type="text" name="xx" style="" class="".../>
        <textarea />
        ...
    </div>
    <div>
        <label
            for="language"
            //指定谁的label
            class="sdfs"
            //stylehere
        >scription text </label>

        <input type="text" name="xx" style="" class="".../>
        <textarea />
        ...
    </div>
    <button> submit </button>
</form>
```

### 在 django 中向目标 url 发送请求实例

我们在一个 created.html 中向 index controller 负责的页面发送数据

我们需要一个 csrf_token 进行验证

```html
{% block body %}
<main>
    <form 
        action="{% url 'snippetsindex' %}"
        method="POST"
        {% csrf_token %}
        ...>
        <div>
            <label>
                sdf
            </label>
            <input ... />
        </div>
        <button> submit </button>
    </form>
</main>
{% end block %}
```

此时，我们可能要在对应的 controller 中添加处理 POST 请求的功能

```python
def index(response):
    if request.method = "POST":
        #for example:
        #request.POST 包含了POST请求带有的所有信息

        #有两种方法可以取出其中的数据
        language = request.POST['language']
        code = request.POST.get('code')
        newSnippet = Snippet.objects.create(language=language, code=code)
        snippet = Snippet.objects.all()

        return render(request, 'index.html', context={'snippets': snippets}
        )
    else:
        return ...
```

### django 重定向

我们简单了解一下重定向的使用方法
如果一个 controller 需要返回的页面属于别的 controller 处理的，可以使用重定向方法，而不是把另一个 controller 中的函数复制过来：

```python
def example(request):
    #...
    snippet = Snippet.objects.create(language="sdf", code= "sdfsdf")
    redirect(controller, args)
    return redirect('snippets:detail', pk=snippet.id)
```

### django 使用 forms 检查表单

当我们需要检查提交的表单或者据此决定下一步操作的时候，我们可以在 controller 中手动写 if 语句等做到。除此以外，我们也可以使用 django 中的 `forms.py` 做到

在对应 app 中创建 `forms.py` 文件:
```python

from django import forms

class =SnippetForm(forms.Form):
    language = forms.CharFiled()
    code = forms.CharField()

```

在需要引用的 controller 可以这么写：
```python
#enter views.py

def index(request):
    form = SnippetForm(request.POST)
    if form.is_valid():
        ...
        return ...
    else:
        ...
        return ...
```

我们也可以将forms作为参数传给模板：
`return reder(request, 'create.html', context={'form': SnippetForm()})`

这里的 `SnippetForm()` 是创建了一个 SnippetForm 的实例

然后再在对应的 create.html 中引用form
```html
//In create.html
{% extends 'base.html' %}
{% block bck %}
{{form}}
...
{% end block %}
```

最后在 forms.py 中加入样式
```python
class SnippetForm(fomrs.Form):
    language= fomrs.CharField()
    #让code输入框变成 Textarea
    code = forms.CharField(widget=forms.Textarea())

```

### 使用 django 中的 View 类制作 controller

如果一个 controller 需要接受许多不同的请求类型，我们可以让他继承自 View 类进行代码优化

```python
#enter views.py

from django.views.generic import View

class IndexView(view):

    def get(self, request, *args, **kwargs):
        #...
        return render(request, 'index.html', context={'snippets': snippets})
    
    def post(self, request, *args, **kwargs):
        #...
        return render...

```

在对应的路由中，需要这样修改：
```python
#enter urls.py
from .views import IndexView...
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(),
    path(),
]
```
### django 返回 JSON 数据

如果返回值是 JSON 格式的数据，需要先将其表示成字典的格式，然后再调用 JsonResponse() 返回之

```python
#某个controller中
#...

from django.httop import JsonResponse

snippets = Snippet.objects.all()
#使用字典生成式列出字典
serialized = {s.id: {'code':s.code, ;'language':s.language,} for s in snippets}
return JsonResponse(serialized)
```


