---
title: '♾️ Infinite Widths Part I: Neural Networks as Gaussian Processes'
date: 2024-11-16
permalink: /posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Gaussian Processes
  - Bayesian Inference
  - Bayesian Neural Networks 
  - Central Limit Theorem
  - Deep Information Propagation

---

This is the first post of a short series on the infinite-width limits of deep neural networks (DNNs). We start by 
reviewing the correspondence between neural networks and Gaussian Processes (GPs).

<p align="center" style="text-align:center;">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/nngp.gif" style="zoom:65%;" />
    <span style="color:grey; font-size:large;">
        <b>Visualising the NNGP correspondence.</b> 
        Empirical distribution of the 2D output of a 3-layer neural network while increasing the width 
        by a factor of 2.
    </span>
</p>

## TL;DR
> **Neural Network as Gaussian Process (NNGP)**: *At initialisation, the output distribution of a neural network 
> converges to a multivariate Gaussian as its width goes to infinity.*

In other words, in the infinite-width limit, predicting with a random neural network is the same as sampling from a 
specific GP.

## Brief history
The result was first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf) for one-hidden-layer neural 
networks and more recently extended to deeper networks [[2]](#2)[[3]](#3) including convolutional [[4]](#4)[[5]](#5) and
transformer [[6]](#6) architectures. In fact, it turns out that any composition of matrix multiplications and element-wise 
functions can be shown to admit a GP in the infinite-width limit [[7]](#7).

## What is a Gaussian Process (GP)?
A GP is a Gaussian distribution over a function. More precisely, the function output for a set of inputs 
$$\{f(x_i, \dots, f(x_n)\}$$ is jointly distributed as a multivariate Gaussian with mean 
$$\boldsymbol{\mu}$$ and covariance or kernel $$K$$, denoted as $$f \sim \mathcal{GP}(\boldsymbol{\mu}, K)$$. See this
[Distill post](https://distill.pub/2019/visual-exploration-gaussian-processes/) for a beautiful explanation of GPs. 

## Intuition behind the NNGP result
There are different ways to prove this result, to different levels of rigour and generality. Here, we will focus
on the original derivation of [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf) for one-hidden-layer network of 
width $$N_\ell$$, before giving some intuition on the extension to deeper networks. Consider the $$i$$th neuron in the 
output layer

$$
z_i(x) = b_i^{(2)} + \sum_j^{N_1} W_{ij}^{(2)} h_j(x)
$$

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/one-hidden-net.png" style="zoom:65%;" />
</p>

where we denote the hidden layer post-activation as $$h_j(x) = \phi(b_i^{(1)} + \sum_{k}^{N_0} W_{jk}^{(1)} x_k)$$ 
with activation function $$\phi$$. All the weights and biases are initialised i.i.d. as 
$$b_i^{(l)} \sim \mathcal{N}(0, \sigma_b^2)$$ and $$W_{ij}^{(l)} \sim \mathcal{N}(0, \sigma_w^2/N_\ell)$$. Note that, 
similar to standard initialisations (e.g. LeCun), we rescale the variance of the weights by the width $$N_\ell$$ to 
avoid divergence when we will apply central limit theorem (CLT) arguments. We would like to understand the prior over 
functions induced by this prior over parameters.

The NNGP result follows from two key observations:
1. Even though they receive the same input $$x$$, all the hidden neurons $$h_j$$ are uncorrelated with each 
other because of independent parameters. (Note that this breaks down for deeper layers at finite width.)
2. Any output neuron $$z_i(x)$$ is a sum of iid random variables. Therefore, as 
$$N \rightarrow \infty$$, CLT tells us that $$z_i(x)$$ will converge to a Gaussian 
distribution. For multiple inputs, this will be a joint multivariate Gaussian, i.e. a GP. Note that the output neurons 
also become independent despite using the same "features" or inputs.

What are the mean and covariance of this GP? The mean is easy: since all the parameters are centered at initialisation, 
the mean of the GP is also zero.

$$
\boldsymbol{\mu}(x) = \mathbb{E}_\theta[z_i(x)] = 0
$$

where $$\theta$$ denotes the set of all parameters. The covariance is a little bit more involved

$$
K(x, x') = \mathbb{E}_\theta[z_i(x)z_i(x')] = \sigma^2_b + \sigma^2_w \mathbb{E}_\theta[h_j(x)(h_j(x')]
$$

where we used the fact that the weights are independent for different inputs. We see that, in addition to the 
initialisation variances, the kernel depends on the activation function $$\phi$$. For some nonlinearities we can 
compute the kernel analytically, while for others we can simply solve a 2D integral.

This is the key result first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf). More recent 
works showed that this argument can be iterated through the layers by conditioning on the GP of the previous layer 
[[2]](#2)

$$
K^l(x, x') = \sigma^2_b + \sigma^2_w \mathbb{E}_{z_i^{l-1}\sim \mathcal{GP}(\mathbf{0}, K^{l-1})}[\phi(z_i^{l-1}(x))\phi(z_i^{l-1}(x'))]
$$

with initial condition $$K^0(x, x') = \sigma^2_b + \frac{\sigma^2_w}{N_0} x x'$$.

## Why does this matter?
This is one of the first results giving us a better insight into the highly dimensional functions computed by DNNs. 
Indeed, similar analyses had been previously carried out to characterise the "signal propagation" in random networks at 
initialisation [[8]](#8)[[9]](#9). Intuitively, if you have two inputs $$x$$ and $$x'$$, you don't want their 
correlation to vanish or explode as they move through network, which would in turn lead to vanishing or exploding 
gradients, respectively.

In addition, since an infinite-width DNN is a GP, one can perform exact Bayesian inference including uncertainty 
estimates without ever instantiating or training a neural network. These NNGPs have been found to outperform simple 
finite SGD-trained fully connected networks [[2]](#2). For convolutional networks, however, the performance of NNGPs 
drops compared to their finite width counterparts, as useful inductive biases such as translation equivariance seem to 
be washed away in this limit [[4]](#4).

In the next post of this series on the infinite-width limits of DNNs, we will look at what happens during training.


## References

<p> <font size="3"> <a id="1">[1]</a> 
R. M. Neal. Priors for infinite networks (tech. rep. no. crg-tr-94-1). <i>University of Toronto</i>, 1994</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Lee, J., Bahri, Y., Novak, R., Schoenholz, S. S., Pennington, J., & Sohl-Dickstein, J. (2017). Deep neural networks as 
gaussian processes. <i>arXiv preprint arXiv:1711.00165.</i> </font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Matthews, A. G. D. G., Rowland, M., Hron, J., Turner, R. E., & Ghahramani, Z. (2018). Gaussian process behaviour in wide 
deep neural networks. <i>arXiv preprint arXiv:1804.11271.</i> </font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Novak, R., Xiao, L., Lee, J., Bahri, Y., Yang, G., Hron, J., ... & Sohl-Dickstein, J. (2018). Bayesian deep convolutional 
networks with many channels are gaussian processes. <i>arXiv preprint arXiv:1810.05148.</i> </font> </p>

<p> <font size="3"> <a id="5">[5]</a> 
Garriga-Alonso, A., Rasmussen, C. E., & Aitchison, L. (2018). Deep convolutional networks as shallow gaussian processes. 
<i>arXiv preprint arXiv:1808.05587.</i> </font> </p>

<p> <font size="3"> <a id="6">[6]</a> 
Hron, J., Bahri, Y., Sohl-Dickstein, J., & Novak, R. (2020). Infinite attention: NNGP and NTK for deep attention 
networks. <i>In International Conference on Machine Learning</i> (pp. 4376-4386). PMLR.</font> </p>

<p> <font size="3"> <a id="7">[7]</a> 
Yang, G. (2019). Wide feedforward or recurrent neural networks of any architecture are gaussian processes. <i>Advances 
in Neural Information Processing Systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="8">[8]</a> 
Schoenholz, S. S., Gilmer, J., Ganguli, S., & Sohl-Dickstein, J. (2016). Deep information propagation. <i>arXiv preprint 
arXiv:1611.01232.</i> </font> </p>

<p> <font size="3"> <a id="9">[9]</a> 
Xiao, L., Bahri, Y., Sohl-Dickstein, J., Schoenholz, S., & Pennington, J. (2018). Dynamical isometry and a mean field 
theory of cnns: How to train 10,000-layer vanilla convolutional neural networks. <i>In International Conference on
Machine Learning</i> (pp. 5393-5402). PMLR.</font> </p>
