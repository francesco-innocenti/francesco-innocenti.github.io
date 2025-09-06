---
title: 'In-Context Learning Demystified?'
date: 2025-08-01
permalink: /posts/2025/08/01/In-Context-Learning-Demystified/
tags:
  - transformers
  - in-context learning
  - large language models
  - implicit gradient descent dynamics


---

>  📖 **TL;DR**: *a transformer block implicitly uses the input context to 
modify its MLP weights.*

Researchers at Google recently published a really cool result [[1]](#1) 
that goes a long way towards understanding the known phenomenon of **in-context 
learning** (ICL) in large language models. The paper is titled [Learning without 
training: the implicit dynamics of in-context learning](https://arxiv.org/abs/2507.16003). 

As first clearly shown by GPT-3 [[2]](#2), ICL is the capability of a model to 
learn to perform a task from examples in its prompt or context without updating 
its parameters—hence *in-context* learning. As an example, I just asked ChatGPT:

> *"if 2+3 = 10 and 4+2 = 12, what is 2+8?"*

The model managed to figure out from a few examples the hidden rule (of doubling 
the result of the sum) and correctly answered "20"—which is quite remarkable. 
This happened at inference time with no parameter updates. How is it possible?

There has been a surge of studies trying to explain ICL. First among these was 
[von Oswald et al. (2023)](https://proceedings.mlr.press/v202/von-oswald23a.html), 
who provided a simple construction where a single linear self-attention layer is 
equivalent to performing gradient descent on some loss, thus showing a form of 
meta-learning. Since then, many papers have generalised and extended these 
results [[4]](#4)[[5]](#5)[[6]](#6). However, as noted by [[1]](#1), most 
theoretical studies have relied on highly simplified models and data settings.

By contrast, [[1]](#1) actually go the opposite way and abstract what they 
see as the key property of context-aware layers such as self-attention. 
Remarkably, they derive a quite general result that for transformers can be 
stated as follows:

> *the next-token prediction of a transformer block with some context $$C$$ and 
query token $$x$$ as input is equivalent to the output of the same transformer 
with only the query as input and weights updated by the context. 
Loosely, this can be written as:*

$$
f_\theta(C, x) = f_{\theta + \Delta \theta(C)}(x)
$$

where $$f_\theta(\cdot)$$ is a transformer block with parameters $$\theta$$. 
This notation is not quite accurate but serves to get the main point across. 
The derivation is remarkably simple.

Said another way, a transformer block can be seen as implicitly using the input 
context to modify its MLP weights. (The statement of the theorem is actually a 
bit more precise and general, so check out the paper for the details.)

The authors derive an explicit formula for the implicit weight update and verify 
their results on some simple problems. They also nicely show that 
building the context token by token defines an implicit gradient descent 
learning dynamics on the MLP weights—which aligns with the intuition that the 
longer the context is, the less the output (or the implicit weight update) 
should change.

The work still has some limitations in that it does not consider the effect of 
multiple blocks or the generation of more than one token at a time, which could 
be interesting research directions.


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
