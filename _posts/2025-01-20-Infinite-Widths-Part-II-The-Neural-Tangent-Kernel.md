---
title: '♾️ Infinite Widths Part II: The Neural Tangent Kernel'
date: 2025-01-20
permalink: /posts/2025/01/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Neural Tangent Kernel
  - Kernel Methods
  - Lazy Learning
  - Linear Regime

---

This is the second post of a short series on the infinite-width limits of deep neural networks (DNNs). Previously, we 
reviewed the correspondence between neural networks and Gaussian Processes (GPs), basically finding that, as the number 
neurons in the hidden layers grows to infinity, the output of a random network becomes Gaussian distributed. Here, we 
go beyond initialisation and look at the Neural Tangent Kernel (NTK) regime, also known as the linear, kernel or "lazy" 
regime for reasons that will become clear below. 

The NTK goes one step beyond the NNGP result by examining the training dynamics of infinitely wide networks, showing 
that (full-batch) gradient descent (GD) training of DNNs can be described by a kernel GD in function space, or 
equivalently, that the network can be replaced by a linearisation in its parameters.

## TL;DR
> **The Neural Tangent Kernel**: *In the infinite-width limit, full-batch gradient descent (GD) training of DNNs can be 
> described by a kernel GD in function space, and the network can be replaced by a linearisation in its parameters *

## Brief history
While similar ideas were afloat in the literature, the function-space NTK was first coined and characterised by 
[[1]](#1). [[2]](#2) and [[3]](#3) extended these results to parameter space, with [[2]](#2) in particular highlighting 
the "laziness" of this regime as the lack of feature learning. Since then, a flurry of papers on the NTK has emerged,
including an extension to basically any standard architecture [[4]](#4). Since this limit is very brittle, most of these
papers try to understand what happens when one tries to move away from it along one or more axes.

## NTK: Function space view
We start by considering a fully connected network of width $N$ and depth $L$



A note on notation: different papers tend to use slightly different notation, often depending on emphasis. 

NOTE: different parameterisation! A note on notation about derivatives...

We will start by considering the gradient flow (continuous-time GD) dynamics of the parameters $$\theta$$ of some network
$$
\frac{d\theta}{dt} = - \nabla_\theta \mathcal{L} = - \frac{\partial f_t}{\partial \theta}^T \frac{\mathcal{L}}{\partial f_t}
$$
where $$\mathcal{L}$$ is some loss function, say the mean squared error. We use the chain rule to get the gradient flow 
dynamics of the network function
$$
\frac{df}{dt} = \frac{\partial f_t}{\partial \theta} \frac{\partial \theta}{\partial t} = 
- \underbrace{\hat{\Theta}_t(X, X')}_{\text{NTK}} \frac{\mathcal{L}}{\partial f_t}
$$
where $$\hat{\Theta}_t(X, X') \coloneqq \frac{\partial f(X)_t}{\partial \theta} \frac{\partial f(X)_t}{\partial \theta}^T$$ is the 
NTK, since it can be seen as a kernel given by the parameter gradient of the function. The challenge in understanding
these dynamics is that the NTK depends on the random initialisation and changes at each training step $$t$$. However, 
as shown by [[1]](#1), in the infinite-width limit the NTK converges and remains constant throughout training 
$$\hat{\Theta}_t(X, X') = \hat{\Theta}_0(X, X')$$.

## NTK: Parameter space view

$$
TODO
$$

## Why does this matter?
...

In the next and last post of this series on the infinite-width limits of DNNs, we will look at ...


## Other resources


## References

<p> <font size="3"> <a id="1">[1]</a> 
Jacot, A., Gabriel, F., & Hongler, C. (2018). Neural tangent kernel: Convergence and generalization in neural networks. 
<i>Advances in neural information processing systems, 31.</i> </font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Chizat, L., Oyallon, E., & Bach, F. (2019). On lazy training in differentiable programming. <i>Advances in neural 
information processing systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Lee, J., Xiao, L., Schoenholz, S., Bahri, Y., Novak, R., Sohl-Dickstein, J., & Pennington, J. (2019). Wide neural 
networks of any depth evolve as linear models under gradient descent. <i>Advances in neural information processing 
systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Yang, G. (2020). Tensor programs ii: Neural tangent kernel for any architecture. <i>arXiv preprint 
arXiv:2006.14548.</i> </font> </p>
