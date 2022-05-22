---
title: 整理配置 Cmake 的若干问题
date: 2022-05-23 19:05:56
tags: Cmake
---

（往期补档）
最近使用clion的时候接触到了使用Cmake编译C++项目的方法，然而官方文档中的解释并不简单明了，故整理一下关于 `cmake` 的配置问题，加强记忆。

一个 `C++` 项目的格式可能长这样

```
- project_demo
	- lib1
		- cmake.txt
		- module1.cpp
		- module2.h
	- cmake.txt
	- main.cpp
```

模块内 cmake 文件的写法将是：

```
add_library(lib1 module1.cpp module2.h) // 生成库文件
```

整个项目的 cmake 文件的写法将是：

```
//include_directory(lib1) 是头文件的引用目录，可以不写
add_subdirectory(lib) // 添加其他需要编译的子目录
// 或者使用：
//link_directories(库目录)

add_executable(project_demo main.cpp)

target_link_libraries(project_demo lib1) // 链接自定义库文件

//target_link_libraries(project_demo lib2...)

```


链接库需要两部操作，第一步是使用 `add_library` 创建库项目
第二部是用 `target_link_library` 将库链接到主 target 上

对于 library 的头文件，clion 文档更偏向于放入独立的 include 文件夹中，否则就需要在 add_library 的时候加入头文件

lib.cpp -->library --> project


- Reference：
  https://zhuanlan.zhihu.com/p/367805492
  https://blog.hudongdong.com/c/26.html
  https://www.jetbrains.com/help/clion/quick-cmake-tutorial.html#static-libs