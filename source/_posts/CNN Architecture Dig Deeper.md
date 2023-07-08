---
title: CNN Architecture Dig Deeper
date: 2023-07-08 16:09
tags: 
decsription:
cover: https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8A%A8%E6%BC%AB%E7%BB%BC%E5%90%882
---

# CNN Architecture Dig Deeper

## Analogy to the fully connected layer and a single neuron


![image-20230708141355727](https://s2.loli.net/2023/07/08/LTd3aOkxEieXwHl.png)



## Convolution Layers

### Dimensional description of CNN



![image-20230708141516780](https://s2.loli.net/2023/07/08/9F37ATuX2esMcvn.png)

 :warning: Notice that we have a batch number of N in practice. So the input is usually of 4-dim.

### Stacking of layers 

Conv + ReLU connects the layers together

<img src="https://s2.loli.net/2023/07/08/DnWIsxASKYiJch6.png" alt="image-20230708142026177" style="zoom: 50%;" />

### Receptive Fields

For convolution layers, each kernels allow us to see a particular local feature with size in the input equals to the kernels size. So a 3x3 kernel can only see the feature of the local feature with size 3x3 on the original input. 

But as we stack convolutional layers together, the complexation helps local features contains richer information, and till one day, the local feature in a deep layer convolution layer will see the feature information from the whole original input picture.

The detailed formular of how the receptive fields grown is given below, as well as its growth visualization

![image-20230708142820894](https://s2.loli.net/2023/07/08/AUTVZymFO1RCHlq.png)

Therefore we get an intuition: bigger receptive fields == deeper network , which is not a health way of improvement. We can use down sampling to shrink the image size namely increase the density of each new outputs' reception field (imagine we output a 1x1 pixel immediately, then its receptive field instantly reaches full picture. But that is not a multi classifier meant to do)

This is **one way** of thinking why we need down-sampling layer, and we dig deeper into it later.

### Common Patterns

![image-20230708144606159](https://s2.loli.net/2023/07/08/tkHquGfYolSbJ2m.png)

Cheat sheets!



## Down Sampling Layer

We introduce max pooling layer and 1x1 convolution layer here. Here is the brief introduction:

![image-20230708143929603](https://s2.loli.net/2023/07/08/vr25S9WHcEgezyk.png)

### 1x1 Conv Layer

Apart from the description above, an interesting perspective on 1x1 Conv Layer is that it is actually **like a fully connected layer operating on the depth dimension**.

Each filter is like a class or column vector of matrix W in FC layers. And the number of filters correspond to the number of W's columns. Then each filter operates on the input picture independently, just like W's columns multiply input matrix X independently in columns.

Therefore we can actually build FC networks inside CNN architectures. We can stack 1x1 layer + ReLU Layer several times which acts like a FC networks.

**But still 1x1 conv layer is more used in down sampling and adapting the number of depth channel**. 

### Pooling Layers

The method of pooling is not restricted to max pooling, but the general pattern should be same, like we operate on a single feature slice in depth once at a time, and we downsize the length/height of the picture by pooling function, and like stride equals kernel size.

![image-20230708145502755](https://s2.loli.net/2023/07/08/A1csWbUfqPjiXOV.png)

![image-20230708145608327](https://s2.loli.net/2023/07/08/GNgqvlfeamB1wFd.png)

 

## Sandwiching them!

Conv + Pooling + ReLU is very often used, but deep network is very hard to train!  We need normalization to help convergence and help train a deeper network.



## Batch Normalization (BN Layer)

General idea: control each layer output to be of zero mean and 1 variance. 

### BN over FC layers

About how batch normalization function in FC layers. We just perform BN along each feature across all batch dimension.

- Normalization across the batch

  ![image-20230708150343277](https://s2.loli.net/2023/07/08/cvQDLfWS3qz6jHd.png)

- Learning the shift and bias

  ![image-20230708150724671](https://s2.loli.net/2023/07/08/qrxjRKuFo9OYCLB.png)

- Recover sample independence in test time.

  **At training time, we do running sum over all $\mu$ and $\sigma$ for each train.** The difference is that in test time, the batch dimension vanishes, and if we had done something that relies on the batch dimension in training time, it creates a difference between them. In BN we just do a similar way without using batch dimension in test time,  which is the starting sentence of this block.

### BN over conv layers

![image-20230708151308659](https://s2.loli.net/2023/07/08/uHxw48DIPXF97bV.png)

In conv layer, the $\mu$ and $\sigma$ are now vectors of length equals to depth, which is similar to what a bias vector look like!

We can also say, for each depth dim, we consider all pixels in height, length, and across all pictures in a batch to compute the $\mu$ and $\sigma$ .

### *Layer Normalization

To deal with the incompatibility during test time and training time, we normalize over feature dimension,(for each sample in batch, we consider every pixels in length, height, and channels)

This is common in Recurrent Neuron Network and Transformers.

### *Instance Normalization

Similarly, we just do normalization on only length and height dimension namely for each sample in batch and for each channel(feature) in a sample we do sone normalization.

![image-20230708152535806](https://s2.loli.net/2023/07/08/H9mcMpjSPnLebt5.png)

