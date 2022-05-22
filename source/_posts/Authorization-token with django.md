---
title: Django 的鉴权操作
date: 2022-05-22 20:05:56
tags: Django
---

(往期补档)
## Topic: Authorization-token with django

在之前的学习中，我们已经熟悉了如何使用 django 搭建一个基本的，可以响应用户请求并提供静态页面的网页后端。不过，如果需要制作一个方便用户登录的网站，需要用到一定的验证方法。如何确定正在访问的使用者是已经登录的用户？如何确保当前用户具有权力查看某些内容？我们需要一种鉴权手段核验身份。因此，我们需继续学习和鉴权有关的知识。

### AAA

AAA = Authentication + Authorization + Audit

Audit: 记录用户操作

TODO: request -> Authorization token Authetication -> is_authenticated -> controllers


### Authorize with django

鉴权的方法不止一种，我们今天学习的是使用 token 鉴权的方法

#### Add a token model

在执行完创建 app 和注册 app 的工作之后，为了实现用 token 鉴权的目的，我们需要新建一个 token 模型

```python
# app-> models.py

from django.contrib.auth.models import User # django default user model

# Use following instead for customized user
from django.contrib.auth.models import AbstractUser # use inherit property to modify complex model

#get current user
from django.contrib.auth import get_user_model

User = get._user_model() #return a current user class

class Token(models.Model):

    # user UUID to define token, id equals to model's name
    # primary_key=True refers to using this name as id in DATABASE
    # default refers to automatically calling a generator function every time a new token is generated, if we wish not to provide the duplicatedcommand every time
    id = models.UUIDFiled(primary_key=True, default=uid.uuid4)

    # let id has one-to-one relationship with a user
    #
    user = models.ForeignKey(User, on_delete=models.CASCADE) # to specify that token will be deleted as user is deleted
```

#### Use a controller to manage login

如果一个 request 直接被送到 controller，我们可以这么做 controller


```python
#app -> veiws.py

from django.http.response import JsonResponse

def index(request, *args, **kwargs):
    # judger if current user has logged in using self-contained method in django
    if request.user.is_authenticated:# return T/F
        return JsonResponse({
            # request.user returns the current user class, within information like username
            'username': request.user.username,
        })
    else:
        return JsonResponse({
            'message': "not Authenticated",
        }, status=401)
```

#### Use middleware to manage login authentication

使用 middleware 对 request 进行处理，然后再发给 controler，实现模块化，可复用等功能

新建 `middleware.py`

Middleware 接受一个 get_response 的犯法，调用这个函数后同时返回一个新的 response

我们先把之前的 views 加到路由，方便后续测试

```python
# in main -> ettings -> urls.py
from django.contrib import adimin
from django.urls import path
from authtoken import views as TokenView # alias

urlpatterns = [
    path('user/me', TokenView.index),
]
```

接着，我们来写 middleware

```python
from django.contrib.auth() import get_user_model
from django.core.exceptions import ValidationError

class TokenMiddleware:

    # 初始化的时候会告知如何 get_response
    def __int__(self,get_reponse):
        self.get_response = get_response

    # 处理请求
    def __call__(self, request):
        # do something
        # 调用认证函数
        self.try_auth(self, request)
        # 使用对应的方法返回经过处理的 request 请求
        return self.get_reponse(request)

    # 认证逻辑
    def try_auth(self, request):
        # 获取请求中的 authenticate
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return
        # 将 auth_header 解包
        auth_method, user_token = auth_header.split(' ')

        # 根据给定的 token 查找对应用户
        try:
            token = TOken.objects.get(pk=user_token)
        except (Token.DoesNotExist, ValidationError):
            return
        # 找到给定用户之后，执行登录操作
        login(request, token.user)

```

现在，我们把写好的 middleware 注册

在 `settings.py` 中的 MIDDLEWARE 列表中末尾加入:
`authtoken.middleware.TokenMiddleware',

至此，对 middleware 的基本构建结束了

#### Desgin a user-defined command to generate token

switch to command line and go into the current app folder

use a python package to implement our command

create a new folder named **management** under the app's folder, and enter into it

create a file named `__init__.py` （can be empty) to denote that this is a python package

add a folder named commands, and enter into it

Add a python file (`<command_name>.py`) with the same name as our command, we can name it token


write in `token.py`

```python

from django.core.management.base import BaseCommand
from authtoken.models import Token
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    # a complete command includes command name and arguments,like: npm run serve, where run is a command, and serve is the argument
    # now the command is token, here we can specify the arguments
    def add_arguments(self, parser):
        # add receivers of argument
        parser.add_argument(
            'action',
            help="blabla"
        )

        parser.add_argument(
            '--user',  # a format of optional arguments
        )

        return super().add_arguments(parser)

    # we will handle the received arguments here
    # the argument option stores the args that user send from cmd,in coordinate with the args defined in function add_arguments
    def handle(self, action *args, **options):
        # designate which function to handle an argument
        actions = {
            'list': self.list_token,
            'generate': self.generate_token,
        }
        if action in actions.keys():
            raise CommandError("unsupported actions")

        # call these functions according to user's input (we stored it in action, or in options[action])
        actions[action](*args, *options)

    # handler_function below:
    def list_token(self, *args, *options):
        tokens = Token.objects.all()

        for token in tokens:
            self.stdout.write(f'{token.user.id} {token.id} {token.user.username}')

    def print_token(self, token):
        self.stdout.write('%s\t%s\t%s' %(token.user.username, token.user.id, token.id))

    # to generate a token, we need to add a optional arguments
    def generate_token(self, *args, **options):
        user = self.fet_user(*args,**options)
        # we have defined the token model to have to arguments, user and id ,while id is defaulted to have a generated function, so we only need to provide a user

        token = Token(user=user)
        token.save()
        self.print_token(token)
        self.stdout.write(self.style.SUCCESS('successfully generate a token'))


    def get_user(self, *args, **options):
        # get user input
        # since we only generate token for registered user, we need to look for him in the database:
        if options['user']:
            username_or_id = options['user']
            # get all users
            User = get_user_model()
            # find user: compare input with database
            try:
                user = User.objects.filter(pk=username_or_id).get()
            except (User.DoesNotExist, valueError):
                try:
                    user=User.objects.Filter(username=username_or_id).get()
                except:
                     User.DoeseNotExist("balbal")
            # return user if we find him in database
            return user

        else:
            raise CommandError("no user given")
```

now we create a superuser to test the command.

`python manage.py createsuperuser testU`

generate:
`python manage.py token generate --user truco`

to design a command, first we need to design argument receiver according if needed, then we use these inputs to implement the according handler function

interaction methods:
```python
def handler_function(self, *args, **kwargs):
    # need user's input
    confirm = input(self.style.ERROR('some txt'))
    # judge according to user's input
    if comfirm != 'y':
        self.stdout.write('exit')
```


#### CORS settings

除去我们可以引入 CORS 包的方法，我们可以自己设计 Middleware 解决这个问题

```python
# inside middleware.py
class CorsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 不直接返回 response 请求，而是需要在里面加上 CORS
        response = self.get_response(request)
        # 在 CORS 允许访问的地址里面加入对应地址，注意协议 + 域名 + 端口号必须全部一致
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:<front_end_port>'
        response.headers['Access-Control-Allow-Methods']= 'GET,POST,PUT'
        response.headers['Access-Control-Allow-Headers'] = '...'
        return response
```


