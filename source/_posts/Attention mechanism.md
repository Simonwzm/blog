---
title: Attention Learning
date: 2023-07-14 15:05
tags: 
decsription:
cover: https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8A%A8%E6%BC%AB%E7%BB%BC%E5%90%882
---


# Attention Mechanism Learning Notes


## Fundamentals for Attention Mechanism

### Vanilla Seq2seq RNNs

In previous lecture, we talk about seq2seq RNN model. 

![image-20230713204347894](https://s2.loli.net/2023/07/13/xgEWa13b5n4iBc8.png)

Specifically, the vanilla version is to transform the output hidden state from the encoder model into two part ($s_0$ and $c$ ) and then send them to the input side of the decoder model.

Typically, the decoder will use $c$ as a context vector and view it as having stored all the information of the encoder model. Thus $c$ is going to be one of the input of all the sliced decoder henceforth. On the other hand $s_0$ will be viewed as the previous hidden state for the decoder RNN. $s_0$ is usually set to zero, and $c$ is usually set to `hout.T`

### Seq2seq with Attention Mechanism

To avoid use a single context vector, we **want the context vector to be generated for each slice of decoder model through the time**. The mechanism to do it is called the attention mechanism.

The principle of attention model is as following:

![498_FA2019_lecture13_230713_212053_1](https://s2.loli.net/2023/07/13/QgK7idFpAolZnHt.jpg)

![498_FA2019_lecture13_230713_212053_2](https://s2.loli.net/2023/07/13/WK3O41GMxvjeXc5.jpg)

![498_FA2019_lecture13_230713_212053_3](https://s2.loli.net/2023/07/13/htgeaJOUDmsAGId.jpg)

![498_FA2019_lecture13_230713_212053_4](https://s2.loli.net/2023/07/13/cBiJT26G5E3fSaC.jpg)

![498_FA2019_lecture13_230713_212053_5](https://s2.loli.net/2023/07/13/DgNiv46U2j7Lpkf.jpg)

> Correction: the result of the output of the FC layer in step 1, denoted as `e` also has a academic name, the `alignment score`. And the process of $s_i$ and $h$ be sent to a FC net like function $f_{att}$ is called the `alignment` operation.

### Image Captioning with RNNs and Attention

![image-20230713213655685](https://s2.loli.net/2023/07/13/fu9ZQKgwOMTE2WX.png)

In this example it is meaningful to look at the shape of the computation.

- The feature grid $[h_{ij}]$ is an output of one layer in the Convolutional Network. So the $h_{ij}$ is a **vector** **with** **length equals to the depth of features** (the number of kernels of the current conv layer, and in all the shape after one conv should be CxHxW, C is the kernel number of this layer). We don't consider batch here currently.
- $e_{tij}$ is a scalar, and so does $a_{tij}$ , which is the attention score/prop of the feature vector $h_{ij}$ at location (i,j) on the feature grid.
- $c_t$ is a vector, a linear combination or weighted sum of vector $h_{ij}$ .
- $s_t$ is a vector, but is the hidden state affiliated to RNN structure. The hidden state is always a vector.

## Attention Layer

### Abstraction into Signs

Given that we can apply attention mechanism to lots of applications, we tend to wrap it up, and make abstractions on it independently so that it can be encapsulated into more applications.

The first thing we need to the is use signature language to express the problem.

The following is the first abstraction.

<img src="https://s2.loli.net/2023/07/13/CD4ROwX1NEKP8Ya.png" alt="image-20230713220831608" style="zoom:50%;" />

Remember that in previous examples, we have a current hidden state in decoder and want to compare it with all the hidden states in the encoder. This process has been abstracted into following:

- The hidden state that initiate the attention process is called a `query vector` q. Given q is from RNN, it should be a vector of shape $D_Q$
- All the hidden state that the query vector q want to compare to is called the input vectors. Given if we have N number of X, we stack them together so that the shape is (N, $D_Q$)
- Before we do similarity comparison to all the X and the q, with function $f_{att}$. Now the function is replaced by `scaled dot product` , the computation is in the illustration above. Note that the scaled constant sqrt($D_Q$) comes from the idea of normalizing the vector better according to their number of dimension. High dimensional vectors tend to have bigger dot product, considering the geometric equation of the dot product.
- The `Softmax` and the `Weighted sum` operation remain the same

### Extent to Multiply Queries

We now extent the query vector into query vector**s**. Meaning the query vectors should be a matrix, with each row representing a query. This extents the scaled dot product to `scaled matrix multiplication` and weighted sum to another `matrix multiplication`, finally the `Softmax` function should still be doing to each query, namely each row of the attention weight matrix `A`, so `Softmax` should be done with `dim=1`.

The detailed extension and shape expression are given as below:

<img src="https://s2.loli.net/2023/07/13/6qCKy38E4WLietk.png" alt="image-20230713222453675" style="zoom:50%;" />

### Add Flexibilities

Notice that we use the input vectors twice, one in comparing similarity (attention scores), another in computing the output vectors.

To add more flexibilities on the input vector, we transform the input vectors X into two types and then sent to two usages. Specifically, key matrix for similarity comparison, and value matrix for output computation. The details are shown in below



<img src="https://s2.loli.net/2023/07/13/PWgMYuUkhvFKXry.png" alt="image-20230713223246133" style="zoom:50%;" />

A clear computational graph may help a lot!

![498_FA2019_lecture13_230714_125135](https://s2.loli.net/2023/07/14/lcMqi4J5QkBWO3Y.jpg)

### Become self-attention

Sometimes there are no queries as input. Instead we want to generate the queries from input vectors $X$, aka the hidden states. That requires another learnable weight matrix. The architecture is as following:

![image-20230714130059243](https://s2.loli.net/2023/07/14/cyxHrTeEVovlwKg.png)

> A common error: $N_Q$ and $N_x$ are different! They differ because Q is processed by multiplying $W_Q$ , previously they are also different, but that comes from queries being another input.
>
> $N_Q$ and $N_x$ are different, which lead to the output `Y `with number $N_Q$ and the only input `X` with number $N_X$ having different numbers. Be careful!
>
> More over, $N_Q$ now is a **hyperparameter**!

The computation is not affected by the permutation of input vectors $X$, the operations are still aligned. This is called the **Permutation Equivariant** . The following shows an example

![image-20230714130349074](https://s2.loli.net/2023/07/14/3yRHe2dniAqETo7.png)

This **can be a drawback**! For example, we want the probability of the period (`.`) to be larger when sentence is long. So we need to add more information on locations to the input (of self-attention layer). One way of this is as the following:

![image-20230714130736270](https://s2.loli.net/2023/07/14/RG2TJsudzIShAyP.png)

### Variants of the Self-Attention Layer

1.  Masked self-attention layer

   Some model requires casualty , the answer to the query should use only information hitherto, like for Q2 we only offer hidden state h1 and h2 (actually their key values K1, K2). A typical application may be translation, and audio understanding, where the input is time aligned from the physical world.

   The computational graph is as following:

   ![image-20230714131909441](https://s2.loli.net/2023/07/14/mpAi6TJF8LUZ2fX.png)

   2. Multi-head self-attention 

      Sometimes we see architectures that divide input in Dx dimension and sent each truncated input to parallel self-attention inputs. Then collect and concatenate the output to form the result matrix Y. The truncated number of chunks (number of heads) and the query dimension generated by input vectors X within each self-attention models are two hyperparameters that we want to tune.

      ![498_FA2019_lecture13_230714_133110](https://s2.loli.net/2023/07/14/D2IMBzLPsFYth86.jpg)

### Attention Model in ConvNet

![498_FA2019_lecture13_230714_135325](https://s2.loli.net/2023/07/14/uOCfz3YsrU5ajxG.jpg)

### Conclusion on (Self-)Attention Model

The attention model solves the problem on tasks that input or output sequences. The essence of understanding sequences is that the generated output should take all the input (or corresponding hidden state) into consideration. We do can use vanilla RNNs . But they are hardly fit for large models. Self-Attention on the other hand fits for this request (a query vector compare to all input vectors), and is also more trainable.



## The Transformer

We designed a new block that encapsulate Self-Attention model and use it do the sequence processing jobs. It is called **the Transformer**.

![image-20230714142542578](https://s2.loli.net/2023/07/14/S8IJVkxfdWnFoRc.png)

Hyperparameters: number of transformer blocks, output dimension of each block: $N_Q$ (also named in `query depth`, normally the same for each transformers) and heads(if we use the multi-head self-attention model)

The final structure is simply multiple cascaded transformers, as shown below:

![image-20230714150303011](https://s2.loli.net/2023/07/14/XODv1KbIV3ecHpC.png)

As the title of the paper inventing transformer, attention (by transformers) is all you need.
