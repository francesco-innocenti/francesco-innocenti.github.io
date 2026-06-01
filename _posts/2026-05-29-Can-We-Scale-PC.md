---
title: 'Can We Scale Predictive Coding? or Why the Brain Might Be Much Wider Than Deep'
date: 2026-05-29
permalink: /posts/2026/05/29/Can-We-Scale-PC/
tags:
  - predictive coding
  - backpropagation
  - local learning
  - infinite width
  - infinite depth
  - maximal update parameterisation
  - muP
  - hyperparameter transfer
  - dynamical mean field theory


---

>  📖 **TL;DR**: *The gradients computed by predictive coding converge to 
backpropagation's for much wider than deep networks (like the brain), under 
stable parameterisations.*

In this post, I review my 2026 ICML paper [On the Infinite Width and Depth Limits of Predictive Coding Networks
](https://arxiv.org/abs/2602.07697). The paper is quite technical, so here we 
focus on explaining the key results at a high level and their implications.


## Motivation
Anyone who has taken an introductory AI course should know that at the core of 
training artificial neural networks is an algorithm called "backpropagation" (BP). 
While powerful, BP is energy inefficient and "biologically implausible" [[1]](#1). 
In particular, while neurons in brain change their connections (or synapses) 
only based on neurons they talk to, BP requires propagating "non-local" 
information through the network.

Predictive coding (PC) is an influential, brain-inspired learning algorithm 
as an alternative to BP [[2]](#2). PC has a long history as a theory of information 
processing in the brain and is based on the basic idea that neurons minimise 
their local prediction errors [[3]](#3).

However, despite some recent encouraging progress [[4]](#4)[[5]](#5)[[6]](#6), 
training wide and especially deep PC networks (PCNs) on large-scale datasets 
competitively with BP remains an open challenge [[7]](#7). Indeed, this is 
*the challenge* at the heart of the whole field of local learning algorithms.

In asking why local algorithms like PC might be hard to scale, it is natural to 
look at what has enabled the successful scaling of BP. While scaling laws 
[[8]](#8) have arguably been the most important factor, if one looks carefully 
at the literature and talks to people at frontier AI labs, one realises that 
model parameterisations derived in "idealised limits" (e.g. infinite width) 
[[9]](#9)[[10]](#10)[[11]](#11) are often used in practice. 

These theoretically motivated parameterisations not only ensure stable training 
dynamics across scales, but also enable the empirical transfer of optimal 
hyperparameters (e.g. learning rate) from small to large models [[12]](#12), 
avoiding the prohibitive tuning cost at large scale. If you have heard of 
$$\mu$$P [[9]](#9), then this is what I am talking about. I have a separate 
[post on this topic](https://francesco-innocenti.github.io/posts/2025/04/09/Infinite-Widths-&-Depths-Part-III-The-Maximal-Update-Parameterisation/), 
but it's not necessary to understand our ICML results.

In this work, we adopted this approach and analysed the infinite width and 
depth limits of networks trained with PC (as opposed to BP). In particular, we 
theoretically derive and empirically validate stable parameterisations for wide 
and deep PCNs, including convolutional networks and transformers. 


## Key results
Our work has two main results. First, we show that

> the set of scalable parameterisations for PC is the same as for BP, in the 
sense of being numerically stable and learning non-trivial features at large 
width and depth. 

Below is a visual illustration of the result. We start by considering the same 
set of general parameterisations as in previous work, and find that the subset 
of parameterisations that are stable (in a well-defined sense) for BP turns out 
to be the exactly same as for PC.

<p>
    <span style="display: block; text-align: center;">
        <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/param_venn_diag.png" style="zoom:50%;">
    </span>
    <span style="display: block; text-align: left; color:grey; font-size:large;">
        <b>The stable parameterisations for PC are exactly the same as for BP.</b> 
        We start by considering the same set of general parameterisations as in 
        previous work, and find that the subset of stable and "rich" (non-lazy) 
        parameterisations when scaling model width and depth for PC is the same 
        as for BP.
    </span>
</p>

The other main result turns out to be a straightforward consequence:

> under of these stable parameterisations, the weight gradients computed 
by PC converge to those computed by BP in a regime where the model width is much 
larger than the depth.

Below is an empirical verification of this result. We train linear residual 
networks with a stable parameterisation on CIFAR-10, and plot the cosine 
similarity between the PC gradients and the BP gradients as a function of the 
model width and depth. As predicted by the theory, we see that the gradient 
alignment converges to 1 for much wider than deep networks.

<p align="left">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/bp_width_convergence_linear.png">
    <span style="color:grey; font-size:large;">
        <b>PC converges to BP for wider than deep linear networks, under stable parameterisations.</b> 
        We train linear residual networks on CIFAR-10 with a stable 
        parameterisation. Plotted is the mean cosine similarity over 3 runs 
        between the PC gradients and the BP gradients at different training 
        steps t. See the paper for more details.
    </span>
</p>

This result turns out to be surprisingly general (see the figure below): we find 
that convergence to BP at large width holds for nonlinear networks including 
CNNs and transformers, trained with different optimisers and loss functions, 
on small and large-scale datasets (e.g. ImageNet).

<p align="left">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/bp_width_convergence_nonlinear.png">
    <span style="color:grey; font-size:large;">
        <b>PC still converges to BP for different nonlinear architectures that are much wider than deep, under stable parameterisations.</b> 
        For more details, see the paper.
    </span>
</p>


## Implications
Our results have 2 key implications for the scaling of PC. First:

> ***if*** one would like to satisfy reasonable notions of stability and 
feature-learning (“the $$\mu$$P desiderata”) [[9]](#9), then ***necessarily*** 
the only scalable parameterisation for PC is the same as for BP (i.e. $$\mu$$P), 
in the sense of being numerically stable and learning non-trivial features at 
large width and depth.

This means that PCNs trained in practice (with the "standard parameterisation") 
cannot be stably scaled in width and depth.

While this result may appear negative, we are also the first (to the best of our 
knowledge) to show that

> BP can be effectively implemented with a local algorithm ***at scale***, for
much wider than deep models.

This result is interesting for two reasons. First, modern LLMs have a width 
(aka embedding dimension) that is at least one order of magnitude larger than 
their depth. This means that if one could do inference fast with PC (more on 
this below), then we could speed up model training by a factor ~depth, since the 
weight updates of PC are parallelisable across layers.

Second, the brain is indeed much wider than it is deep [[13]](#13), with ~10k 
synapses per neurons and 6 cortical layers. Our results therefore suggest an 
elegant way in which biology could do backprop using only local updates.


## Limitations & future directions
Our work has still several limitations pointing to future directions. First, 
while we provided supporting experiments on different nonlinear architectures, 
our theory relies on linear networks. It could be interesting to see if one 
could use tools from dynamical mean field theory (as used in previous work) 
[[10]](#10)[[14]](#14) to generalise the theory to nonlinear models.

Our results also do not necessarily rule out other notions or desiderata of a 
stable and feature-learning parameterisation, where PC might not converge to 
(and perhaps be better than) BP.

The main bottleneck of PC remains the computational cost of converging its 
iterative (optimisation-based) inference process. While there has been some 
recent work accelerating this on GPUs [[6]](#6)[[15]](#15), it is clear that 
to beat BP we need analog implementations. Whether PC can be implemented on 
such hardware remains an important open question.

The standard transformer we tested is not biologically plausible since the 
self-attention mechanism [[16]](#16) is highly non-local. It would be 
interesting to investigate attention mechanisms where the softmax is itself the 
gradient of some energy function [[17]](#17). These mechanisms are closely 
related to modern Hopfield networks [[18]](#18) and have some bio-plausible 
implementations [[19]](#19). 


## References

<p> <font size="3"> <a id="1">[1]</a> 
Lillicrap, T. P., Santoro, A., Marris, L., Akerman, C. J., & Hinton, G. (2020). 
Backpropagation and the brain. <i>Nature Reviews Neuroscience, 21</i>(6), 
335-346.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Millidge, B., Seth, A., & Buckley, C. L. (2021). Predictive coding: a 
theoretical and experimental review. <i>arXiv preprint arXiv:2107.12979.</i> </font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Rao, R. P., & Ballard, D. H. (1999). Predictive coding in the visual cortex: a 
functional interpretation of some extra-classical receptive-field effects. 
<i>Nature neuroscience, 2</i>(1), 79-87.</font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Qi, C., Lukasiewicz, T., & Salvatori, T. (2025). Training deep predictive coding 
networks. <i>In New Frontiers in Associative Memories.</i> </font> </p>

<p> <font size="3"> <a id="5">[5]</a> 
Innocenti, F., Achour, E. M., & Buckley, C. L. (2025). $$\mu$$PC: Scaling 
Predictive Coding to 100+ Layer Networks. <i>Advances in Neural Information 
Processing Systems 38.</i> </font> </p>

<p> <font size="3"> <a id="6">[6]</a> 
Goemaere, C., Oliviers, G., Bogacz, R., & Demeester, T. (2025). ePC: Overcoming 
Exponential Signal Decay in Deep Predictive Coding Networks. <i>arXiv preprint 
arXiv:2505.20137.</i> </font> </p>

<p> <font size="3"> <a id="7">[7]</a> 
Pinchetti, L., Qi, C., Lokshyn, O., Emde, C., M'Charrak, A., Tang, M., ... & 
Salvatori, T. (2025). Benchmarking Predictive Coding Networks--Made Simple. In 
<i>International Conference on Learning Representations</i> (Vol. 2025, pp. 
35701-35734).</font> </p>

<p> <font size="3"> <a id="8">[8]</a> 
Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., 
... & Amodei, D. (2020). Scaling laws for neural language models. 
<i>arXiv preprint arXiv:2001.08361.</i> </font> </p>

<p> <font size="3"> <a id="9">[9]</a> 
Yang, G., & Hu, E. J. (2021). Tensor programs iv: Feature learning in 
infinite-width neural networks. In <i>International Conference on Machine 
Learning</i> (pp. 11727-11737). PMLR.</font> </p>

<p> <font size="3"> <a id="10">[10]</a> 
Bordelon, B., & Pehlevan, C. (2022). Self-consistent dynamical field theory of 
kernel evolution in wide neural networks. <i>Advances in Neural Information 
Processing Systems, 35</i>, 32240-32256.</font> </p>

<p> <font size="3"> <a id="11">[11]</a> 
Dey, N., Zhang, B., Noci, L., Li, M., Bordelon, B., Bergsma, S., ... & Hestness, 
J. (2026). Don't be lazy: CompleteP enables compute-efficient deep transformers. 
<i>Advances in Neural Information Processing Systems, 38</i>, 
137707-137739.</font> </p>

<p> <font size="3"> <a id="12">[12]</a> 
Yang, G., Hu, E., Babuschkin, I., Sidor, S., Liu, X., Farhi, D., ... & Gao, J. 
(2021). Tuning large neural networks via zero-shot hyperparameter transfer. 
<i>Advances in Neural Information Processing Systems, 34</i>, 
17084-17097.</font> </p>

<p> <font size="3"> <a id="13">[13]</a> 
Suzuki, M., Pennartz, C. M., & Aru, J. (2023). How deep is the brain? The 
shallow brain hypothesis. <i>Nature Reviews Neuroscience, 24</i>(12), 
778-791.</font> </p>

<p> <font size="3"> <a id="14">[14]</a> 
Bordelon, B., & Pehlevan, C. (2022). The influence of learning rule on 
representation dynamics in wide neural networks. 
<i>arXiv preprint arXiv:2210.02157.</i> </font> </p>

<p> <font size="3"> <a id="15">[15]</a> 
Pinchetti, L., Frieder, S., Lukasiewicz, T., & Salvatori, T. (2026). Faster 
Predictive Coding Networks via Better Initialization. 
<i>arXiv preprint arXiv:2601.20895.</i> </font> </p>

<p> <font size="3"> <a id="16">[16]</a> 
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, 
A. N., ... & Polosukhin, I. (2017). Attention is all you need. 
<i>Advances in neural information processing systems, 30.</i> </font> </p>

<p> <font size="3"> <a id="17">[17]</a> 
Singh, R., & Buckley, C. L. (2023). Attention as implicit structural inference. 
<i>Advances in Neural Information Processing Systems, 36</i>, 
24929-24946.</font> </p>

<p> <font size="3"> <a id="18">[18]</a> 
Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T., ... & 
Hochreiter, S. (2020). Hopfield networks is all you need. 
<i>arXiv preprint arXiv:2008.02217.</i> </font> </p>

<p> <font size="3"> <a id="19">[19]</a> 
Kozachkov, L., Slotine, J. J., & Krotov, D. (2025). Neuron–astrocyte 
associative memory. <i>Proceedings of the National Academy of Sciences, 122</i>(21), 
e2417788122.</font> </p>
