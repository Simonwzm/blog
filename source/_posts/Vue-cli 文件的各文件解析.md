![[Pasted image 20220322221510.png]]
最近在学习vue，这里做一点笔记。
这是一个vue-cli项目的文件目录
构建的选项是：Bable+Router+Vuex+CSS Pre-procesosr
我们从最上层文件夹开始说起
## 根目录
- node_modules: npm 用来管理node-package 的地方，在`vue create myProject`  之后自动创建了，不需要在意
- public： 知识盲区
- src：源代码所在地，重要，待会讲解
- package.json: 用来注册项目里可能会用到的组件等等，比如 `npm run dev/serve/build` 的脚本就写在里面
- main.js：整个页面的入口，引用了Vue页面应用，并且调用render函数，从而展示初始页面![[Pasted image 20220322223947.png]]

## `src` 文件夹
- assets：用来存放网页上需要用到的图片，在views下的文件中如下使用
```html
<img alt="Vue logo" src="../assets/logo.png">
```
- storex: 和`Vuex`有关，知识盲区
- router：和Vue router有关 [[07 Vue router相关用法]]
- component：存放组件，组件是可以被重复使用的Vue实例，或说可以被重复利用的模板页面元素。但在Vue-cli中就是一个集html，CSS，JavaScript为一体的单页面应用，相比views文件夹中的Vue实例，都是需要发布的页面，component中的组件可以用来构建起这些页面![[06 Vue component使用方法]]
- views：存放的的一个个需要被发布的Vue应用[[08 Vue学习笔记]]

通常，一个vue-cli的启动由main.js开始
`main.js` 中import了 `App.vue`, 因此，首先展示的就是 `App.vue` 的内容
而 `App.Vue` 中的编写方式运用了 `vue rounter`
通过这些方法，vue-cli实现了网页的创建
![[07 Vue router相关用法]]


#Vue  #web 