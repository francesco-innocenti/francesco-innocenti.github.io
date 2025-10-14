---
title: 'Energy-based Transformers'
date: 2025-07-18
permalink: /posts/2025/07/18/Energy-based-Transformers/
tags:
  - transformers
  - energy-based models
  - energy-based transformers
  - system-2 thinking
  - inference as optimisation

---

>  📖 **TL;DR**: *Energy-based Transformers (EBTs) learn a scalar energy 
function parameterised by a transformer. Empirically, EBTs show promising 
scaling and reasoning properties on both language and vision tasks.*

This is a short note on the recent paper [Energy-Based Transformers are 
Scalable Learners and Thinkers](https://arxiv.org/abs/2507.02092) [[1]](#1), 
including a potential research idea. 


## EBTs: an overview
Current approaches to inference-time computation are limited to specific 
modalities such as text, verifiable domains such as maths and coding, or need
supervision in the form of verifiable rewards. Motivated by these limitations, 
the authors introduce **Energy-based Transformers** (EBTs). This is basically a 
transformer $$\theta$$ that takes both a context sequence $$x$$ and candidate 
prediction $$\hat{y}$$ as input and outputs a single scalar energy 
$$E_\theta(x, \hat{y})$$, where this energy represents an unnormalised 
probability and can be thought of as a measure of the *compatibility* between 
the context and the prediction. 
<a name="eq1"></a>

Like other energy-based models (EBMs), EBTs allow one to frame test-time 
***inference as an optimisation problem***, where one can improve the candidate 
prediction by a process of gradient-based energy minimisation

$$
\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}} E_\theta(x, \hat{y}_i).
$$

What's cool about this is that it's similar to the iterative inference procedure 
of many energy-based local learning algorithms such as predictive coding [[2]](#2) 
and equilibrium propagation. Indeed, EBTs can be roughly seen as predictive 
coding networks with a "single  layer" (where that layer is a transformer) with 
only part of the model input (prediction) unclamped. In contrast to standard 
predictive coding models, this means (i) that only the predictions (as 
opposed to all the network nodes) are updated, and (ii) that the inference 
gradient is non-local and therefore commputed using standard backpropagation. 
While this allows for higher model expressivity, it leads to expensive 
computation of the weight gradients as we'll see next.

At (ideally) convergence of the inference dynamics ([Eq. 1](#eq1)), say after 
$$N$$ steps, we compute some loss between the converged predictions and ground 
truths $$\mathcal{L}(\hat{y}_N, y)$$. The parameters are then updated using the 
gradient of the loss with respect to the weights

$$
\Delta \theta \propto - \nabla_\theta \mathcal{L}(\hat{y}_N(\theta), y).
$$

Importantly, a naive way of computing this gradient as used by the authors is to backpropagate through the entire inference process ([Eq. 1](#eq1)), which we 
emphasised by making explicit the dependence of the converged predictions on the 
parameters $$\hat{y}(\theta)$$. Note that, unlike in predictive coding, we 
cannot treat the converged predictions as a constant because the loss does not 
explicitly depend on the parameters, only implicitly through the inference 
process.


## A research idea: leveraging implicit gradients
One way of getting around the issue of tracking gradients through the inner 
loop---common in bi-level optimisation---is to use implicit gradients, which 
have been previously used for meta-learning [[3]](#3) and deep equilibrium 
models [[4]](#4). In particular, we can leverage the implicit function theorem 
to directly compute gradients at the converged solution. We start by assuming 
convergence to a solution $$\hat{\mathbf{y}}^*$$ where

$$
\nabla_{\hat{\mathbf{y}}} E_{\boldsymbol{\theta}}(\mathbf{X}, \hat{\mathbf{y}}^*(\boldsymbol{\theta})) = 0.
$$

To simplify the notation, define $$g(\hat{\mathbf{y}}(\boldsymbol{\theta}), \boldsymbol{\theta}) := \nabla_{\hat{\mathbf{y}}} E_{\boldsymbol{\theta}}(\mathbf{X}, \hat{\mathbf{y}}(\boldsymbol{\theta}))$$ 
so that at a fixed point $$g(\hat{\mathbf{y}}^*(\boldsymbol{\theta}), \boldsymbol{\theta}) = 0$$. 
To determine the implicit gradient $$\partial \hat{\mathbf{y}} / \partial \boldsymbol{\theta}$$, 
we differentiate the optimality condition with respect to the parameters

$$
\begin{aligned}
\underbrace{\frac{\partial g}{\partial \boldsymbol{\theta}}}_{\text{direct effect}} + \underbrace{\frac{\partial g}{\partial \hat{\mathbf{y}}^*} \frac{\partial \hat{\mathbf{y}}^*}{\partial \boldsymbol{\theta}}}_{\text{indirect effect}}
&= \frac{\partial^2 E}{\partial \boldsymbol{\theta}\partial \hat{\mathbf{y}}^*} + \frac{\partial^2 E}{(\partial \hat{\mathbf{y}}^*)^2} \frac{\partial \hat{\mathbf{y}}^*}{\partial \boldsymbol{\theta}} = 0,
\end{aligned}
$$

noticing that it depends both directly and indirectly on $$\boldsymbol{\theta}$$. 
Now let $$\mathbf{G} := \frac{\partial^2 E}{\partial \boldsymbol{\theta}\partial \hat{\mathbf{y}}^*}$$ 
and $$\mathbf{H} := \frac{\partial^2 E}{(\partial \hat{\mathbf{y}}^*)^2}$$. 
Solving for $$\partial \hat{\mathbf{y}} / \partial \boldsymbol{\theta}$$ and 
assuming that the Hessian of the energy with respect to the predictions is 
invertible and the energy is continuously differentiable, we obtain

$$
\frac{\partial \hat{\mathbf{y}}^*}{\partial \boldsymbol{\theta}} = - \mathbf{H}^{-1}\mathbf{G}.
$$

Now we can simply apply the chain rule to get the parameter gradient of the loss 
and substitue our implicit gradient

$$
\begin{aligned}
\frac{\partial \mathcal{L}}{\partial \boldsymbol{\theta}} &= \frac{\partial \hat{\mathbf{y}}^*}{\partial \boldsymbol{\theta}}^T\frac{\partial \mathcal{L}}{\partial \hat{\mathbf{y}}^*} \\ 
&= - \mathbf{G}^T \left(\mathbf{H}^{-1}\right)^T \frac{\partial \mathcal{L}}{\partial \hat{\mathbf{y}}^*}
\end{aligned}
$$

where note that we only need to access the converged solution $$\mathbf{y}^*$$, 
thus avoiding differentiating through the inner optimisation problem. To avoid 
storing and directly inverting the energy Hessian with respect to the 
predictions, we can use Hessian-vector products and conjugate gradients (CG) 
which scales with the number of CG steps rather than inference steps.


## Concluding thoughts 
I was surprised that they were able to train such a complicated EBTs—and indeed 
the amount of tuning and regularisation required is non-trivial and could be 
further improved. Nevertheless, they managed to successfully scale 
different EBTs architectures to both language and vision tasks, showing that: 
* EBTs have promising scaling trends compared to standard transformers in terms 
of data, batch size, parameters, FLOPs and depth;
* EBTs can outperform transformers on reasoning tasks and diffusion models on 
image denoising while being more efficient; and
* EBTs also seem to outperform transformers on out-of-distribution tasks.


## References

<p> <font size="3"> <a id="1">[1]</a> 
Gladstone, A., Nanduru, G., Islam, M. M., Han, P., Ha, H., Chadha, A., ... & Iqbal, T. (2025). Energy-Based Transformers are Scalable Learners and Thinkers. <i>arXiv preprint arXiv:2507.02092.</i> </font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Millidge, B., Seth, A., & Buckley, C. L. (2021). Predictive coding: a theoretical and experimental review. <i>arXiv preprint arXiv:2107.12979.</i> </font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Rajeswaran, A., Finn, C., Kakade, S. M., & Levine, S. (2019). Meta-learning with implicit gradients. <i>Advances in neural information processing systems, 32.</i> </font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Bai, S., Kolter, J. Z., & Koltun, V. (2019). Deep equilibrium models. <i>Advances in neural information processing systems, 32.</i> </font> </p>
