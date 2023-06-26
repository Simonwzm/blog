---
title: BeautifulSoup 尝试
date: 2023-06-26 21:06
tags: 
decsription:
cover: https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8A%A8%E6%BC%AB%E7%BB%BC%E5%90%882
---


# BeautifulSoup 尝试

BeautifySoup中的基本对象主要有两种：Tag和beautifySoup对象。

BeautifySoup对象通常的作用是接收文件，比如将html的文本用来构建bsp对象后，才能对其做一定的操作


## tag

Tag就是html文档中的一个标签。除了初始属性之外，tag的属性就是对应html文档中标签的属性，比如class，style属性等等。此外，tag中对属性的引用和修改使用的是python 字典的方法，这点在下图中可窥见一斑：

```python
tag['class'] = 'verybold'
tag['id'] = 1
tag
# <blockquote class="verybold" id="1">Extremely bold</blockquote>

del tag['class']
del tag['id']
tag
# <blockquote>Extremely bold</blockquote>

tag['class']
# KeyError: 'class'
print(tag.get('class'))
# None
```

注意如果是多个属性的话，返回的将是一个属性值的列表。

如果需要取得标签中包括的内容，使用 `tagname.string` 方法，可以获得对应的navigateString类型的数据，接着使用str() 可以成为真正的string类型数据。

> 参考网页：https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

> [!Notice]
> 注意，有些遍历方法返回的是一个tag的列表，此时无法直接对其使用tag的方法。

### 常用的方法

1. 遍历：
    - findAll() ：通过一系列过滤器和标签名找到所有合适的tag，返回tag列表
2. 搜索：
    -  关于子节点/父节点/兄弟节点：
        对于子节点，我们可以使用.children属性得到所有的子节点，.descendent可以返回有递归的子节点，即不是直接的子节点也可以。对于父节点可以使用.parent/.parents属性获得直接父节点/所有父节点。对于兄弟节点，使用.next_sibling(s)/.previous_sibling(s) 可以遍历前后的兄弟节点
    - 使用css选择器：方便，这里不多介绍了
3. 修改：这里不多介绍了，具体见介绍文档，其实也少有用到
> [!NOTICE]
> bsp中的下一个节点不是真的是下一个标签，而有可能是一些换行字符串等等，尤其在兄弟节点的搜索中
> 


## BeautifySoup对象

没有什么非常值得介绍的内容，就是将html转化为bsp类从而处理的一个东西。常用语法：`soup = BeautifulSoup(html_content)`
soup的语法在搜索上与tag是一样的。


## 输入输出编码

仍和输入转为bsp的时候，处理时都会被转成unicode。这个转换相当智能，可以在输入是混合编码时仍有很好的表现。输出的时候默认使用utf-8，但也可以指定方式，如果遇到无法编码的字符，会将其转化为一系列XML特殊字符引用，比如ISO-Latin-1或ASCII,那么在这些编码中SNOWMAN字符会被转换成“&#9731”

> 参考链接：https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id51


#python #Web 
