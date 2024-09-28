---
title: '💥 Thermodynamic Natural Gradient Descent'
date: 2024-07-19
permalink: /posts/2024/07/19/Thermodynamic-Natural-Gradient/
tags:
  - Machine Learning
  - Natural Gradient Descent
  - Fisher Information
  - Second-order Methods
  - Thermodynamic AI
  - Normal Computing

---

I recently came across this paper [Thermodynamic Natural Gradient Descent](https://arxiv.org/abs/2405.13817) by 
[Normal Computing](https://www.normalcomputing.com/). I found it very interesting, so below is my brief take on it.

>  📖 **TL;DR**: *they show that natural gradient descent (NGD) can be run at a speed approaching that of first-order methods 
> like standard GD with competitive performance using a combination of digital and analog hardware.*

For the authors' summary, see:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">We recently released our latest paper from <a href="https://twitter.com/NormalComputing?ref_src=twsrc%5Etfw">@NormalComputing</a> on &quot;Thermodynamic Natural Gradient Descent&quot; (TNGD), showcasing a groundbreaking approach to AI optimization. <br><br>But how does it work?<br><br>TNGD combines the power of GPUs and innovative thermodynamic computers called… <a href="https://t.co/GBTRTjgIWI">pic.twitter.com/GBTRTjgIWI</a></p>&mdash; Normal Computing 🧠🌡️ (@NormalComputing) <a href="https://twitter.com/NormalComputing/status/1800918542755438862?ref_src=twsrc%5Etfw">June 12, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## ✋ Epistemic check
* Overall, I found the work to be a novel contribution, showing a strong proof of concept for a much faster second-order 
optimiser on a clever digital-analog framework.
* That being said, I am not 100% familiar with the all approximations of the Fisher matrix used in this work and their implications.
* I also did not fully follow all the theoretical complexity calculations.

## Proposal
Against the background of the increasing cost of training AI models, the authors introduce a more efficient method for 
training neural networks with natural gradient descent (NGD) called "thermodynamic NGD" (TNGD).

They essentially combine a GPU (digital) device with a “thermodynamic” or stochastic (analog) device (more details below). 
Unlike current inference accelerators, their method is architecture-agnostic (i.e. the hardware doesn't need to embed 
the model architecture), and they build on their previous work showing that analog computation can accelerate linear 
algebra operations like matrix inversion, exponentials etc. 

They empirically show that TNGD is competitive with standard first-order optimisers including Adam on classification and 
language fine-tuning tasks.

## Natural gradient descent in a nutshell
I won’t explain NGD in detail here as there are many other good sources for that (e.g. see [Martens, 2020](https://www.jmlr.org/papers/v21/17-678.html)). 
Briefly, NGD performs the following weight update

$$
g = F^{-1} \nabla \ell(\theta)
$$

where $$\nabla \ell(\theta)$$ is the gradient of some loss with respect to model parameters $$\theta$$, and $$F$$ is the 
Fisher information matrix. The Fisher matrix is defined as the variance of the gradient of the log-likelihood (a.k.a. 
the "score") or the expected negative Hessian of the log-likelihood. Intuitively, the Fisher tells you how much 
information some data gives you about the correct value of unknown parameters.

Given the high compute and memory cost of forming the Fisher for neural nets (quadratic in the number of parameters), 
there are many simplifications and approximations that are made in practice. First, since we do not have access to the 
data distribution, we estimate the Fisher from a data batch, and this is known as the empirical Fisher. A further 
approximation is the generalised Gauss-Newton matrix $$J_f H_L J_f$$ where $$J_f$$ is the Jacobian of the model and $$H_L$$ is 
the Hessian of the loss with respect to the model prediction. In overparamterised settings where the batch and output 
dimension are much smaller than the number of parameters, one can dampen the Fisher ($$F + \lambda I$$) and also use a 
trick called the Woodbury identity to compute the inverse Fisher-vector product $$F^{-1}v$$.

## 🥩 The meat: Thermodynamic NGD
The authors build on their previous work showing that a linear system can be solved faster on a thermodynamic device called 
a stochastic processing unit (SPU) than on standard digital hardware. They did this by running an Ornstein–Uhlenbeck (OU) 
process given by the stochastic differential equation (SDE)

$$
\dot{x} = -(Ax - b) + \mathcal{N}(0, 2 \beta^{-1})
$$

where $$A$$ is a positive matrix and $$\beta>0$$ controls the noise. One just needs to let the SPU equilibrate, at which 
point $$x$$ has the following Boltzmann distribution

$$
x \sim \mathcal{N}(\color{blue}A^{-1}b\color{black}, \beta^{-1}A^{-1})
$$

where we see that the mean of this distribution $$\color{blue}A^{-1}b$$ is the solution of the linear system $$Ax = b$$. 
Without showing the maths, the authors basically derive an SDE for NGD with the approximations mentioned above. 

Given this, they then employ a very clever hybrid hardware setup. They use a GPU to compute the loss gradient and 
approximate Fisher. The GPU then communicates with an SPU to run the process dynamics to equilibrium to get an estimate 
of the natural gradient. They point out that in practice they don't need to wait for convergence but can take samples 
after some time steps $$T$$ without significantly affecting performance. Nicely, they also note that if one chooses the 
gradient at the first step $$t=0$$ to be the loss gradient, one can interpolate between SGD and NGD as a function of $$t$$.

## Empirical results

The authors first run a few simulations to validate their theoretical complexity calculations, showing that (as predicted)
the cost of TNGD scales well with the number of parameters $$N$$ but badly with the output dimension $$d_{out}$$ compared to
standard NGD and other approximations.

They then test TNGD on two tasks: classification on MNIST, and language fine-tuning. On MNIST, they find that their method
converges faster than Adam with practically the same performance and that TNGD is about only 2x slower per iteration 
compared to Adam on a A100 GPU.

Consistent with the interpretation of fewer iterations being closer to SGD, more iterations lead to better performance 
until it approaches that of exact NGD. Interestingly, asynchronous updates (i.e. with a small time delay) between the 
devices lead to better performance than exact NGD.

On the language task, TNGD performs better than Adam only when combined with it. As on MNIST, more iterations lead to 
better performance.

## 💭 Concluding thoughts

Overall, I found the hybrid hardware setup that allows the authors to make NGD competitive in speed (and performance)
with first-order methods very innovative. Below I include a couple of broader points about this work.

First, I wonder whether the theory behind the SDE could be extended to approximately solve non-linear systems too. This 
would be very exciting since energy-based algorithms like predictive coding (which I work on, see my previous 
[blog post](https://francesco-innocenti.github.io/posts/2023/08/10/PC-as-a-2nd-Order-Method/)) could potentially be run 
much faster.

A more general point is about second-order methods including NGD. While there is empirical evidence---and in some simplistic
cases theoretical guarantees---that second-order methods can converge faster than standard optimisers, we do not know 
whether these algorithms ultimately converge to a better-generalising solution. This intimate relationship between
optimisation and generalisation is a fundamental unanswered question in deep learning theory, and while it does not 
matter from a practical perspective ("if it performs well, then don't worry about it"), it is worth bearing in mind.

## References

<p> <font size="3"> <a id="1">[1]</a> 
Donatella, K., Duffield, S., Aifer, M., Melanson, D., Crooks, G., & Coles, P. J. (2024). Thermodynamic Natural Gradient Descent. <i>arXiv preprint arXiv:2405.13817</i>.</font> </p>

<p> <font size="3"> <a id="1">[2]</a> 
Martens, J. (2020). New insights and perspectives on the natural gradient method. <i>Journal of Machine Learning Research, 21</i></font>(146), 1-76.</p>
