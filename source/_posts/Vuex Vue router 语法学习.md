---
title: Vuex & Vue router 语法学习
date: 2022-05-22 20:35:22
tags: Vue
---

## Vuex 和 Vue router

### Vuex

Vuex 用来管理网站上的公共数据，比如用户变量属性等等。

- Vuex 结构

    Vuex 中存储了这些不同的对象：
    ```javascript
    export default new Vuex.Store({
        state: {},
        getters: {},
        mutations: {},
        actions: {},
        mudules: {}
    })
    ```

    state 是需要 vuex 保存的状态，所有组件可以通过一些方法得到它
    getter：类似 computed 参数，对 state 里面的变量做一些修改后，产生的新参数。同理，如果一个参数完全依赖于 state 中的一些值

    mutations 里面定义了许多函数，这个函数只允许输入当前的一些 state，输出新的 state，相当于更新了 state
    actions：完成异步的功能

    我们可以这样在组件中使用 Vuex：

1. 获取 state 里的参数：

    `xxx = this.$store.state.var_name`

2. 使用 mutations 里的参数更改 state 里的变量：

    首先在 mutations 里定义一个函数
    ```javascript
    mutations: {
        func1(state) {
            state.var_name ++
            return state
            // 注意不是 returen state.var_name
        }
    }
    ```

    然后在 methods 中调用：
    ```javascript
    methods: {
        my_func() {
            // 调用 mutations 中的 func1 修改 state.var_name
            return this.$store.commit('func1')
        }
    }
    ```

3. 使用 getters 代替 computed

    如下配置 getters：
    ```javascript
    getters: {
        var2(state) {
            return state.var1++
        }
    }
    ```

    在组件里如下引用：
    ```javascript
    computed: {
        myVar2: {
            return this.$store.getters.var2
        }
    }
    ```

4.  使用 actions 更新 state

    actions 会调用 mutations 里面的函数，从而达到改变 state 的方法

    下面展示了如何写 actions
    ```javascript
    actions: {
        action_name(context) {
            // 这里需要填入的是 mutations 里面的对应方法名
            context.commit('func1')
        }
    }
    ```

    接着我们在 methods 中调用它：
    ```javascript
    methods: {
    my_action1() {
        this.$store.dispatch('action_name')
    }
    }
    ```

5.  使用 map 命令调用 Vuex

    为了简化每次重复写 `this.$store.state.var_name` ，我们可以使用如下命令：
    ```javascript
    import {mapState} from 'vuex'
    ...
    computed: {
        ...mapState(['var_name']),
        // {counter: () => this.$store.state.counter}，所以需要使用... 解包
    }
    ```

###  使用 vue router

为了实现动态获得生成的页面，我们可以使用带参数的动态路由

进入 router -> index.js 添加对应页面的路由：
```javascript
import NoteView from '../views/NoteView.vue'
const routes = [
    {},
    {},
    {
        // Vue 里面的 url 需要在最前面写 /，django 则不用

        path: '/xxx/:id',
        name: 'notes',
        component: 'NoteView'
    }
]
```

接着添加对应的页面组件：
```html
//enter src -> views -> 新建 NoteView.vue

<template>
    <div>
        this is note number:{{noteID}}
    </div>
</template>

<script>
    export default: {
        computed: {
            noteID() {
                return this.$route.params.id
            }
        }
    }
```

`this.$route.params` 返回一个对象，包含了关于当前 router 处理的页面的参数。
其中的 `id` 就是我们在 `index.js` 中写的 `:id`

因此，这样实现的效果就是，如果在 url 中输入 /xxxx/...，那么这个页面就会被路由给 NoteView 处理，且可以在这个 view 中，使用 `this.$route.params` 调用 url 中输入了什么

### 关于使用生命周期钩子

我们可以使用 life time hook 在 vue 实例被创建和调用的各个阶段执行不同的命令

如果我们想在网页被载入的立刻就做某件事情，我们可以这样写：
```javascript
export default: {
    created() {
        // 类似 document.createElement('')
        // 它只存在于 js 中，没有被放入 document 数中

        // 我们可以将重要的向后端请求数据的功能写在这个里面


    }
}
```























