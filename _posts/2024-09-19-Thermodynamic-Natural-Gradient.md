---
title: '💥 Thermodynamic Natural Gradient Descent'
date: 2024-09-19
permalink: /posts/2024/09/19/Thermodynamic-Natural-Gradient/
tags:
  - Machine Learning
  - Natural Gradient Descent
  - Fisher Information
  - Second-order Methods
  - Thermodynamic AI
  - Normal Computing

---

I recently came across the paper “Thermodynamic Natural Gradient Descent” by [Normal Computing](https://www.normalcomputing.com/). 
I found this paper very interesting, so below is my brief take on it.

>  📖 **TL;DR**: *they show that natural gradient descent (NGD) can be run at a speed approaching that of first-order methods 
> like standard GD with competitive performance using a combination of digital and analog hardware.*

For the authors' summary:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">We recently released our latest paper from <a href="https://twitter.com/NormalComputing?ref_src=twsrc%5Etfw">@NormalComputing</a> on &quot;Thermodynamic Natural Gradient Descent&quot; (TNGD), showcasing a groundbreaking approach to AI optimization. <br><br>But how does it work?<br><br>TNGD combines the power of GPUs and innovative thermodynamic computers called… <a href="https://t.co/GBTRTjgIWI">pic.twitter.com/GBTRTjgIWI</a></p>&mdash; Normal Computing 🧠🌡️ (@NormalComputing) <a href="https://twitter.com/NormalComputing/status/1800918542755438862?ref_src=twsrc%5Etfw">June 12, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## ✋ Epistemic check
* Overall, I found the work to be a novel contribution, showing a strong proof of concept for a much faster second-order 
optimiser on a clever digital-analog framework.
* That being said, I am not 100% familiar with the all approximations of the Fisher matrix used in this work and their implications.
* I also did not fully follow all the theoretical complexity calculations.

## Proposal
Against the background of the increasing cost of training AI models, the authors introduce a more efficient method for 
training neural networks with natural gradient descent (NGD) called "thermodynamic NGD" (TNGD).

They combine a GPU (digital) device with a “thermodynamic” or stochastic (analog) device. 
Unlike current inference accelerators, their method is architecture-agnostic (i.e. the hardware doesn't need to embed 
the model architecture), and they build on their previous work showing that thermodynamic computing (i.e. computing with
thermodynamic processes) can accelerate linear algebra operations like matrix inversion, exponentials etc. 

They empirically show that TNGD is competitive with standard optimisers including Adam on classification and language 
fine-tuning tasks.

## Natural gradient descent in a nutshell
I won’t explain NGD in detail here as there are many other good sources for that (e.g. [Martens, 2020](https://www.jmlr.org/papers/v21/17-678.html)). 
Briefly, NGD performs the following weight update

$$
g = F^{-1} \nabla \ell(\theta)
$$

where $\nabla \ell(\theta)$ is the gradient of some loss with respect to model parameters $\theta$, and $F$ is the 
Fisher information matrix. The Fisher matrix is defined as the variance of the gradient of the log-likelihood (a.k.a. 
the "score") or the expected negative Hessian of the log-likelihood. Intuitively, the Fisher tells you how much 
information some data gives you about the correct value of unknown parameters.

Given the high compute and memory cost of forming the Fisher for neural nets (quadratic in the number of parameters), 
there are many simplifications and approximations that are made in practice. First, since we do not have access to the 
data distribution, we estimate the Fisher from a data batch, and this is known as the empirical Fisher. A further 
approximation is the generalised Gauss-Newton matrix $J_f H_L J_f$ where $J_f$ is the Jacobian of the model and $H_L$ is 
the Hessian of the loss with respect to the model prediction. In overparamterised settings where the batch and output 
dimension are much smaller than the number of parameters, one can dampen the Fisher ($F + \lambda I$) and also use a 
trick called the Woodbury identity to compute the inverse Fisher-vector product $F_{-1}v$.

## 🥩 The meat: Thermodynamic NGD
The authors build on their previous work showing that a linear system can be solved faster on a thermodynamic device called 
a stochastic processing unit (SPU) than on standard digital hardware. They did this by running an Ornstein–Uhlenbeck (OU) 
process given by the stochastic differential equation (SDE)

$$
\dot{x} = -(Ax - b) + \mathcal{N}(0, 2 \beta^{-1})
$$

where $A$ is a positive matrix and $\beta>0$ controls the noise. One just needs to let the SPU equilibrate, at which 
point $x$ has the following Boltzmann distribution

$$
x \sim \mathcal{N}(A^{-1}b, \beta^{-1}A^{-1})
$$

where we see that the mean of this distribution $\color{blue}A^{-1}b$ is the solution of the linear system $Ax = b$. 
Without showing the maths, the authors derive the SDE for NGD with their approximations, meaning that the average of that
process should give an estimate of the NG. They point out that in practice they don't need to wait for convergence but 
can take samples after some time steps $T$ without significantly affecting performance. Nicely, they also note that if one 
chooses the gradient at time 0 to be the loss gradient, one can interpolate between SGD and NGD as a function of $t$.

TODO!

## Empirical results

The authors first run a few simulations to validate their theoretical complexity calculations, showing that (as predicted)
the cost of TNGD scales well with the number of parameters $N$ but badly with the output dimension $d_{out}$ compared to
standard NGD and other approximations.

They then test TNGD on two tasks: classification on MNIST, and language fine-tuning. On MNIST, they find that their method
converges faster than Adam with practically the same performance and that TNGD is about only l2x slower per iteration 
compared to Adam on a A100 GPU.

Consistent with the interpretation of fewer iterations being closer to SGD, more iterations lead to better performance 
until it approaches that of exact NGD. Interestingly, asynchronous updates (i.e. with a small time delay) between the 
devices lead to better performance than exact NGD.

On the language task, TNGD performs better than Adam only when combined with it. As on MNIST, more iterations lead to 
better performance.

## 💭 Concluding thoughts

The motivation behind using a second-order method is that it will converge faster. Like for the more general field, 
the main block behind the adoption of these higher-order algorithms is the more expensive computational costs. 
However, it is worth noting that the whole field of higher-order optimisers (including NGD) is based on the premise 
that they will lead to equal or better-generalising solutions, for which we have no theoretical guarantees for practical 
settings.
