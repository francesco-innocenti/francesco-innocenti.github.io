---
title: '♾️ Infinite Widths Part III: The Maximal Update Parameterisation ($$\mu$$P)'
date: 2025-04-09
permalink: /posts/2025/04/09/Infinite-Widths-Part-III-The-Maximal-Update-Parameterisation/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Neural Tangent Kernel
  - Maximal Update Parameterisation
  - Hyperparameter Transfer
  - Tensor Programs
  - Rich Regime
  - Feature Learning
  - Dynamical Mean Field Theory

---

This is the third and last post of a short series on the infinite-width limits 
of deep neural networks (DNNs). In [the first post](https://francesco-innocenti.github.io/posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/), 
we showed that the output of a random network becomes Gaussian distributed in 
the infinite-width limit. [The second post](https://francesco-innocenti.github.io/posts/2025/02/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/) 
went beyond initialisation and showed that infinitely wide nets trained with GD
are basically kernel methods.

We also saw that the main limitation of this kernel (NTK) regime is that the 
weights and so the layer activations barely move during training [[1]](#1)[[2]](#2). 
This fails to capture the behaviour of practical, finite-width networks and 
results in worse generalisation performance.

Here, we review the Maximal Update Parameterisation ($$\mu$$P) [[3]](#3), a 
developing and much more influential parameterisation of DNNs that effectively 
puts feature learning back into the infinite-width limit.

I think $$\mu$$P is amazing. It's only a slight overstatement to say that $$\mu$$P 
is the only theory that has had a major impact on practice: many frontier AI labs 
including OpenAI, xAI and Apple (and probably others too) make use of it. Of 
course, $$\mu$$P built itself on previous theoretical advances including the NTK, 
the theory of signal propagation in DNNs, and mean-field theories, among others.  


## TL;DR
> **The Maximal Update Parameterisation**: roughly, $$\mu$$P and its extensions 
> are a prescription for how to common knobs of DNNs (such the initialisation 
> and the learning rate) such that the order of the feature or activation 
> updates at each layer does not vary with the network size (e.g. width and 
> depth) while changing as much possible (maximal feature learning).

$$\mu$$P allows not only for more stable training dynamics but also for zero-shot 
hyperparameter transfer [[4]](#4)[[9]](#9), meaning that you can tune a small model 
and transfer optimal hyperparameters such as the learning rate to bigger 
(wider and/or deeper) models. This provides major efficiency gains at large 
scale as first shown by [[4]](#4)[[9]](#9). 


## $$\mu$$P
Motivated by the lack of feature learning in the NTK or "lazy" regime, [[3]](#3)
introduced $$\mu$$P as a parameterisation that essentially allows for as much
feature learning as possible in the infinite-width limit. The parameterisation 
is maximal (hence $$\mu$$P) in this sense. By as much as possible, we mean that
we allow the features or activations at each layer to change as much as possible
without blowing up with the width $$N$$. In the NTK, the features evolve in 
$$\mathcal{O}(N^{-1/2})$$ and so remain practically unchanged during training at 
large width. In $$\mu$$P, the features instead change at $$\mathcal{O}_N(1)$$.

More formally, $$\mu$$P can be derived from the following 3 desiderata:
* the layer preactivations are $$\mathcal{O}_N(1)$$ at initialisation;
* the network predictions are $$\mathcal{O}_N(1)$$ during training; and
* the layer features also evolve in $$\mathcal{O}_N(1)$$ during training.
These are seen desiderata because they are not strict necessary or sufficient 
conditions but rather things that we would like DNNs to have to ensure more
stable training dynamics at different scales and, as we will see, transfer of
hyperparameters.

Satisfying these desiderata boils down to solving a system of a equations for a
set of scalars (commonly referred to as "abcd") parameterising the layer 
transformation, the (Gaussian) initialisation variance, and the learning rate [[5]](#5)[[6]](#6).
I highly recommend [these lecture notes](https://mlschool.princeton.edu/sites/g/files/toruqf5946/files/documents/Princeton___Lecture_Notes_0.pdf) for step-by-step derivations. 
Different optimisers (e.g. SGD vs Adam) and types of layer (e.g. fully connected 
vs convolutional) lead to different "abcd" scalings. One version of $$\mu$$P 
rescales each layer by $$1/\sqrt{\mathtt{fan\_in}}$$ except for the output which 
is scaled by $$1/\mathtt{fan\_in}$$. If you read [Part II](https://francesco-innocenti.github.io/posts/2025/02/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/) of this 
series, you might recall that this is very similar to the NTK parameterisation. 
The only difference---which turns out to be critical---is the output scaling. 
This is what allows the feature to change in the infinite-width limit. [[3]](#3)
also showed that while in the standard parameterisation (SP) of DNNs (based on 
He and related initialisation) the features do evolve, the output diverges with 
the width.

Remarkably, [[4]](#4) showed that many optimal hyperparameters in $$\mu$$P also 
remain stable as the model size changes. This unlocks zero-shot hyperparameter 
transfer, meaning that one can tune a small model and then use the optimal 
hyperparameters such as the learning rate to train a bigger model, avoiding the 
expensive tuning at large scale.


## Depth-$$\mu$$P
Excitingly, $$\mu$$P has recently been extended to depth for ResNets (Depth-$$\mu$$P) 
[[7]](#7)[[8]](#8), such that stable training dynamics and transfer are also 
conserved independent of the network depth $$L$$ [[9]](#9). This is done mainly by 
scaling each residual block by $$1/sqrt{L}$$. This was enabled by the 
commutativity of the infinite-width and infinite-depth limit of ResNets [[10]](#10)[[11]](#11).
We note, however, that it is not entirely clear whether this is the optimal scaling 
for depth (cf. [[7]](#7)[[8]](#8)[[16]](#16)).


## Other extensions
Standard (width-only) $$\mu$$P has also been extended to some local algorithms [[12]](#12), 
sparse networks [[13]](#13), second-order methods [[14]](#14), and 
sharpness-aware minimisation [[15]](#15).


## Other resources
Besides the references below, I found the following material useful in understanding $$\mu$$P:
* Microsoft's [blog post](https://www.microsoft.com/en-us/research/blog/on-infinitely-wide-neural-networks-that-exhibit-feature-learning/) introducing $$\mu$$P;
* [this conversation](https://www.youtube.com/watch?v=1aXOXHA7Jcw&t=2723s&ab_channel=TimothyNguyen) with Greg Yang focused on Tensor Programs;
* Microsoft's [blog post on the hyperparameter transfer results](https://www.microsoft.com/en-us/research/blog/%C2%B5transfer-a-technique-for-hyperparameter-tuning-of-enormous-neural-networks/); and
* the [`mup` github repo](https://github.com/microsoft/mup?tab=readme-ov-file#coord-check) (PyTorch).

For other reviews of $$\mu$$P, see:
* [this post](https://blog.speechmatics.com/mup) by Speechmatics, and
* [this post](https://cerebras.ai/blog/the-practitioners-guide-to-the-maximal-update-parameterization) by Cerebras.

See also:
* [`nanoGPT-mup` github repo](https://github.com/EleutherAI/nanoGPT-mup?tab=readme-ov-file) (PyTorch)


## References

<p> <font size="3"> <a id="1">[1]</a> 
Chizat, L., Oyallon, E., & Bach, F. (2019). On lazy training in differentiable programming. <i>Advances in neural 
information processing systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Lee, J., Xiao, L., Schoenholz, S., Bahri, Y., Novak, R., Sohl-Dickstein, J., & Pennington, J. (2019). Wide neural 
networks of any depth evolve as linear models under gradient descent. <i>Advances in neural information processing 
systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Yang, G., & Hu, E. J. (2021). Tensor programs iv: Feature learning in infinite-width neural networks. 
In <i>International Conference on Machine Learning</i> (pp. 11727-11737). PMLR.</font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Yang, G., Hu, E., Babuschkin, I., Sidor, S., Liu, X., Farhi, D., ... & Gao, J. (2021). 
Tuning large neural networks via zero-shot hyperparameter transfer. 
Advances in Neural Information Processing Systems, 34</i>, 17084-17097.</font> </p>

<p> <font size="3"> <a id="5">[5]</a> 
Pehlevan, C., & Bordelon, B. (2023). Lecture Notes on Infinite-Width Limits of Neural Networks.</font> </p>

<p> <font size="3"> <a id="6">[6]</a> 
Yang, G., & Littwin, E. (2023). Tensor programs ivb: Adaptive optimization in the infinite-width limit. <i>arXiv preprint arXiv:2308.01814.</i> </font> </p>

<p> <font size="3"> <a id="7">[7]</a> 
Yang, G., Yu, D., Zhu, C., & Hayou, S. (2023). Tensor programs vi: Feature learning in infinite-depth neural networks. <i>arXiv preprint arXiv:2310.02244.</i> </font> </p>

<p> <font size="3"> <a id="8">[8]</a> 
Bordelon, B., Noci, L., Li, M. B., Hanin, B., & Pehlevan, C. (2023). Depthwise hyperparameter transfer in residual networks: Dynamics and scaling limit. <i>arXiv preprint arXiv:2309.16620.</i> </font> </p>

<p> <font size="3"> <a id="9">[9]</a> 
Noci, L., Meterez, A., Hofmann, T., & Orvieto, A. (2024). Super consistency of neural network landscapes and learning rate transfer. <i>Advances in Neural Information Processing Systems, 37</i>, 102696-102743.</font> </p>

<p> <font size="3"> <a id="10">[10]</a> 
Hayou, S. (2024). Commutative Scaling of Width and Depth in Deep Neural Networks. <i>Journal of Machine Learning Research, 25</i>(299), 1-41.</font> </p>

<p> <font size="3"> <a id="11">[11]</a> 
Hayou, S., & Yang, G. (2023, July). Width and depth limits commute in residual networks. In <i>International Conference on Machine Learning</i> (pp. 12700-12723). PMLR.</font> </p>

<p> <font size="3"> <a id="12">[12]</a> 
Ishikawa, S., Yokota, R., & Karakida, R. (2024). Local Loss Optimization in the Infinite Width: Stable Parameterization of Predictive Coding Networks and Target Propagation. <i>arXiv preprint arXiv:2411.02001.</i> </font> </p>

<p> <font size="3"> <a id="13">[13]</a> 
Dey, N., Bergsma, S., & Hestness, J. (2024). Sparse maximal update parameterization: A holistic approach to sparse training dynamics. <i>arXiv preprint arXiv:2405.15743.</i> </font> </p>

<p> <font size="3"> <a id="14">[14]</a> 
Ishikawa, S., & Karakida, R. (2023). On the parameterization of second-order optimization effective towards the infinite width. <i>arXiv preprint arXiv:2312.12226.</i> </font> </p>

<p> <font size="3"> <a id="15">[15]</a> 
Haas, M., Xu, J., Cevher, V., & Vankadara, L. C. Effective Sharpness Aware Minimization Requires Layerwise Perturbation Scaling. In <i>High-dimensional Learning Dynamics 2024: The Emergence of Structure and Reasoning.</i> </font> </p>

<p> <font size="3"> <a id="16">[16]</a> 
Dey, N., Zhang, B. C., Noci, L., Li, M., Bordelon, B., Bergsma, S., ... & Hestness, J. (2025). Don't be lazy: CompleteP enables compute-efficient deep transformers. <i>arXiv preprint arXiv:2505.01618.</i> </font> </p>