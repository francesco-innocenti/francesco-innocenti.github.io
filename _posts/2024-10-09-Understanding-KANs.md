---
title: 'Understanding KANs'
date: 2024-10-09
permalink: /posts/2024/10/09/Understanding-KANs/
tags:
  - Multi-layer Perceptrons
  - Deep Neural Networks
  - Kolmogorov-Arnold Networks
  - KAN
  - Kolmogorov-Arnold Representation Theorem
  - Splines
  - Neural Scaling Laws
  - Interpretability

---

Confused about the recent [KAN: Kolmogorov-Arnold Networks](https://arxiv.org/abs/2404.19756)? Me too, so I re-derived 
a minimal example where it is easy to see the difference between KANs and multi-layer perceptrons (MLPs).


## KAN architecture made easy

A single neuron is all we need to start with. Recall that a neuron in an MLP simply performs a weighted sum of its 
inputs and then applies some activation function $$\phi$$ (e.g. ReLU)

$$
\textbf{MLP neuron:} \quad z_i = \phi \left( \sum_{j=1}^{n} w_{ij}x_j \right) \quad [\text{"Sum, then activate"}]
$$

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/mlp_neuron.png" width="200">
</p>

A KAN neuron, by contrast, applies a unique activation function $$\phi_{j}$$ to each input $$x_{j}$$ and then sums

$$
\textbf{KAN neuron:} \quad z_i = \sum_{j=1}^{n} \phi_{ij}(x_j) \quad [\text{"Activate, then sum"}]
$$

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/kan_neuron.png" width="200">
</p>

That's it. That's the fundamental difference between KANs and MLPs. So, as the authors emphasise, while MLPs have *fixed
activations on nodes*, KANs have *learnable activations on edges*. To extend to layers, recall the MLP layer is just an 
affine transformation $$W_\ell$$ of the previous layer followed by the activation function $$\phi$$ applied element-wise

$$
\textbf{MLP layer:} \quad \mathbf{z}_\ell = \phi(W_\ell \mathbf{z}_{\ell-1})
$$

Now, if you try to combine KAN neurons, you realise that all the activation functions of a layer $$\phi_{ij}$$ can be 
combined in a single matrix $$\boldsymbol{\phi}_\ell$$

$$
\textbf{KAN layer:} \quad \mathbf{z}_\ell = \boldsymbol{\phi}_\ell \mathbf{z}_{\ell-1}
$$

so that a KAN layer is a non-linear transformation of the previous layer. 


## But why? The KA theorem

TODO

## References

<p> <font size="3"> <a id="1">[1]</a> 
Z. Liu, Y. Wang, S. Vaidya, F. Ruehle, J. Halverson, M. Soljačić, T. Y. Hou, and M. Tegmark. Kan: Kolmogorov-arnold networks. <i>arXiv preprint arXiv:2404.19756</i>, 2024.</font> </p>

