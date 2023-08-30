---
title: 记花了一天时间和￥150获得一个google voice
date: 2022-08-07 11:59
tags: 
decsription:
cover: "https://s2.loli.net/2022/08/07/LKI8qMUpcaGWud1.png"
---

# 记花了一天时间和￥150获得一个google voice

Google voice 是google提供的虚拟美国电话号码服务。使用gv号码可以用来接受国外sms，电话，或者注册一些应用等等。

然而正式应为gv的应用广泛，其出现了一定的滥用现象，以及由于国际局势今后在哪个，导致google于今年收紧了gv的注册和保号流程。这使得我第一次尝试注册gv的过程非常艰难。

下面为自己记录一下这次经历，最后做一定的总结

{% mermaid %}
flowchart TB
	A(Register Google Voice number) -- need USA local phone number for verification --> B(free phone numbers from apps)
	B -- failed: user disabled --> C(sms receiving service providers)
	C -- failed: virtual phone does not support verification--> D(paid phone number from other apps)
	D -- failed: no available payment methods in google play --> E(paid sms receiving service provider)
	E -- failed --> A
	A -- buy a second-hand number --> F(TG groups)
	F --> G(Success)
{% endmermaid %}

总结一下，目前的 GV 注册，如果没有一个美国实体电话卡会非常艰难。
其中，免费电话号app应该都被封禁了，sms代收服务商在gv服务上是不可行的（但是用来验证其他的账号是真的有用，已经搞了一个TG的英国号了（公共虚拟电话号，不是很安全，所以不会做大用处），付费电话号，由于通常收费方式是通过google play，又因为gp的付款方式中，礼品卡只有美国原生ip可以充值（翻墙无用），银行卡不支持银联，且paypal只有美区可用，所以我没办法通过gp进行充值。最终，得到的方法只有买现成的号。然而tb卖号的店铺估计最近被全面封禁，找不到任何一家相关的店铺。最终前往TG买号，使用bot操作非常便利。TG还是厉害啊。

最终花费计算：35（gp礼品卡）+35（[付费sms service provider](https://sms-man.com/)) + 70（TG购买费用）+10（杂项）

最终时间：1天

如果一开始就买号的话，省时又省力。唉，这该死的好胜心。

小收获：

- 验证码代收平台：<https://sms-man.com/>， <https://user.verifywithsms.com>
- 检查代理的伪装程度：<https://whoer.net/>
- 证件伪装： tompsd （暂未了解清楚）
- 美区Paypal注册：<https://www.bacaoo.com/info/16955>
- 一个技术社区：<https://www.v2ex.com/>
- ifttt：一个android自动化软件（暂未了解清楚）
- 关于clash的udp代理：<https://ocguide.eyw015.com/quest-guide/basic-net#ru-he-zhi-dao-xian-lu-shi-fou-zhi-chi-udp>
- 币种管理网站：Payeer，perfect money ... （需要验证，非常麻烦）






