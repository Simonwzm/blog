
---
title: 使用vscode remote插件的一些思考 
date: 2022-09-15 09:36
tags: 
decsription:
cover: https://s2.loli.net/2022/09/15/W5bztOeFpBs4noS.jpg
---


学校的电工导课程需要使用docker环境进行开发。老师推荐使用vscode+remote-container的方式进行。由于不是非常明白其中的机理，所以尝试研究一下官网给出的教程。

Remote container 的功能主要是：在一个开发容器中打开各种项目/repo，同时在容器的开发环境中进行开发

打开的项目可以是：本地的文件夹/GitHubPR/GithubRepo/本地工作区等等。

其用途是可以使开发具有统一的环境，同时依然可以使用vscode本地安装的插件，以及可以与本地文件夹/项目进行互动

以上效果的实现是通过vsocde插件和docker desktop一起做到的。
- 首先，docker desktop提供了docker的守护进程，docker的容器会通过这个守护进程进行管理。
- 其次，我们在vscode中选择需要在容器中进行的操作，如果是打开本地文件夹或者工作区，remote container 会将这个文件夹或工作区作为一个volume传入将来的docker container中，便于容器和宿主机通讯。
- 接着，我们选择需要使用什么container进行开发，使用本地容器可以直接激活，使用远程容器则需要下载。


当docker container 准备完毕，docker会在container中启动一个vscode server，其中配置了容器对环境的要求，额外的插件，同时将本地的插件复制进去，从而配置好需要的工作环境。之后，我们在宿主机上敲代码，vscode本地程序会和container中的server通讯，从而达到环境中开发的目的。最后本地文件夹的volume会挂载到container中的操作系统中，映射到`/workspace`文件夹下
注意，只有存放在volume中的文件才会被保存。

vscode会在第一次创建容器之后，保存一个`.devcontainer`文件，保存了使用什么容器以及需要什么样的环境和vscode插件。如果文件夹中有这个文件，docker会根据这个而打开对应container，配置vscode环境。因此将这个文件一起给到协作者，他们无须对remote container做任何的初始配置既可以使用应有的开发环境。

当然，`.devcontainer` 是可以修改的，所以支持个性化的环境修改。


> 补充： 可以使用远程主机的docker，具体配置看这里：https://code.visualstudio.com/docs/remote/containers#_open-a-folder-on-a-remote-ssh-host-in-a-container

本文的参考资料为：
https://code.visualstudio.com/docs/remote/containers-tutorial
https://code.visualstudio.com/docs/remote/containers#_quick-start-try-a-development-container

volume的学习资料为：
https://docs.docker.com/storage/volumes/

挂载的学习资料为：
https://www.cnblogs.com/cangqinglang/p/12170828.html


