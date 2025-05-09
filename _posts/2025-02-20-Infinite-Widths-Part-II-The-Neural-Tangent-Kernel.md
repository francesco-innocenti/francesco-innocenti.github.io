---
title: '♾️ Infinite Widths Part II: The Neural Tangent Kernel'
date: 2025-02-20
permalink: /posts/2025/02/20/Infinite-Widths-Part-II-The-Neural-Tangent-Kernel/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Neural Tangent Kernel
  - Kernel Methods
  - Lazy Learning
  - Linear Regime

---

This is the second post of a short series on the infinite-width limits of deep neural networks (DNNs). [Previously](https://francesco-innocenti.github.io/posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/), we 
reviewed the correspondence between neural networks and Gaussian Processes (NNGP), showing that, as the number 
neurons in the hidden layers grows to infinity, the output of a random network becomes Gaussian distributed. 

Here, we 
go beyond initialisation and look at the Neural Tangent Kernel (NTK) regime, also known as the linear, kernel or "lazy" 
regime for reasons that will become clear below. The NTK goes one step beyond the NNGP result by examining the training dynamics of infinitely wide networks.


## TL;DR
> **The Neural Tangent Kernel**: In the infinite-width limit, full-batch gradient descent (GD) training of DNNs can be 
> described by a kernel GD in function space, which is equivalent to replacing the network with a linearisation of its parameters at initialisation.


## Brief history
While similar ideas were afloat in the literature, the function-space NTK was first coined and characterised by 
[[1]](#1). [[2]](#2) and [[3]](#3) extended these results to parameter space, with [[2]](#2) in particular highlighting 
the "laziness" of this regime as the lack of feature learning. Since then, a flurry of papers on the NTK has emerged,
including an extension to basically any standard architecture [[4]](#4). Since this limit is very brittle, most of these
papers try to understand what happens when one tries to move away from it along one or more axes.


## NTK: Function space view
> **A note on notation**: different papers use slightly different notation depending on emphasis and formality. Here we prioritise brevity over rigour.

Consider a fully connected network of width $$N$$ and depth $$L$$

$$
\mathbf{z}_\ell = \frac{1}{\sqrt{N_\ell}} W_\ell \phi(\mathbf{z_{\ell-1}})
$$

where $$z_\ell$$ are the layer preactivations, $$\phi$$ is some activation function, and $$W_\ell$$ are the weights all initialised from a standard Gaussian, $$W_{ij} \sim \mathcal{N}(0, 1)$$. Note that, unlike the standard parameterisation used for the [GP results](https://francesco-innocenti.github.io/posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/), we rescale the layers themselves by the width $$N_\ell$$ rather than the initialisation. This is known as the "NTK parameterisation", and the reason for this subtle change is that we would like to keep the backward pass as well as the forward pass stable at infinite width since we are also interested in the training dynamics.

Now consider the gradient flow (continuous-time GD) dynamics of the parameters $$\theta$$ of an NTK-parameterised network

$$
\begin{align}
  \dot{\theta} = - \nabla_\theta \mathcal{L} &= - \frac{\partial f(X)}{\partial \theta}^T \nabla_f \mathcal{L} \\
  &= - \frac{\partial f(X)}{\partial \theta}^T (Y - f(X))
\end{align}
$$

where the first term is the Jacobian of the output with respect to the parameters evaluated on all the training inputs $$X$$, and $$\mathcal{L}$$ is the mean squared error loss. We use the chain rule to get the gradient flow (GF) dynamics of the network function

$$
\begin{equation}
  \dot{f} = \frac{\partial f(X)}{\partial \theta} \dot{\theta} = 
  - \underbrace{K_t(X, X')}_{\text{NTK}} (Y - f(X))
\end{equation}
$$

where $$K_t(X, X') := \frac{\partial f(X)}{\partial \theta} \frac{\partial f(X)}{\partial \theta}^T$$ is the object known as the NTK since it can be seen as a kernel given by the parameter gradient (hence tangent) of the network function (hence neural).

The challenge in understanding
these dynamics is that the NTK depends on the initialisation and changes at each training step t[^1]. However, as shown by [[1]](#1), in the infinite-width limit the NTK becomes deterministic at initialisation and remains constant throughout training, $$K_t(X, X') = K_0(X, X')$$. It turns out that this is the same as approximating the network as a linear model around its initialisation ([[2]](#2) & [[3]](#3)), as we show next.


## NTK: Parameter space view
Consider a first-order Taylor expansion of the network at initialisation $$\theta_0$$,

$$
f^{\text{lin}}(\theta) \approx f(\theta_0) + \frac{\partial f(\theta_0)}{\partial \theta}^T (\theta - \theta_0)
$$

where we omit the inputs and emphasise the dependence of f on the initialisation. This can be justified by showing that the Hessian vanishes with the width [[2]](#2). Noting that the approximation is linear in $$\theta$$, we now take the parameter gradient of the linearised model

$$
\dot{\theta} = - \frac{\partial f(\theta_0)}{\partial \theta}^T (Y - f(X))
$$

We again use the chain rule to obtain the function GD dynamics

$$
\dot{f} = - K_0(X, X') (Y - f(X))
$$

where we see that the NTK is constant that depends only on the network architecture. Because the parameters barely move from their initialisation, this is popularly known as the "lazy regime", as first termed by [[2]](#2). 

Together, these results show that, in the infinite-width limit, the parameter and function dynamics of DNNs can be understood as a kernel method. In the case of the mean squared error loss, we can solve these analytically, without the need to train a neural network.


## Why does this matter?
The NTK result went beyond the GP correspondence---which only considered the forward pass of infinite-width networks---by studying the training dynamics. It thus provided a crucial bridge between the much-better understood kernels and DNNs. 

However, as emphasised by [[2]](#2), the main limitation of the NTK is that the network barely learns in this regime, which does not seem to capture the behaviour of real, finite-width networks. Indeed, as mentioned above, any small departure from the above assumptions---different loss, large learning rates, weight regularisation, etc.---break away from this limit. More to the point, people found that these idealised networks have worse generalisation than their finite-width counterparts (e.g. see [[4]](#4) & [[5]](#5)).

In the next post of this series, we will look at a more recent and influential parameterisation of DNNs which went beyond the NTK and effectively "put the learning back" into the infinite-width limit.


## Other resources
There are many other resources that do a much better job at reviewing the NTK, including:
* [this blog post](https://www.eigentales.com/NTK/) for a visually intuitive explanation. 
* [this other post](https://lilianweng.github.io/posts/2022-09-08-ntk/) for a more rigorous walkthrough of the NTK.
* a series of tutorial blogs on the NTK by RBC Borealis, starting from [linear models](https://rbcborealis.com/research-blogs/gradient-flow/), moving on to [neural networks](https://rbcborealis.com/research-blogs/the-neural-tangent-kernel/), and concluding with [its applications](https://rbcborealis.com/research-blogs/neural-tangent-kernel-applications/).
* this [lecture video](https://www.youtube.com/watch?v=DObobAnELkU&ab_channel=SoheilFeizi) on the NTK.


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

<p> <font size="3"> <a id="5">[5]</a> 
Arora, S., Du, S. S., Hu, W., Li, Z., Salakhutdinov, R. R., & Wang, R. (2019). On exact computation with an infinitely wide neural net. <i>Advances in neural information processing systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="6">[6]</a> 
Yang, G., & Hu, E. J. (2021, July). Tensor programs iv: Feature learning in infinite-width neural networks. <i>In International Conference on Machine Learning</i> (pp. 11727-11737). PMLR.</font> </p>

[^1]: Note that, for a linear model of the form $$f(X) = WX$$, the NTK is constant during training, depending only on the empirical input covariance, i.e. $$XX^T$$.
