# PPT Review Report

[toc]

This review report is about several topics proposed by Prof.Mengwei Xu

Several inquisitive points are mentioned.

## MobileFM

The author believes that today mobile NPUs are only optimized for a few models despite their high efficiency. Models still contain a lot of tensors that cannot be accelerated by NPUs. Therefore speedup on some models are comparatively small.

The following graph 

![image-20230906001512053](https://s2.loli.net/2023/09/06/Fbakq3IluGhsUKe.png)This graph shows that, first, NPU update only affect a few models. Second, NPUs are indeed helpful. Third, NPUs are indeed economical.



![image-20230906001839631](https://s2.loli.net/2023/09/06/KdEisagJPbDVle9.png)

The second illustration demonstrate that there are still many tensors in the model that cannot be optimized by NPU. And it also shows that those not fit for NPU are considerably slower than those can fit (or partially fit) the NPU.

The author then proposed their idea, which is to build a mobile foundation model (Mobile FM) that serves all mobile tasks, and can be better optimized by the mobile platform.

## FedFwd

![image-20230906004520820](https://s2.loli.net/2023/09/06/oyYThq2DmenSrsU.png)

The author proposed that backprop is very expensive in FL, because it requires huge memory footprints, NPU unfriendly operators and low client scalability. The above illustration is a brief instance of the simple neural network. From the calculation procedure we see that the neural network use the tanh nonlinearity. And it uses the Mean Squared Error (MSE). The way we can inference this from the illustration is recorded [here](https://chat.openai.com/share/4bc55501-d63f-4ee9-ad19-086694398415)

The author mentioned the potential to use forward gradient to accelerate the backprop of LLMs. Simply speaking, we can compute the numerical gradient to substitute calculating the analytical gradient from backprop. Typically, the numerical gradient can be calculated by $\frac{f(x+\Delta x) - f(x)}{\Delta x}$ to approximate the accurate gradient. 

![image-20230906004231249](https://s2.loli.net/2023/09/06/wn3i2BIOeDZmVso.png)

The above illustrate in a high dimension target function, how can we calculate the forward gradient and use empirical mean to average out and get more close to the true gradient. The explanation of the above illustration is [here](https://chat.openai.com/share/74c3b42c-d692-4bc9-a28c-5413d5da6259)

However, the cost of computing forward gradient also raise with the increase of model's trainable parameter size.

Therefore, the author propose FedFwd, which is a method delivers speedup in forward gradient computation leveraging NPU and more clients.

## EdgeMoE

In the original transformer model, we use several Multi-perceptron Layer or the feed-forward layer  between the classification linear network and the output of self-attention layer.

These layers do increase the model capacity, but they are bulky to train. The more complicated the downstream tasks are, the more complicated the model will have to be trained, and the feed forward layer may grow be denser and require to be larger for more performance.

We can use a structure called MoE to improve this architecture. Instead using one MLP as FFN, we use a structure called Mixture of Experts. While experts are like smaller size MLP layers, they may perform well if trained on more specific and relatively easier tasks. If we can build a router that relay the output of the attention layer to a certain expert layer that is trained on and specialized in this task, then we can achieve equal performance and replace a bulky MLP FFN with several small specialized Experts. 

The reason why it suits the mobile platform is introduced in the PPT

![image-20230906135649456](https://s2.loli.net/2023/09/06/sQ4VtmZKDpFb1vW.png)

The right illustration describes the preload strategy of the EdgeMoE model. A detailed version is given below

![image-20230906135839163](https://s2.loli.net/2023/09/06/Q7Iy1TWBRdE4aAm.png)

