---
title: '⛰️ The Energy Landscape of Predictive Coding Networks'
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
In it, we provide, in my humble opinion, the best theory so far on the learning dynamics of predictive coding. 
This work was very much inspired by our [previous paper](https://openreview.net/forum?id=x7PUpFKZ8M) which I wrote about 
in [another post](https://francesco-innocenti.github.io/posts/2023/08/10/PC-as-a-2nd-Order-Method/). 

I'd like to
acknowledge my collaborators [El Mehdi Achour](https://scholar.google.com/citations?user=A-i6nwgAAAAJ&hl=en&oi=ao),
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
so here's a refresher. PC is an energy-based learning algorithm that can be used as an alternative to backpropagation 
(BP) to train deep neural networks. The key difference with BP is that, before updating weights, PC performs iterative 
inference over the network activities, as schematically shown by the gif below. 

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/pc_inference.gif" width="300">
</p>

More formally, PC first minimises an energy function $$\mathcal{F}$$ *with respect to activities*

$$
\textbf{PC inference:} \quad \Delta z \propto - \nabla_{z} \mathcal{F}
$$

until convergence is reached $$\Delta z \approx 0$$. (For simplicity, we will denote the energy at an inference 
equilibrium as $$\mathcal{F}^*$$.) Then, at equilibrium, we update the weights

$$ 
\textbf{PC learning:} \quad \Delta \theta \propto - \nabla_{\theta} \mathcal{F}^*
$$

How can we gain insight into these learning dynamics? There have been some theories, but they have all tended to make 
unrealistic assumptions or approximations and do not predict well experimental data. In previous work [[1]](#1), for 
example, we showed that performing first-order updates on neurons allow one to perform some kind of second-order update 
on the weights, making PC an implicit second-order method. But this was only to a second-order approximation and doesn't 
provide as much explanatory power as we would like. 

## 🪆 Toy models (going deeper) <a name="toy"></a>

It's often a good idea to start from toy models. In our previous post, we considered the simplest possible deep neural 
network with a single hidden linear unit $$f(x) = w_2w_1x$$. We then showed that PC inference has the effect of 
reshaping the loss landscape, and that SGD on this reshaped landscape (the equilibrated energy) escapes the saddle 
point at the origin faster than on the loss $$\mathcal{L}$$.

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/toy_1mlp.png" style="zoom:20%;" />
</p>
<p align="center">
    <span style="color:grey; font-size:small;">Figure 1</span>
</p>

Now let's try to go deeper (don't think Inception 😉) and see if we can get some more intuition. Still looking at the 
origin, what happens if we add just one layer or weight?

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/toy_2mlp.png" style="zoom:20%;" />
</p>
<p align="center">
    <span style="color:grey; font-size:small;">Figure 2</span>
</p>

We see that, starting near the origin, SGD on the equilibrated energy escapes significantly faster than on the loss (given 
the same learning rate). It's not as easy to see from the landscape visualisations, but if you look closely BP spends a 
lot more time near the saddle (as indicated by the higher concentration of yellow dots 🟡). If this reminds you of 
"vanishing gradients", it's exactly that–just viewed from a landscape perspective. What happens if we further increase 
the network depth and width?

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/toy_deep_mlp.png" style="zoom:20%;" />
</p>
<p align="center">
    <span style="color:grey; font-size:small;">Figure 3</span>
</p>

For a more standard network (with 4 layers and non-unit width), PC now escapes orders of magnitude faster than BP 
(again initialising close to the origin and using SGD with the same learning rate). Now we can no longer visualise the 
landscape; however, we can project it onto the maximum and minimum curvature (Hessian) directions. Interestingly, we see 
that, while the loss is flat (to second order) around the origin, the equilibrated energy has negative curvature.

So it seems that, no matter the network depth and width, PC inference makes the origin saddle much easier to escape, 
with more robust to vanishing gradients. Can we say something more formal?

## 🏔 A landscape theory <a name="theory"></a>

In our paper, we use deep *linear* networks (DLNs) as our theoretical model, as these are the standard model for 
studies of the loss landscape and are relatively well understood. In contrast to previous theories of PC, this is
the only major assumption we make, and we empirically verify that the theory holds for non-linear networks.

The first surprising theoretical result is that for DLNs we can derive an exact solution for the energy at the inference 
equilibrium $$\mathcal{F}^*$$. This is important because this is the effective weight landscape on which PC learns. 

$$
\mathcal{F}^* = 1/2N \sum_i^N (\mathbf{y}_i - W_{L:1} \mathbf{x}_i)^T S^{-1} (\mathbf{y}_i - W_{L:1} \mathbf{x}_i)
$$

where as standard $$\mathbf{x}_i$$ and $$\mathbf{y}_i$$ are the input and output, respectively, and $$W_{L:1}$$ is just 
a shorthand for the network's feedforward map. So, in the linear case, the equilibrated energy is simply a rescaled 
mean squared error (MSE) loss, where the rescaling depends on the network weights. This formalises the intuition from 
our toy simulations that PC inference has the effect of reshaping the loss landscape. But How does this rescaling 
reshape the loss landscape?

Let's return to our origin saddle, for which we have some intuition. We know from previous work that this saddle
becomes flatter and flatter as you increase the depth of the network. More precisely, the "order-flatness" of the 
saddle, if you like, is equal to the number of hidden layers (think vanishing gradients). So, if you have 1 hidden layer, 
then the saddle is flat to order 1 (the gradient is zero), but there is negative curvature. And if you have 2 hidden 
layers, then there is no curvature around the saddle, but there will be an escape direction in the third-derivative.

First-order saddles are also known as "strict", while higher-order saddles are labelled as "non-strict" [[2]](#2). You 
can loosely think of these are "good" and "bad" saddles, respectively, in that strict saddles are relatively easy to 
escape. It turns out that the origin saddle of the equilibrated energy is always strict independent of network depth. 
In maths speak,

$$
\lambda_{\text{min}}(H_{\mathcal{F}^*}(\boldsymbol{\theta} = \mathbf{0})) < 0 \quad [\text{strict saddle}]
$$

The Hessian at the origin of the equilibrated energy has negative curvature for any DLN. This result explains our toy 
simulations. But what about other non-strict saddles? We know that there are plenty others in the loss landscape. 
Do they also become strict in the equilibrated energy, i.e. after PC inference? In the paper we consider a 
general saddle type of which the origin is one (technically saddles of rank zero) and prove that indeed they all 
become strict in the equilibrated energy.

## Experiments <a name="exps"></a>

The above theory is for linear networks. Does it still hold for practical, non-linear ones? Fortunately, yes. We run a 
variety of experiments with different datasets, architectures and non-linearities and in all cases find that, when 
initialised close to any of the studied saddles, SGD on the equilibrated energy escapes much faster than on the loss 
(again for the same learning rate). The figure below shows results for the origin saddle, for example.

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/nonlinear_nets_origin_saddle.png" style="zoom:15%;" />
</p>
<p align="center">
    <span style="color:grey; font-size:small;">Figure 4</span>
</p>

To test saddles that we do not address theoretically, we trained networks on a matrix completion task where we know that
starting near the origin GD will transition through saddles of successive rank before converging to a solution. The
figure below shows that PC quickly escapes all the saddles visited by BP, including higher-order ones that we did not 
study theoretically, and that it does not suffer from vanishing gradients.

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/matrix_completion.png" style="zoom:15%;" />
</p>
<p align="center">
    <span style="color:grey; font-size:small;">Figure 5</span>
</p>

Based on all these results, we conjecture that all the saddles of the equilibrated energy are strict. We don't prove it,
hence the question mark in the title, but the empirical evidence is quite compelling.

## 💭 Concluding thoughts <a name="thoughts"></a>

TODO

## References

<p> <font size="3"> <a id="1">[1]</a> 
Innocenti, F., Singh, R., & Buckley, C. L. (2023). Understanding Predictive Coding as a Second-Order Trust-Region Method. <i>ICML Workshop on Localized Learning (LLW).</i>.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
R. Ge, F. Huang, C. Jin, and Y. Yuan. (2015). Escaping from saddle points—online stochastic gradient for tensor decomposition. <i>In Conference on learning theory,</i> pages 797–842. PMLR..</font> </p>
