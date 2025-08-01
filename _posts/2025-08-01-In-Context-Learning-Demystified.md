---
title: 'In-Context Learning Demystified'
date: 2025-08-01
permalink: /posts/2025/08/01/In-Context-Learning-Demystified/
tags:
  - 

---

>  📖 **TL;DR**: *the output of a transformer taking some context and query 
token as input is equivalent to the output of the same transformer taking only 
the query as input and updated weights depending on the context.*

Researchers at Google recently published a really cool result [[1]](#1) 
that goes a long way towards understanding the popular phenomenon of **in-context 
learning** (ICL) in large language models. The paper is titled [Learning without 
training: the implicit dynamics of in-context learning](https://arxiv.org/abs/2507.16003). 

As first clearly shown by GPT-3 [[2]](#2), ICL is the capability of a language 
model to learn to perform a task from examples in its prompt or context without 
updating its parameters—hence *in-context** learning. As an example, I just 
asked ChatGPT:

> *"if 2+3 = 10 and 4+2 = 12, what is 2+8?"*

It is unlikely (though possible) that this task was not part of the pretraining 
data and yet ChatGPT figured out from just the 2 examples given the hidden rule 
of doubling the result of the sum and correctly answered "20"—which is quite 
remarkable. This happened at inference time with no parameter updates. How is 
it possible?

There has been a surge of studies trying to explain this phenomenon. First 
among these was [von Oswald et al. (2023)](https://proceedings.mlr.press/v202/von-oswald23a.html), who provided a simple construction where a single linear self-attention 
layer is equivalent to performing gradient descent on some loss, thus showing a 
form of meta-learning. Since then, many papers have generalised and extended 
these results [[4]](#4)[[5]](#5)[[6]](#6). However, as noted by [[1]](#1), most 
theoretical studies significantly simplify the model, employing toy 
reparameterisations of self-attention, for example without softmax.

By contrast, [[1]](#1) actually go the opposite way and abstract away what they 
see as the key property in context-aware layers such as attention. Remarkably, 
they derive a very general result that for transformers can be stated as 
follows:

> *the output of a transformer taking some context $C$ and query token $x$ as 
input is equivalent to the output of the same transformer taking only the query 
as input and updated weights depending on the context. Mathematically, this can 
be written as:*

$$
f_W(C, x) = f_{W + \Delta W(C)}(x)
$$

where $$f_W$$ is the network function with parameters $$\theta$$ (omitted for 
simplicity) that includes an MLP with weights $$W$$. This notation is not quite 
accurate but serves to get the main point across. The derivation is remarkably 
simple and quite elegant in my opinion.

Said another way, inputting a query along with some context to a transformer 
turns out to be the same as inputting only the query to the same transformer 
with updated MLP weights, where the update depends on the context. The statement 
of the theorem is actually a bit more precise and general, so check out the 
paper for the details.

The authors further derive an explicit formula for the implicit weight update 
and verify their results on some toy tasks. They also nicely show that building 
the context token by token defines an implicit gradient descent learning 
dynamics on the MLP weights. This aligns with the intuition that the more tokens 
you feed into the context, the less the output (or implicit weight update) 
should change.

The work still has some limitations in that it does not consider the effect of 
multiple blocks, nor the generation of more than one token. These are 
interesting research directions, although to my mind the result provides a 
strong explanation for ICL.


## References

<p> <font size="3"> <a id="1">[1]</a> 
Dherin, B., Munn, M., Mazzawi, H., Wunder, M., & Gonzalvo, J. (2025). Learning without training: The implicit dynamics of in-context learning. arXiv preprint <i>arXiv:2507.16003.</i> </font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. <i>Advances in neural information processing systems, 33</i>, 1877-1901.</font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Von Oswald, J., Niklasson, E., Randazzo, E., Sacramento, J., Mordvintsev, A., Zhmoginov, A., & Vladymyrov, M. (2023, July). Transformers learn in-context by gradient descent. In <i>International Conference on Machine Learning</i> (pp. 35151-35174). PMLR.</font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Ahn, K., Cheng, X., Daneshmand, H., & Sra, S. (2023). Transformers learn to implement preconditioned gradient descent for in-context learning. <i>Advances in Neural Information Processing Systems, 36</i>, 45614-45650.</font> </p>

<p> <font size="3"> <a id="5">[5]</a> 
Zhang, Y., Singh, A. K., Latham, P. E., & Saxe, A. (2025). Training dynamics of in-context learning in linear attention. <i>arXiv preprint arXiv:2501.16265.</i> </font> </p>

<p> <font size="3"> <a id="6">[6]</a> 
He, J., Pan, X., Chen, S., & Yang, Z. (2025). In-context linear regression demystified: Training dynamics and mechanistic interpretability of multi-head softmax attention. <i>arXiv preprint arXiv:2503.12734.</i> </font> </p>
