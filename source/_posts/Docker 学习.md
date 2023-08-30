---
title: Docker 学习
date: 2022-08-22 16:20
tags: 
decsription:
cover: "https://s2.loli.net/2022/08/23/GoYaeEtwx2y6WKq.jpg"
---

# Docker 学习

当我们有一种开箱即用的开发需求的时候，docker在此时就有了用武之地。docker可以将某个开发环境和其中的服务打包，组成一个image。这个image就可以在任何一台装有docker且符合十分基本条件的机器上使用该image生成container。container就是映像类的实例（如此理解不甚完整，但是便于自己的记忆），我们也可以修改参数，从image产生的不同的container。而且，对image的修改也是十分迅速的，归功于docker使用的“写时复制”模型。

Docker的核心组件有：

- docker客户端和服务器：docker服务器或说守护进程负责控制各种运行中的容器，同时处理从客户端来的各种请求。**客户端和服务器可以运行在同一台机器上，也可以是远程服务器**。如果运行在同一台机器上的话，服务器即docker的守护进程。

- Docker的镜像和容器：可以理解为镜像是类，容器是对象

将 docker 作为一种工具使用，在了解docker的一些基本原理和一些常用命令的参数解释后，我们主要关注docke的一些命令的用法

本笔记所用参考书为《第一本Docker书修订版》，内容多集中在前5章

## 使用ubuntu安装docker

此处参考了这篇[教程](https://yeasy.gitbook.io/docker_practice/install/ubuntu)。这里就不再重复了

简单总结一下就是首先添加docker软件源，然后再安装。

安装完后启动docker：

```bash
sudo systemctl enable docker
sudo systemctl start docker
# sudo systemctl stop docker
# sudo systemctl restart docker
```

有关建立docker用户组的问题，我并没有尝试。我对用户组的概念不是非常熟悉，不太想多建一个组，不过确实建立docker组可以避免很多需要权限的地方要加sudo～

之后要做的一部是配置国内镜像。国内从docker hub 拉取镜像有点困难，所以才需要国内镜像。

需要在`/etc/docker/daemon.json`文件中写入以下源（没有文件就sudo创建一个）

```bash
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

之后重启docker服务：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

检查成功方法：
`docker run --rm hello-world`

若输出以下结果说明安装成功：

```bash
$ docker run --rm hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete
Digest: sha256:308866a43596e83578c7dfa15e27a73011bdd402185a84c5cd7f32a88b501a24
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

安装完，下次开机后可以运行
`sudo docker info` 查看docker守护进程是否开启

## Docker 容器基本运行

### 运行（关闭）交互式容器

```bash
# sudo docker run [--name name] [-i] [-t] [image_name] [cmd]
#e.g.:
sudo docker run -i -t ubuntu:20.04 /bin/bash
```

--name 为容器设定一个名字，方便唤起，否则只能用run命令返回的id

-i, -t 命令通常一起使用，-i开启容器中的标准输入，-t指示docker为创建的容器分配一个伪终端，这样我们就得到了一个可以交互的容器，而不是一个运行在后台的容器

/bin/bash 命令指示docker在新容器中运行/bin/bash命令，启动了一个bash shell

使用exit退出终端的同时，可以退出容器，且容器会关闭。如果是后台的容器，可以使用

```bash
sudo docker stop xxx
```

结束之。

如果是重新开启某个容器，使用上例中的结构，stop改成start即可

### 运行守护式程序

```bash
sudo docker run --name xxx -d ubuntu:latest /bin/sh -c "xxx"
```

此时docker使这个容器在后台运行， -c 指令附加了容器开始的时候所要运行的指令

### 查看当前主机上的容器

可以使用`sudo docker ps [-a]` 查看所有本机上的容器，不添加 -a 只会列举当前运行中的容器

### 查看正在运行的容器的状态

如果要查看容器对硬件的占用信息，可以使用：

```bash
sudo docker stats
```

如果是一个交互式的容器，可以使用 attach + name/id 回到之前的运行中的交互式容器的shell

如果不是交互式的，可以使用

```bash
sudo docker logs name/id
```

列出最近一些容器中的日志（log）

可以使用

```bash
sudo docker logs --tail 0 -f name
```

跟踪容器最新的日志。

如果要查看容器的进程，可以使用，

```bash
sudo docker top name
```

### 为运行中的容器附加进程

同样，附加的进程也分为交互式的和后台式的

附加一个后台进程的命令：

```bash
sudo docker exec -d name cmd
```

附加一个交互的任务的方法为：

```bash
sudo docker exec -t -i name (cmd, e.g.:) /bin/bash
```

上述命令如果添加 -u 的参数，可以指示进程所属的用户

### 其他操作

- 删除容器: sudo docker rm name/id

## Docker hub 的一些操作

- tag: 使用 name:tag 的方式可以指定一个具体tag的image，通常被用来指定特定版本的镜像

- pull: 可以通过docker pull命令先发制人地将镜像从docker hub拉取到本地

## 使用的 Dockerfile 构建镜像

Dockerfile由一系列指令和参数组成。每条指令，如FROM，都必须为大写字母，且后面要跟随一个参数 eg:
`FROM ubuntu:14.04`。Dockerfile中的指令会按顺序从上到下执行，所以应该根据需要合理安排指令的顺序。

Dockerfile构建镜像的过可以立即诶为：每条指令在之前的镜像上多加了一个图层，得到一个修改过的镜像。如此不断地叠加，镜像变得越来越符合我们的需要。

其流程又可以写成：

1. Docker从基础镜像运行一个容器。
2. 执行一条指令，对容器做出修改。
3. 执行类似docker commit的操作，提交一个新的镜像层。
4. Docker再基于刚提交的镜像运行一个新容器。
5. 执行Dockerfile中的下一条指令，直到所有指令都执行完毕。

### Dockerfile中的常用指令

1. CMD
    Dockerfile中的CMD指令指定一个容器启动时**启动时运行的命令**，RUN命令指image被构建时要运行的命令。CMD类似docker run image 后面所追加的命令，两者等效。
    在Dockerfile中只能指定一条CMD指令，后面的CMD会覆盖前面的CMD，即仅最后一个有效。而在`sudo docker run ...`后面跟上的指令，则可以覆盖dockerfile中的cmd指令

2. ENTRYPOINT
   ENTRYPOINT 的作用类似于CMD。但是ENTRYPOINT不能像CMD一样直接被命令行中的语句覆盖。

   > 通常我们也会用数组的形式为ENTRYPOINT和CMD书写命令，比如：
   > `ENTRYPOINT ["/usr/sbin/nginx"]`，`ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]`
   > 其好处是可以直观地指定多个参数

3. WORKDIR
   用来在容器内部设置一个工作目录，其后的CMD和ENTRYPOINT指令就在这个工作目录中运行
   如下方代码所示：

   ```Dockerfile
   WORKDIR /opt/webapp/db
   RUN bundle install
   WORKDIR /opt/webapp
   ENTRYPOINT [ "rackup" ]
   ```

4. ENV
   用来在镜像构建过程中设置环境变量，设置好的变量可以在后续的任何RUN指令中使用
   如下方代码所示：

   ```Dockerfile
   ENV RVM_PATH /home/rvm/
   ```

5. USER
   用来指定镜像会以什么用户运行
   如下方代码所示：

   ```Dockerfile
   USER nginx
   ```

6. VOLUMN
   创建一个卷的指令。一个卷是一个或者多个容器内被选定的特定的目录，这个目录可以绕过联合文件系统，并提供如共享数据或者对数据进行持久化的功能。

   - 卷可以在容器间共享和重用。
   - 一个容器可以不是必须和其他容器共享卷。
   - 对卷的修改是立时生效的。
   - 对卷的修改不会对更新镜像产生影响。
   - 卷会一直存在直到没有任何容器再使用它。

   卷功能让我们可以将数据（如源代码）、数据库或者其他内容添加到镜像中而不是将这些内容提交到镜像中，并且允许我们在多个容器间共享这些内容。我们可以利用此功能来测试容器和内部的应用程序代码，管理日志，或者处理容器内部的数据库。

   可以如下使用VOLUME指令:

   ```dockerfile
   VOLUME ["/opt/project"]
   ```

   这样就会在如下的地方创建挂载点

7. 其他
   其他如copy，add等都是比较常见的命令，这里不再一一介绍暂时
