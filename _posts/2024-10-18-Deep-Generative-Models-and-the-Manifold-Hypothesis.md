---
title: 'Deep Generative Models and the Manifold Hypothesis'
date: 2024-10-18
permalink: /posts/2024/10/18/Deep-Generative-Models-and-the-Manifold-Hypothesis/
tags:
  - Deep Generative Models
  - Manifold Hypothesis
  - Manifold Learning
  - Manifold Overfitting
  - Variational Autoencoders
  - Normalizing Flows
  - Energy-based Models
  - Generative Adversarial Networks
  - Diffusion Models

---

This post provides a brief review of deep generative models (DGMs) from the perspective of the "manifold hypothesis" as
recently outlined in [this paper](). 

## The manifold hypothesis
The manifold hypothesis essentially says that.

> **Manifold hypothesis**: high-dimensional data in $\mathbb{R}^{D}$ of the real world lies in a much lower and often 
> unknown $d$-dimensional space or submanifold $\mathbb{M} \in \mathbb{R}^{D}$ with $d < D$.

As X show, it turns out that taking this hypothesis seriously goes a long way towards explaining the successes and failures
of a variety of DGMs and has important implications for their development and refinement. This hypothesis is intuitive,
for example if one considers images and realises that changing the value of one pixel will likely not affect the overall
image. There are also theoretical results showing that the difficulty of learning (for example the data density) scales
exponentially with the *intrinsic* $d$ dimension of the data rather than its *ambient* one. If this were not true, then
DGMs would not work given the high dimensionality of modern data modalities such as images and text (the curse of 
dimensionality). Finally, there is solid empirical evidence that the intrisic dimension of datasets such as images is 
indeed much lower than its ambient dimension.

low-dimensional structure

* manifold-aware
* manifold-unaware
* 2-step models
* upper bound on Wasserstein distance


Observation: autoencoders do not by themselves learn the data manifold structure even with perfect reconstruction, since
the it could learn to both decode points outside the manifold and (see Figure 1)

failures of KL divergence




## References

<p> <font size="3"> <a id="1">[1]</a> 
Z. Liu, Y. Wang, S. Vaidya, F. Ruehle, J. Halverson, M. Soljačić, T. Y. Hou, and M. Tegmark. Kan: Kolmogorov-arnold networks. <i>arXiv preprint arXiv:2404.19756</i>, 2024.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Y. Wang, J. W. Siegel, Z. Liu, T. Y. Hou. On the expressiveness and spectral bias of KANs. <i>arXiv preprint arXiv:2410.01803.</i>, 2024.</font> </p>
