---
title: 'Energy-based Transformers'
date: 2025-07-18
permalink: /posts/2025/07/18/Energy-based-Transformers/
tags:
  - 

---

>  📖 **TL;DR**: *Energy-based Transformers (EBTs) learn a scalar energy 
function parameterised by a transformer. Empirically, EBTs show promising 
scaling and reasoning properties on both language and vision tasks.*

This is a short note on the recent paper [Energy-Based Transformers are 
Scalable Learners and Thinkers](https://arxiv.org/abs/2507.02092). 

Current approaches to inference-time computation are limited to specific 
modalities such as text, verifiable domains such as maths and coding, or need
supervision in the form of verifiable rewards. Motivated by these limitations, 
the authors introduce **Energy-based Transformers** (EBTs). This is basically a 
transformer $$\theta$$ that takes both a context sequence $$x$$ and candidate 
prediction $$\hat{y}$$ as input and outputs a single scalar energy 
$$E_\theta(x, \hat{y})$$, where this energy represents an unnormalised 
probability and can be thought of as a measure of the *compatibility* between 
the context and the prediction. 

Like other energy-based models (EBMs), EBTs allow one to frame test-time 
***inference as an optimisation problem***, where one can improve the candidate 
prediction by a process of gradient-based energy minimisation
<a name="eq1"></a>

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
