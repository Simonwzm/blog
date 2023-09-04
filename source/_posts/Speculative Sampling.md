---
title: Speculative Sampling 
date: 2023-09-04 15:36
tags: Deep Learning
description: Click in for more details
cover: "https://s2.loli.net/2023/09/04/YGQ7mjtXSIwpMrv.jpg"
---




# Speculative Sampling

**In this article, I aim to reinterpret and rephrase the concepts from a [video](https://www.youtube.com/watch?v=q6oiidmVnwE) that I've recently watched and get inspired. The topic is to explain the term `Speculative Sampling` , a technique in accelerating inference time for LLMs. The original credit should go to [them](https://www.youtube.com/@datasciencecastnet)**

Speculative Sampling is a technique that speeds up autoregressive language model sampling through the use of a smaller 'draft' model. It is often called alternatively as "assisted generation".On some data types this can give a 2x speedup with no loss in accuracy.

## Inefficiency in LLM Inference

We first explain how it speeds up the inference time of large language model.



<div style="display:none">The problem originated from the mathematical principle of autoregressive models. Because the function calculate the probability $p(x_t)$ based on the chain formula for conditional probability, we need to do a brand-new forward pass over all the previous sequence to generate only one token. If we want to generate another token, we need to update the context and do it over again.</div>

<div style="display:none">In inference time of a language model, if I am to generate some tokens after a given context, like "`<context>` I like a" , we expect it to complete in three samplings. </div>

<div style="display:hidden">- The first sampling outputs the probability of the token "I". </div>
<div style="display:hidden">- Due to the principle of autoregressive model, although we just need to add the output token into context, we need to feed the updated context into the model and run from the beginning  to obtain only one output token, or say doing another sampling. The second sampling outputs the probability for "like". 
- Similar to step two, the third sampling output the probability for token "a" which also require a new set of forward pass. </div>

<div style="display:hidden">Therefore we need to iteratively run the large model for 3 times for three new output. </div>

<div style="display:hidden"> But recall the structure of transformer (decoder), the context/previous sequence is actually provided to the transformer at once. Transformers are designed to handle entire sequences simultaneously, and each position in the sequence attends to every other position. It means that the transformer outputs a predicted token for each of the input token. In training, it is convenient to utilize the feature since we already know the label and can compare the result with the label together after the model output. But for inference however, we only expect the last output token as our output, and we need to run again for the next next token prediction. That is not very economical.</div>


Autoregressive models, based on mathematical principles, pose a specific challenge when it comes to inference, especially in the context of language models. This drawback is why sampling in LLMs are expensive.

At the heart of autoregressive models is the chain rule of conditional probability. This means when we're estimating the probability of a token $p(x_t)$, it's contingent on the entire preceding sequence. Thus, for each token we want to generate, a brand-new forward pass over the entire preceding sequence is needed.

For clarity, let's use an example. Suppose we are generating tokens following a given context: "`<context>` I like a". The generation process can be broken down as follows:

1. In the first instance, the model samples and outputs the probability of the token "I".
2. Given the autoregressive nature, to predict the next token, we have to incorporate "I" into the context and restart the forward pass. The model then samples and gives us the probability for "like".
3. Again, following the same logic, to generate the next token "a", the model requires yet another fresh forward pass with the updated context.

So, in this example, we find ourselves invoking the model three times consecutively to generate three new tokens.

However, there's a nuance here. The structure of the Transformer (often used for these tasks), particularly its decoder, is designed to take in the entire sequence or context at once. The reason being, within a Transformer, every position in the input sequence has the capability to "attend" to every other position. Hence, when given a sequence, the Transformer provides a predicted token for each position in that sequence. This feature is beneficial during training because we have the ground truth labels and can easily compare the model's predictions with them.

But during inference, a bottleneck emerges. Typically, we're only interested in the last output token for our generated sequence. But, because of how Transformers work, to get the next token prediction, we need to feed in the entire sequence again and run another forward pass. This iterative approach is not time or computation efficient.

## Speculative Sampling

Now that we understand the crux of the existing problem, we see how speculative sampling cope with this.

Noticing that no matter what we try, we have to undergo the process of inferencing new tokens using iterations, why not use smaller model to do the inference. By using a faster but less accurate model to generate our answer sequence, we get the so-called draft sequence,  it can then serve as something similar to a "ground truth" for training. Specifically, we can use the large model to "examine" this draft sequence just like in a training scenery, because we can input the known draft sequence to the model at the same time. Finally we collect the output from the large model's transformer, and compare it to the draft sequence. If there is a mismatch, we just throw away the subsequent draft sequence. Then assume the small model did everything correctly, we only need to invoke the large model once to generate our answer, at the expense of calling the small model several times. Even if there is a mistake, we can quickly throw away the false result and generate a new one, since the bottleneck is from the large model.

This is actually the rough idea of speculative sampling. Of course there are some implementing details, but the core concept of the problem is show above.

There are some tiny implications in the above logic. To support the above idea, we not only need the small model to be enough fast and enough strong at the same time, we also need the fact that the big model is faster at dealing with long context once, then at iteratively executing several samplings with relatively short context. The former is justified by experiments on code inference or other tasks. The latter, being not very intuitive, relies on the following fact, which is mentioned by [@Karpathy](https://twitter.com/karpathy) in his [blog](https://twitter.com/karpathy/status/1697318534555336961). I quoted the following sentence as the reason to the problem.

 *"This unintuitive fact is because sampling is heavily memory bound: most of the "work" is not doing compute, it is reading in the weights of the transformer from VRAM into on-chip cache for processing"*

Therefore starting a new round of inference which requires reloading weights to cache is more time-consuming, rather than inputting a long context in the Transformer which tends to involve much computation.

This make up for the last piece of the whole picture, I hope the explanation is clear. Again, if you want explanations with a bit of drawings and more intuitive, you can opt for the [video](https://www.youtube.com/watch?v=q6oiidmVnwE)