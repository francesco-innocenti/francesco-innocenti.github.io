---
title: '♾️ Infinite Widths Part II: Neural Networks as Kernel Methods'
date: 2024-12-30
permalink: /posts/2024/12/30/Infinite-Widths-Part-II-Neural-Networks-as-Kernel-Methods/
tags:
  - Deep Neural Networks
  - Infinite Width Limit
  - Neural Tangent Kernel
  - Kernel Regression
  - Lazy Regime

---

This is the first post of a short series on the infinite-width limits of deep neural networks (DNNs). We start by 
reviewing the correspondence between neural networks and Gaussian Processes (GPs).

## Key idea
> **Neural Network as Gaussian Process (NNGP)**: *At initialisation, the output distribution of a neural network 
> converges to an architecture-dependent Gaussian process as its width goes to infinity.*

In other words, in the infinite-width limit, the neural network function is the same as sampling from a Gaussian process.
This result can be roughly thought of as the infinite-width limit the "feedforward pass" of a random neural network
(though it can be extended to the first "backward pass").

## Brief history
The result was first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf) for one-hidden-layer neural 
networks and more recently extended to deeper networks [[2]](#2)[[3]](#3) including convolutional 
architectures [[4]](#4)[[5]](#5). In fact, it turns out that any composition of matrix multiplications and element-wise 
functions can be shown to admit a GP in the infinite-width limit [[6]](#6).

## What is a Gaussian Process (GP)?
A GP is a Gaussian distribution over a function. More precisely, the function output for a set of inputs is jointly 
distributed as a multivariate Gaussian with mean and covariance $$\boldsymbol{\mu}$$ and $$K$$, denoted as 
$$\mathcal{GP}(\mu, K)$$.

## NNGP result
Let's start with a one-hidden-layer network of width $$N$$. Consider the $$i$$th neuron in the output layer

$$
z_i(\mathbf{x}) = b_i^2 + \sum_j^N W_{ij}^2 h_j(\mathbf{x})
$$

<p align="center">
    <img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/one-hidden-net.png" style="zoom:65%;" />
</p>

where we denote hidden layer post-activation as $$h_j(\mathbf{x}) = \phi(b_i^1 \sum_{k}^D W_{jk}^1 x_k)$$ with 
activation function $$\phi$$. All the weights and biases are initialised i.i.d. as 
$$b_i^l \sim \mathcal{N}(0, \sigma_b^2)$$ and $$W_{ij}^l \sim \mathcal{N}(0, \sigma_w^2/N)$$. (The weight variance 
scaling comes from applying the central limit theorem as we now show.) $$\boldsymbol{\theta}$$ will denote the set of 
all parameters.

The NNGP result follows from two key observations:
1. Any hidden neuron $$h_j(\mathbf{x})$$ is independent of other hidden neurons $$h_j'(\mathbf{x})$$ for $$j \neq j'$$ 
because all the parameters (weights and biases) are iid and the activation is applied element-wise. So even though all 
hidden neurons receive the same input, they are uncorrelated because of independent parameters. Note that this breaks 
down for deeper layers at finite width.
2. Any output neuron $$z_i(\mathbf{x})$$ is a sum of iid random variables. Therefore, as $$N \rightarrow \infty$$, the 
CLT tells us that $$z_i(\mathbf{x})$$ will converge to a Gaussian distribution, which will be a joint multivariate for 
multiple inputs. In the infinite-width limit, a random neural network is a GP.

What are the mean and covariance of this GP? The mean is easy: since all the parameters are initialised with zero mean, 
the mean of the GP is also zero.

$$
\mu(\mathbf{x}) = \mathbb{E}_{\boldsymbol{\theta}}[z_i(\mathbf{x})] = 0
$$

The covariance is a little bit more involved

$$
K(\mathbf{x}, \mathbf{x}') = \mathbb{E}_{\boldsymbol{\theta}}[z_i(\mathbf{x})z_i(\mathbf{x}')] = \sigma^2_b + \sigma^2_w \mathbb{E}_{\boldsymbol{\theta}}[h_j(\mathbf{x})(h_{j'}(\mathbf{x}')]
$$

where we have used the fact that the weights independent for different inputs. We see that the covariance therefore 
depends on the initialisation variances and the specific activation function. For some nonlinearities we can compute 
the kernel analytically, for others this simply involves solving a 2D integral.

This is essentially the result first proved by [Neal (1994)](https://glizen.com/radfordneal/ftp/pin.pdf). More recent 
works showed that this argument can be iterated through the layers by conditioning on the GP of the previous layer, and 
the GP kernel can be expressed as a composition of layer kernels.

## Why does this matter?
This is one of the first results giving us a better insight into the highly dimensional functions computed by neural 
networks. It also enables us to predict whether networks can be trained by studying the signal propagation throughout
them. Plus, one can also do exact bayesian inference/model with GPs.

In the next post of this series on infinite-width limits of NNs, we will look 
at what happens during training.


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
Yang, G. (2019). Wide feedforward or recurrent neural networks of any architecture are gaussian processes. <i>Advances 
in Neural Information Processing Systems, 32.</i> </font> </p>
