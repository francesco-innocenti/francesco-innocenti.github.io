---
title: '♾️ Infinite Widths Part I: Neural Networks as Gaussian Processes'
date: 2024-11-16
permalink: /posts/2024/11/16/Infinite-Widths-Part-I-Neural-Networks-as-Gaussian-Processes/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Gaussian Processes

---

This is the first post of a short series on the infinite-width limits of deep neural networks (DNNs). We start by 
reviewing the correspondence between neural networks and Gaussian Processes (GPs).

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/nngp.gif" style="zoom:65%;" />
</p>

## Key idea
> **Neural Network as Gaussian Process (NNGP)**: *At initialisation, the output distribution of a neural network 
> converges to a multivariate Gaussian as its width goes to infinity.*

In other words, in the infinite-width limit, predicting with a neural network is the same as sampling from a specific GP.

## Brief history
The result was first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf) for one-hidden-layer neural 
networks and more recently extended to deeper networks [[2]](#2)[[3]](#3) including convolutional [[4]](#4)[[5]](#5) and
transformer [[6]](#6) architectures. In fact, it turns out that any composition of matrix multiplications and element-wise 
functions can be shown to admit a GP in the infinite-width limit [[7]](#7).

## What is a Gaussian Process (GP)?
A GP is a Gaussian distribution over a function. More precisely, the function output for a set of inputs is jointly 
distributed as a multivariate Gaussian with mean $$\boldsymbol{\mu}$$  and covariance or kernel $$K$$, denoted as 
$$\mathcal{GP}(\boldsymbol{\mu}, K)$$.

## Intuition behind the NNGP result
Let's start with a one-hidden-layer network of width $$n$$. Consider the $$i$$th neuron in the output layer

$$
z_i(\mathbf{x}) = b_i^{(2)} + \sum_j^n W_{ij}^{(2)} h_j(\mathbf{x})
$$

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/one-hidden-net.png" style="zoom:65%;" />
</p>

where we denote the hidden layer post-activation as $$h_j(\mathbf{x}) = \phi(b_i^{(1)} + \sum_{k}^D W_{jk}^{(1)} x_k)$$ 
with activation function $$\phi$$. All the weights and biases are initialised i.i.d. as 
$$b_i^{(l)} \sim \mathcal{N}(0, \sigma_b^2)$$ and $$W_{ij}^{(l)} \sim \mathcal{N}(0, \sigma_w^2/n)$$. 
$$\boldsymbol{\theta}$$ will denote the set of all parameters. We would like to understand the prior over functions
induced by this prior over parameters.

The NNGP result follows from two key observations:
1. Any hidden neuron $$h_j(\mathbf{x})$$ is independent of other hidden neurons $$h_j'(\mathbf{x})$$ for $$j \neq j'$$ 
because all the parameters are iid (and the activation is applied element-wise). So even though all hidden neurons 
receive the same input, they are uncorrelated because of independent parameters. (Note that this breaks down for deeper 
layers at finite width.)
2. Any output neuron $$z_i(\mathbf{x})$$ is a sum of iid random variables. Therefore, the central limit theorem tells us 
that, as $$n \rightarrow \infty$$, $$z_i(\mathbf{x})$$ will converge to a Gaussian distribution. For multiple inputs, 
this will be a joint multivariate Gaussian, i.e. a GP. Note that the output neurons also become independent despite
using the same features.

What are the mean and covariance of this GP? The mean is easy: since all the parameters are initialised with zero mean, 
the mean of the GP is also zero.

$$
\boldsymbol{\mu}(\mathbf{x}) = \mathbb{E}_{\boldsymbol{\theta}}[z_i(\mathbf{x})] = 0
$$

The covariance is a little bit more involved

$$
K(\mathbf{x}, \mathbf{x}') = \mathbb{E}_{\boldsymbol{\theta}}[z_i(\mathbf{x})z_i(\mathbf{x}')] = \sigma^2_b + \sigma^2_w \mathbb{E}_{\boldsymbol{\theta}}[h_j(\mathbf{x})(h_{j'}(\mathbf{x}')]
$$

where we have used the fact that the weights are independent for different inputs. We see that, in addition to the
the initialisation variances, the kernel depends on the activation function $$\phi$$. For some nonlinearities we can 
compute the kernel analytically, while for others we can simply solve a 2D integral.

This is the key result first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf). More recent 
works showed that this argument can be iterated through the layers by conditioning on the GP of the previous layer 
[[2]](#2)

$$
K(\mathbf{x}, \mathbf{x}')^l = \mathbb{E}_{\boldsymbol{\theta}}[z_i^l(\mathbf{x})z_i^l(\mathbf{x}')] = \sigma^2_b + \sigma^2_w \mathbb{E}_{z_i^{l-1}\sim \mathcal{GP}(\mathbf{0}, K^{l-1})}[\phi(z_i^l(\mathbf{x}))\phi(z_i^l(\mathbf{x}'))]
$$

and that the GP kernel can be expressed as a composition of layer kernels.

## Why does this matter?
This is one of the first results giving us a better insight into the highly dimensional functions computed by DNNs. 
Indeed, similar analyses had been previously carried out to characterise the "signal propagation" in random networks at 
initialisation [[8]](#8)[[9]](#9). Intuitively, if you have two inputs $x$ and $x'$, we don't want their correlation 
to vanish or explode as they move through network, which would in turn lead to vanishing and exploding gradients, 
respectively.

In addition, since an infinite-width DNN is a GP, one can perform exact Bayesian inference including uncertainty 
estimates without training a neural network. While far from being an accurate model of DNNs, these GPs have been found 
outperform trained fully connected networks at finite width [[2]](#2).

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
