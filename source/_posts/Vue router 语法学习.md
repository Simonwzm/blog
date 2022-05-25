---
title: Vue router 语法学习
date: 2022-05-20 21:05:56
tags: Vue
---

## Vue router 路由语法

### router-view
在 `main.js` 中与 Vue 实例绑定的 `<div id="app">` 中，使用 `router-view` 展示页面元素

`router-view` 可以使页面跳转到其他页面的时候，不会全部刷新，而是替换 `<router-view>`  中的内容，例如如下的 `App.vue` 中，
```vue
<template>
  <div id="app">
    <nav>
      <router-link to="/auth/login">Login</router-link> |
      <router-link to="/auth/register">register</router-link>

    </nav>
    <router-view/>
  </div>
</template>
```
（style 和 script 省略，如果有的话）

### nav 节点

<nav/> 节点用于生成一个导航条
其下的 <router-view/> 节点，根据所在页面的地址，根据 router 文件夹下 `index.js` 中的配置，返回相应的页面（应当为 views 文件中的 `.vue` 文件）

### Vue router 的配置

再看到 router 文件夹下的 `index.js` 文件：
```JavaScript
import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/auth/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/auth/login',
    name: 'login',
    component: LoginView,
  }
]

const router = new VueRouter({
  routes
})

export default router

```

可以看到，`index.js` 首先 import 需要其路由的页面
随后在 `route` 数组常量中，创建需要路由页面的对象

对象中的数据分别有：
- name，不知道
- path：对应网页的相对地址
- component：对应网页所用的 `.vue` 应用

最后，router 就可以根据 `<router-link to=""></router-link> | <router-link to="">xxx</router-link>` 提供的相对地址无需刷新地返回另外的页面

** 注意，router 返回的页面都是在 `<router-view/>` 节点出展示的 **

#Vue  #Web