---
title: '♾️ Infinite Widths (& Depths) Part III: The Maximal Update Parameterisation ($$\mu$$P)'
date: 2025-04-09
permalink: /posts/2025/04/09/Infinite-Widths-&-Depths-Part-III-The-Maximal-Update-Parameterisation/
tags:
  - deep neural networks
  - infinite width limit
  - neural tangent kernel
  - maximal update parameterisation
  - mup
  - hyperparameter transfer
  - tensor programs
  - rich regime
  - feature learning
  - dynamical mean field theory
  - optimisation theory

---

This is the third and last post of a short series on the infinite-width limits 
of deep neural networks (DNNs). In [Part I](https://francesco-innocenti.github.io/posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/), we showed that the output of a random network becomes Gaussian distributed in 
the infinite-width limit. [Part II](https://francesco-innocenti.github.io/posts/2025/02/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/) 
went beyond initialisation and showed that infinitely wide nets trained with GD
are basically kernel methods.

We also saw that the main limitation of this kernel (NTK) regime is that the 
weights and so the layer preactivations barely move during training at large width [[1]](#1)[[2]](#2). 
This fails to capture the behaviour of practical, finite-width networks and 
results in worse generalisation performance.

Here, we review the Maximal Update Parameterisation ($$\mu$$P) [[3]](#3), a 
rapidly developing and much more influential parameterisation of DNNs that 
effectively puts feature learning back into the infinite-width limit. I am 
grateful to [Alexandru Meterez](https://scholar.google.com/citations?user=wSrCMa4AAAAJ&hl=en&oi=ao) 
for helping me understand $$\mu$$P much more quickly than I would have on my own.


## TL;DR
> **The Maximal Update Parameterisation**: roughly, $$\mu$$P and its extensions 
> are a prescription for how to scale a model such that the order of the feature 
> updates at each layer does not vary with the model size (e.g. width and depth).

Under $$\mu$$P, it turns that what you don't only get more stable training 
dynamics, but also stable hyperparameters, meaning that optimal hyperparameters
will be conserved across different model sizes. This unlocks *zero-shot 
hyperparameter transfer* [[4]](#4)[[9]](#9), meaning that you can tune a small 
model and transfer optimal hyperparameters such as the learning rate to bigger 
(wider and/or deeper) models, resulting in major efficiencies at large scale.


## $$\mu$$P
Motivated by the lack of feature learning in the NTK or "lazy" regime, [[3]](#3)
introduced $$\mu$$P as a parameterisation that essentially allows for as much
feature learning as possible in the infinite-width limit. By as much as possible, 
it is meant that we allow the features or preactivations at each layer to change as 
much as possible without blowing up with the width $$N$$. The parameterisation 
is maximal (hence $$\mu$$P) in this sense. More specifically, in the NTK the 
features evolve in $$\mathcal{O}(N^{-1/2})$$ time and so remain practically 
unchanged during training at large width. In $$\mu$$P, the features updates are 
instead of order $$\mathcal{O}_N(1)$$.

More formally, $$\mu$$P can be derived from the following 3 desiderata:
* the layer preactivations are $$\mathcal{O}_N(1)$$ at initialisation;
* the network predictions are $$\mathcal{O}_N(1)$$ during training; and
* the layer features also evolve in $$\mathcal{O}_N(1)$$ during training.

These are seen desiderata because they are not strict necessary or sufficient 
conditions but rather things that we would like DNNs to have to ensure more
stable training dynamics and, as it turns out, hyperparameters at different scales.

Satisfying these desiderata boils down to solving a system of equations for a
set of scalars (commonly referred to as "abcd") parameterising the layer 
transformation, the (Gaussian) initialisation variance, and the learning rate [[5]](#5)[[6]](#6).
Different optimisers (e.g. SGD vs Adam) and types of layer (e.g. fully connected 
vs convolutional) lead to different "abcd" scalings. One version of $$\mu$$P 
rescales each layer by $$1/\sqrt{\mathtt{fan\_in}}$$ except for the output which 
is scaled by $$1/N$$. If you read [Part II](https://francesco-innocenti.github.io/posts/2025/02/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/) 
of this series, you might notice that this scaling recipe is very similar to the 
NTK parameterisation. The only difference lies in the output scaling, which 
turns out to be critical and is what allows the features to change in the 
infinite-width limit. [[3]](#3) also showed that while in the standard 
parameterisation (SP) of DNNs (based on He and similar initialisations) the 
features do evolve, the output diverges with the width.

Remarkably, [[4]](#4) showed that in $$\mu$$P many optimal hyperparameters also 
remain stable as the width changes. As noted above, this means that you can tune 
a small model and then use the optimal hyperparameters such as the learning rate 
to train a bigger (i.e. wider) model, avoiding the expensive tuning at large 
scale.


## Extensions
Standard (width-only) $$\mu$$P has been extended to some local algorithms [[12]](#12), 
sparse networks [[13]](#13), second-order methods [[14]](#14), and 
sharpness-aware minimisation [[15]](#15).

Excitingly, $$\mu$$P has also been extended to depth for ResNets ("Depth-$$\mu$$P") 
[[7]](#7)[[8]](#8), such that stable training dynamics and transfer are also 
conserved independent of the network depth $$L$$ [[9]](#9). This is done mainly by 
scaling each residual block by $$1/\sqrt{L}$$ and is enabled by the commutativity 
of the infinite-width and infinite-depth limit of ResNets [[10]](#10)[[11]](#11). 

Recently, I found that using Depth-$$\mu$$P for a local algorithm called predictive
coding allowed, for the first time, stable training of 100+ layer networks [[16]](#16). 
See the [paper](https://arxiv.org/abs/2505.13124) and 
[blog post](https://francesco-innocenti.github.io/posts/2025/05/20/Scaling-Predictive-Coding-to-100+-Layer-Networks/) 
for more.


## Concluding thoughts
I think $$\mu$$P is amazing. It's only a slight overstatement to say that $$\mu$$P 
is the only theory that has had a major impact on practice: many frontier AI labs 
including OpenAI, xAI and Apple (and probably others too) make use of it. Of 
course, $$\mu$$P built itself on previous theoretical advances including the NTK, 
the theory of signal propagation in DNNs, and mean-field theories, among others.  


## Other resources
Besides the references below, I found the following material useful in 
understanding $$\mu$$P:
* Microsoft's [blog post](https://www.microsoft.com/en-us/research/blog/on-infinitely-wide-neural-networks-that-exhibit-feature-learning/) 
introducing $$\mu$$P;
* [this conversation](https://www.youtube.com/watch?v=1aXOXHA7Jcw&t=2723s&ab_channel=TimothyNguyen) 
with Greg Yang focused on "Tensor Programs";
* Microsoft's [blog post on the hyperparameter transfer results](https://www.microsoft.com/en-us/research/blog/%C2%B5transfer-a-technique-for-hyperparameter-tuning-of-enormous-neural-networks/);
* the [`mup`](https://github.com/microsoft/mup?tab=readme-ov-file#coord-check) github repo (PyTorch); and
* [this talk](https://www.youtube.com/watch?v=CnAfD7aVzLg&ab_channel=AutoMLSeminars) 
on the scaling exponents of different parameterisations;

For other reviews of $$\mu$$P, see:
* [this post](https://blog.speechmatics.com/mup) by Speechmatics, and
* [this post](https://cerebras.ai/blog/the-practitioners-guide-to-the-maximal-update-parameterization) 
by Cerebras.

See also the [`nanoGPT-mup`](https://github.com/EleutherAI/nanoGPT-mup?tab=readme-ov-file) 
github repo (PyTorch).


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
<i>Advances in Neural Information Processing Systems, 34</i>, 17084-17097.</font> </p>

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
Innocenti, F., Achour, E. M., & Buckley, C. L. (2025). $\mu$PC: Scaling Predictive Coding to 100+ Layer Networks. <i>arXiv preprint arXiv:2505.13124.</i> </font> </p>
