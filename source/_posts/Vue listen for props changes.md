---
title: Vue watch 语法
date: 2022-05-20 21:09:56
tags: Vue
---
## Vue 监听父组件变化用法 --- Watch 的用法
我们首先要明白实现的一个组件的目的。

如果一个组件只需要父组件向其中初始传入一次值，那么再props里填写需要接受的参数以后，可以直接在template里面使用 `this.name` 直接使用props中接收到的参数使组件运作，前提是 **不更改这个值** ，否则会报错

如果这个组件非常依赖父组件传入的数据工作，那么可能有一些内部的函数需要变动props中的值。如果变动只是为了组件内部的运行，而不需要向父组件发送更改props的数据，我们只需使用本文提到的watch参数就可以，如果需要同步更改父组件的数据，那么需要使用 `emit` 方法，本文暂不讨论。

**Watch 的用法**

watch方法监视了一个参数的变化，如果这个参数变化了，那么就做以下的事情
```js
export default {
	props: {
		prop1: <type1>,
		prop2: <type2>
	},
	data () {
		return {
			example: 'notchange'
		
		}	
	}
	watch: {
		prop1: function(newVal, oldVal) {
			this.example = 'changed'
			//可以干任何事，比如调用methods之类
		}
	}
}
```





