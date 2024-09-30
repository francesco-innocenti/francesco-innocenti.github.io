---
title: '🧠 The Energy Landscape of Predictive Coding Networks'
date: 2024-10-01
permalink: /posts/2024/10/01/The-Energy-Landscape-of-Predictive-Coding-Networks/
tags:
  - Predictive Coding
  - Backpropagation
  - Deep Neural Networks
  - Loss Landscape
  - Saddle Points
  - Gradient Descent
  - Vanishing Gradients
  - Local Learning
  - Inference Learning

---

>  📖 **TL;DR**: *Predictive coding makes the loss landscape of deep neural networks more benign and robust to vanishing 
> gradients.*

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/images/origin_saddle_toy_models.png" width="700">
</p>

This post explains my recent NeurIPS 2024 paper [Only Strict Saddles in the Energy Landscape of Predictive Coding Networks?](https://arxiv.org/abs/2408.11979). 
It was very much inspired by our [previous paper](https://openreview.net/forum?id=x7PUpFKZ8M) which I wrote about in 
[another post](https://francesco-innocenti.github.io/posts/2023/08/10/PC-as-a-2nd-Order-Method/).

This work was in collaboration with [El Mehdi Achour](https://scholar.google.com/citations?user=A-i6nwgAAAAJ&hl=en&oi=ao),
[Ryan Singh](https://scholar.google.com/citations?user=Ukqus4oAAAAJ&hl=en&oi=ao) 
and my supervisor [Christopher L. Buckley](https://scholar.google.com/citations?user=nWuZ0XcAAAAJ&hl=en&oi=ao).

## Overview

1. [Predictive coding: A refresher](#pc)
2. [Toy models (going deeper)](#toy)
3. [A landscape theory](#theory)
4. [Experiments](#exps)
5. [Concluding thoughts](#thoughts)

## 🧠 Predictive coding: A refresher <a name="pc"></a>

I gave a primer of predictive coding (PC) in a [previous blog post](https://francesco-innocenti.github.io/posts/2023/08/10/PC-as-a-2nd-Order-Method/), 
so here's a refresher. PC is an energy-based algorithm that can train deep neural networks as an alternative to 
backpropagation (BP). The key difference with BP is that PC performs iterative inference over network activities before 
updating weights, as schematically shown by the gif below. 

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/pc_inference.gif" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

More formally, PC first minimises an energy function $$\mathcal{F}$$ *with respect to activities*

$$
\textbf{PC inference:} \quad \Delta z \propto - \nabla_{z} \mathcal{F}
$$

until convergence is reached $$\Delta z \approx 0$$. For simplicity, we will denote the energy at an inference 
equilibrium as $$\mathcal{F}^*$$. Then, at the inference equilibrium, we update the weights

$$ 
\textbf{PC learning:} \quad \Delta \theta \propto - \nabla_{\theta} \mathcal{F}^*
$$

How can we gain insight into these learning dynamics? Previous theoretical works have tried, but they do not explain
all experimental data and tend to make simplifying assumptions or approximations. For example, in my previous work,
we showed that these first-order updates on neurons allow one to perform some kind of second-order update on the 
weights, making PC an implicit second-order method. In this work, however, we provide a more comprehensive theory.

## 🧸 Toy models (going deeper) <a name="toy"></a>

In our previous post, we considered the simplest possible deep neural network or multi-layer perceptron (MLP) with a single 
hidden linear unit $$f(x) = w_2w_1x$$. We then showed that PC inference has the effect of reshaping the
loss landscape, and SGD on this restructured landscape (the equilibrated energy) escapes the saddle point at the origin 
faster than on the loss $$\mathcal{L}$$.

<p align="center">
  <img src="../images/pc_trust_region_toy.png" width="700">
</p>

We used this example to motivate a theory of PC as an *approximate* implicit second-order method. However, this theory
does not have much predictive power and is only an approximation. Before generalising, however, let's try to see if
we can get some more intuition from a deeper network. First, still considering the origin, what happens if we add just one 
layer (with also one weight)?

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/toy_2mlp.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

Starting near the origin, SGD on the equilibrated energy also escapes significantly faster than on the loss. It's not
as easy to see from the landscape visualisation, but if you look closely BP (with SGD) spends a lot more time near the 
saddle (as indicated by the higher concentration of yellow points). Does this remain true for deeper and wide (non-unit) 
models as well?

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/toy_deep_mlp.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

Yes, as it turns out, and PC seems to escape even faster (as long as you initialise close to the origin) given the same
learning rate. Now we can no longer visualise the landscape; however, we can project it onto the maximum and minimum 
curvature (Hessian) directions. Interestingly, we see that around the origin the loss is flat (to second order) while 
the equilibrated energy has negative curvature. 

What is going on here? Can we say something more formal?

## 🤔 A landscape theory <a name="theory"></a>

In this paper, we used deep *linear* networks (DLNs) as theoretical model. This is because these are the standard model
for studies of the loss landscape and are relatively well understood. The first surprising result is that for DLNs we
can derive an exact solution for the energy at the inference equilibrium.

$$
\mathcal{F}^* = 1/2N \sum_i^N (\mathbf{y}_i W_{L:1} \mathbf{x}_i)^T S^{-1} (\mathbf{y}_i W_{L:1} \mathbf{x}_i)
$$

So, in the linear case, the equilibrated energy is simply a rescaled mean squared error (MSE) loss, where the rescaling
depends on the network weights. How does this rescaling reshape the loss landscape? Is it useful? 

Let's return to our origin saddle, for which we have some intuition. First, we know from previous work that this saddle
becomes flatter and flatter with the depth of the network. More specifically, the order-flatness of the saddle, if you like,
will be equal to the number of hidden layers. So, if you have 1 hidden layer, then the saddle is flat to order 1 (the 
gradient is zero). And if you have 2 hidden layers, then the saddle is flat to second order as the Hessian is zero.

First-order saddles are also known as strict, while higher-order saddles are labelled as non-strict. As it turns out,
the origin saddle of the equilibrated energy is always of first-order independent of network depth, with negative curvature.

$$
\lambda_{\text{min}}(H_{\mathcal{F}^*}(\boldsymbol{\theta} = \mathbf{0})) < 0, \quad \forall H \geq 1 [\text{strict saddle}]
$$

This explains our toy simulations. But what about other non-strict saddles? We know that there are plenty others in the loss 
landscape. In the paper we consider a general saddle type of which the origin is one (technically saddle of rank zero)
and prove that they all become strict in the equilibrated energy (see paper for more details).

## Experiments <a name="exps"></a>

The above theory is for linear networks. Does it still hold for practical, non-linear ones? Yes. We run a wide range of
experiments with different datasets, architectures and non-linearities and find that, when initialised close to any 
saddle that we consider, SGD on the equilibrated energy escapes much faster than on the loss (for the same learning rate).
The figure below is for the origin saddle, for example.

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/nonlinear_nets_origin_saddle.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

And for saddles that we do not address theoretically, we run ...

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/matrix_completion.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

## 💭 Concluding thoughts <a name="thoughts"></a>

TODO

## References

<p> <font size="3"> <a id="1">[1]</a> 
Millidge, B., Seth, A., & Buckley, C. L. (2021). Predictive coding: a theoretical and experimental review. <i>arXiv preprint arXiv:2107.12979</i>.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Du, S. S., Jin, C., Lee, J. D., Jordan, M. I., Singh, A., and Poczos, B. Gradient descent can take exponential time to escape saddle points. <i>Advances in neural information processing systems</i>, 30, 2017.</font> </p>

[^1]: ...
