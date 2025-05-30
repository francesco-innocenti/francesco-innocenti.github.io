---
title: 'KANs Made Simple'
date: 2024-10-09
permalink: /posts/2024/10/09/KANs-Made-Simple/
tags:
  - multi-layer perceptrons
  - deep neural networks
  - Kolmogorov-Arnold networks
  - KAN
  - Kolmogorov-Arnold representation theorem
  - splines
  - neural scaling laws
  - interpretability

---

🤔 Confused about the recent [KAN: Kolmogorov-Arnold Networks](https://arxiv.org/abs/2404.19756)? I was too, so here's 
a minimal explanation that makes it easy to see the difference between KANs and multi-layer perceptrons (MLPs).


## The KAN architecture made easy

A single neuron is all we need to start with. Recall that a neuron in an MLP simply performs a weighted sum of its 
inputs and then applies some activation function $$\phi$$ (e.g. ReLU).

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/mlp_neuron.png" width="200">
</p>

$$
\textbf{MLP neuron:} \quad z_i = \phi \left( \sum_{j=1}^{n} w_{ij}x_j \right)
$$

A KAN neuron, on the other hand, applies a unique activation function $$\phi_{j}$$ to each input $$x_{j}$$ and then sums

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/kan_neuron.png" width="200">
</p>

$$
\textbf{KAN neuron:} \quad z_i = \sum_{j=1}^{n} \phi_{ij}(x_j)
$$

That's it. That's the fundamental difference between KANs and MLPs. As the authors emphasise, while MLPs have 
*fixed activations on nodes*, KANs have *learnable activations on edges*. These learnable activations are *splines*, 
which are basically a way of smoothly connecting a set of points by dividing the space between them into segments and 
fitting a polynomial to each segment.

Extending to a layer of neurons, recall that the MLP layer is just a linear transformation $$W_\ell$$ of the previous 
layer followed by the activation function $$\phi$$ applied element-wise.

$$
\textbf{MLP layer:} \quad \mathbf{z}_\ell = \phi(W_\ell \mathbf{z}_{\ell-1})
$$

Now, if you try to put together KAN neurons in a layer, you realise that all the activation functions of a layer 
$$\phi_{ij}$$ can be combined in a single matrix $$\boldsymbol{\phi}_\ell$$

$$
\textbf{KAN layer:} \quad \mathbf{z}_\ell = \boldsymbol{\phi}_\ell \mathbf{z}_{\ell-1}
$$

so that a KAN layer is a non-linear transformation of the previous layer. Like an MLP, a KAN is then simply a stack of
its layers.

$$
\begin{equation}
\begin{aligned}
\text{MLP}(\mathbf{x}) &= (W_L \circ \phi \circ W_{L-1} \circ \phi \circ \dots \circ \phi \circ W_1)\mathbf{x} \\
\text{KAN}(\mathbf{x}) &= (\boldsymbol{\phi}_L \circ \boldsymbol{\phi}_{L-1} \circ \dots \circ \boldsymbol{\phi}_1)\mathbf{x}
\end{aligned}
\end{equation}
$$


## But why? The Kolmogorov-Arnold representation theorem

What fundamentally motivates this change in architecture design? Enter the Kolmogorov-Arnold representation (KAT) 
theorem. Very roughly, this says that

> **KAT theorem**: *Any multivariate continuous function can be represented by summing many univariate continuous functions.*
 
The theorem was proved for the following 2-layer KAN

$$
f(x_1, \dots, x_n) = \sum_{i=1}^{2n+1} \boldsymbol{\phi}_i \left( \sum_{j=1}^n \phi_{ij}(x_j)  \right) 
$$

where $$2n+1$$ is the hidden layer size. But what about the approximation capabilities of deep KANs of the kind tested 
by the authors? Interestingly, [this recent paper](https://arxiv.org/abs/2410.01803) seems to prove that while MLPs can 
be represented by KANs of comparable (slightly larger) size, they scale quadratically (instead of linearly) with the 
grid size of the splines, suggesting that certain functions can be represented more efficiently by KANs.


## References

<p> <font size="3"> <a id="1">[1]</a> 
Z. Liu, Y. Wang, S. Vaidya, F. Ruehle, J. Halverson, M. Soljačić, T. Y. Hou, and M. Tegmark. Kan: Kolmogorov-arnold networks. <i>arXiv preprint arXiv:2404.19756</i>, 2024.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Y. Wang, J. W. Siegel, Z. Liu, T. Y. Hou. On the expressiveness and spectral bias of KANs. <i>arXiv preprint arXiv:2410.01803.</i>, 2024.</font> </p>
