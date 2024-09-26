---
title: '🧠 Predictive Coding as a 2<sup>nd</sup>-Order Method'
date: 2023-08-10
permalink: /posts/2023/08/10/PC-as-a-2nd-Order-Method/
tags:
  - Predictive Coding
  - Backpropagation
  - Trust Region
  - Second-Order
  - Fisher Information
  - Saddles
  - Local Learning
  - Inference Learning

---

>  📖 **TL;DR**: *Predictive coding implicitly performs a 2<sup>nd</sup>-order weight update via 1<sup>st</sup>-order (gradient) updates on neurons that in some cases allow it to converge faster than backpropagation with standard gradient descent.*

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/images/pc_trust_region_toy.png" width="700">

In this post, I explain my recent paper [Understanding Predictive Coding as a Second-Order Trust-Region Method](https://openreview.net/forum?id=x7PUpFKZ8M), which won a Best Paper Award at the [ICML 2023 Workshop on Localized Learning](https://sites.google.com/view/localized-learning-workshop). You can rewatch my talk [here](https://icml.cc/virtual/2023/workshop/21484). This is work in collaboration with Ryan Singh and my supervisor Christopher L. Buckley. I assume no knowledge of predictive coding and try to keep the mathematical notation to a minimum to get the main points across.

## Overview

1. [Predictive coding](#pc)
2. [A toy model](#toy)
3. [Theory](#theory)
4. [Some experiments](#exps)
5. [Concluding thoughts](#thoughts)

## <a name="pc"></a>Predictive coding

PC is one of many brain-inspired learning algorithms that can train deep neural networks as an alternative to backpropagation (BP) [[1]](#1). 
How does it work? How is it different from BP? The fundamental difference lies in how PC predicts an output for a given 
input–i.e. how it performs *inference* before learning. To see this, consider a deep neural network as a parameterised 
function $$f(x; \theta)$$ with input $$x$$ and parameters $$\theta$$. In BP, we start with a feedforward pass to get the 
network's prediction $$\hat{y} = f(x; \theta)$$ and compare it to the target $$y$$ via a loss function, for example the 
squared or $$\ell_2$$ loss

$$
\textbf{BP loss:} \quad \mathcal{L} = \big( y - f(x; \theta) \big)^2
$$

(where we ignore multiple data samples for simplicity). BP computes the gradient of the loss with respect to the 
parameters $$\nabla_\theta \mathcal{L}$$, which we can then use to minimise the loss with gradient descent (GD) 
<a name="eq2"></a>

$$
\textbf{Gradient descent:} \quad \Delta \theta \propto - \nabla_\theta \mathcal{L}
$$

We could of course perform more complicated updates, using adaptive optimisers like Adam, but we'll ignore these here. 
How does PC differ from this basic scheme? First, in PC you can think of each layer as trying to improve its prediction 
of the activity of the layer below, and we minimise an energy function which is a *sum of squared errors at each layer*

$$
\textbf{PC energy:} \quad \mathcal{F} = \sum_{\ell=1}^L \big( z_\ell - \phi_\ell(z_{\ell-1}; \theta_\ell) \big)^2
$$

where $$\phi_\ell$$ is some activation function, and the first and last layer are fixed to the input and output of the 
network, $$z_1 = x, z_L = y$$, respectively. Instead of a forward pass, during inference we perform GD on the energy 
*with respect to the activities*

$$
\textbf{PC inference:} \quad \Delta z_\ell \propto - \nabla_{z_\ell} \mathcal{F}
$$

Moreover, we don't do just one update, but run the dynamics until they converge to an equilibrium when 
$$\Delta z_\ell \approx 0$$. Intuitively, you can think of this process as the network trying to settle to a state that 
is most compatible with both the input and the target. For notational convenience, we will denote the energy at an 
inference equilibrium as $$\mathcal{F}^*$$. At this point, we update the weights, again using GD <a name="eq5"></a>

$$ 
\textbf{PC learning:} \quad \Delta \theta_\ell \propto - \nabla_{\theta_\ell} \mathcal{F}^*
$$

So we see that the key difference between BP (with standard GD, [Eq. 2](#eq2)) and PC ([Eq. 5](#eq5)) lies in their 
inference procedure, which leads to the minimisation of different objectives. While in BP we descend a global loss 
function, in PC we descend a sum of equilibrated local energies. If we want to understand how PC differs from BP, we 
therefore need to formally characterise the difference between the loss $$\mathcal{L}$$ and the equilibrated energy 
$$\mathcal{F}^*$$.

In a way, this shouldn't be surprising. Locality is a common feature of biologically plausible algorithms and so it's 
natural to expect local objectives to differ from global ones. However, as we will see, for PC 
*a 1<sup>st</sup>-order update on the equilibrated energy can be seen as performing some kind of 
2<sup>nd</sup>-order update on the loss*. In particular, we will show that PC inference–which makes use of only gradient 
updates–implicitly estimates $$2^{\text{nd}}$$-order information that is later used at learning. To build some intuition, 
we next look at a toy model.

## A toy model <a name="toy"></a>

Consider a toy network with a single hidden linear unit and two weights $$f(x) = w_2w_1x$$. Because we can flip the sign 
of any weight without changing the network function $$f(-\mathbf{w}) = f(\mathbf{w})$$, the loss landscape has a saddle 
point at the origin $$\mathbf{w} = (0, 0)$$, as shown below. <a name="fig1"></a>

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/bp_loss_land.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{1}}\notag$$</p>

It is well know that (S)GD is attracted to and slows down near saddles [[e.g. 2]](#2), and this is indeed what we 
observe from running it on our toy network from a random initialisation $$\mathbf{w}^0$$ and the loss gradient field 
$$\nabla_{\mathbf{w}} \mathcal{L}$$ more generally ([Figure 1](#fig1)). Now let's look at what happens with PC 
([Figure 2](#fig2)). We see that at initialisation ($$t = 0$$) the energy is the same as the loss[^1]; however, as 
inference proceeds, the geometry of the landscape changes along with the gradients. <a name="fig2"></a>

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/pc_energy_infer_dynamics.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{2}}\notag$$</p>

In particular, it looks like the overall landscape is flattened. We are now ready to do learning, i.e. to take a GD 
step on the equilibrated energy w.r.t. the weights. As shown in [Figure 3](#fig3), for the same initialisation PC 
clearly evades the saddle, taking a more direct path to the closest manifold of solutions. More generally, the 
equilibrated energy gradient field $$\nabla_\mathbf{w} \mathcal{F^*}$$ looks qualitatively more aligned with the 
solutions than that of the loss. <a name="fig3"></a>

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/pc_energy_land.png" style="zoom:15%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{3}}\notag$$</p>

In fact, it is easy to prove that in this toy model PC will always escape the saddle faster than BP. Intuitively, this 
is because the equilibrated energy shows both a flatter “trap” direction leading to the saddle and a more negatively 
curved “escape” direction leading to a valley of solutions. So what's going on here? Let's try to be more rigorous and 
do some theory.

## Theory <a name="theory"></a>

As mentioned above, to understand how PC differs from BP, it would be helpful if we could relate the energy to the loss. 
To do so, we can perform a second-order Taylor expansion of the energy around the *feedforward values* $$\hat{x}$$ which 
characterise the loss, arriving at (see paper for derivation) <a name="eq6"></a>

$$
\mathcal{F}(x) = \mathcal{L}(\hat{x}) + g_{\mathcal{L}}(\hat{x})^T \Delta x + \frac{1}{2} \Delta x^T \mathcal{I}(\hat{x}) \Delta x + \mathcal{O}(\Delta x^3)
$$

where $$\Delta x = (x - \hat{x})$$, $$g_{\mathcal{L}}(\hat{x})$$ denotes the gradient of the loss w.r.t. the activities, 
and $$\mathcal{I}(\hat{x})$$ is the Fisher information of the feedforward values w.r.t. the generative model defined by 
the PC network $$p(x, y)$$. Notably, this expression defines a trust-region problem on the BP loss in activity space 
with an adaptive $$2^{\text{nd}}$$-order geometry given by $$\mathcal{I}(\hat{x})$$ (see paper for more details). 
To study the inference equilibrium of PC, we can solve for the optimal solution at $$\partial \mathcal{F}/\partial x = 0$$ 
<a name="eq7"></a>

$$
\textbf{Approx. inference solution:} \quad \Delta x^* \approx - \mathcal{I}(\hat{x})^{-1} g_{\mathcal{L}}(\hat{x})
$$

and see that PC inference is essentially doing natural gradient on the BP loss w.r.t. the activities. Now, to see the 
impact of inference on learning, we can plug this solution ([Eq. 7](#eq7)) back into our energy approximation 
([Eq. 6](#eq6)) and calculate the energy gradient w.r.t. the weights (see paper for derivation)

$$
\textbf{Approx. weight gradient:} \quad \underbrace{\vphantom{\frac{\partial \hat{x}}{\partial \theta}}\nabla_{\theta} \mathcal{F}^*}_{\text{PC direction}} \approx \underbrace{\frac{\partial \hat{x}}{\partial \theta}\mathcal{I}(\hat{x})^{-1}g_{\mathcal{L}}(\hat{x})}_{\text{TR direction}} + \underbrace{\vphantom{\frac{\partial \hat{x}}{\partial \theta}}g_{\mathcal{L}}(\theta)}_{\text{BP direction}}
$$

where $$g_{\mathcal{L}}(\theta)$$ is the loss gradient w.r.t. the weights, and $$\partial \hat{x}/\partial \theta$$ is 
the mapping from activity to weight space. Thus, we see that the PC weight update essentially shifts the loss (BP) 
gradient in the direction of the TR inference solution mapped back into weight space.

## Some experiments <a name="exps"></a>

Does this have practical implications for training neural networks? Our as well as others' experiments suggest *yes*, 
at least in certain cases. For example, here are some results showing faster convergence of PC over BP on 10-layer 
networks trained on MNIST controlling for the best learning rate

<img src="https://raw.githubusercontent.com/francesco-innocenti/francesco-innocenti.github.io/master/_posts/imgs/DNN_exps.png" style="zoom:20%;" />
<p style="text-align:center">$$\color{grey}{\small{\text{Figure}}} \space \color{grey}{\small{4}}\notag$$</p>

Similar speedups have been previously found on other datasets, tasks, and architectures [[4]](#4)[[5]](#5).

## Concluding thoughts <a name="thoughts"></a>

To sum up, we have shown that PC implicitly performs a kind of $$2^{\text{nd}}$$-order update on the weights by 
$$1^{\text{st}}$$-order updates on activities. To our knowledge, this is the first local learning algorithm that has 
been shown to use $$2^{\text{nd}}$$-order information via only $$1^{\text{st}}$$-order updates.

Does this mean that we should trash BP and start training neural nets with PC? Probably not, at least for now. First, 
PC inference–which is what we show gives the algorithm its $$2^{\text{nd}}$$-order information–is computationally 
expensive, requiring lots of iterations to converge, and scales badly with network size. This could be addressed with 
neuromorphic hardware and amortisation. However, even if this inference cost can be overcome, PC would have to compete 
with state-of-the-art optimisers like Adam which converge a lot faster than (S)GD.

In our paper we also discuss the potential implications of our findings for neuroscience and, in particular, for 
whether the brain may perform gradient descent on an Euclidean geometry.

## References

<p> <font size="3"> <a id="1">[1]</a> 
Millidge, B., Seth, A., & Buckley, C. L. (2021). Predictive coding: a theoretical and experimental review. <i>arXiv preprint arXiv:2107.12979</i>.</font> </p>

<p> <font size="3"> <a id="2">[2]</a> 
Du, S. S., Jin, C., Lee, J. D., Jordan, M. I., Singh, A., and Poczos, B. Gradient descent can take exponential time to escape saddle points. <i>Advances in neural information processing systems</i>, 30, 2017.</font> </p>

<p> <font size="3"> <a id="3">[3]</a> 
Jin, C., Ge, R., Netrapalli, P., Kakade, S. M., & Jordan, M. I. (2017). How to escape saddle points efficiently. In <i>International conference on machine learning</i> (pp. 1724-1732). PMLR.</font> </p>

<p> <font size="3"> <a id="4">[4]</a> 
Alonso, N., Millidge, B., Krichmar, J., & Neftci, E. O. (2022). A theoretical framework for inference learning. <i>Advances in Neural Information Processing Systems</i>, 35, 37335-37348.</font> </p>

<p> <font size="3"> <a id="5">[5]</a> 
Song, Y., Millidge, B., Salvatori, T., Lukasiewicz, T., Xu, Z., & Bogacz, R. (2022). Inferring neural activity before plasticity: A foundation for learning beyond backpropagation. <i>bioRxiv</i>, 2022-05.</font> </p>

[^1]: The acute observer will notice that while the energy and the loss are the same, their gradients aren't. This is because of the local weight update rule in PC, which only under some extra conditions can approximate or equal the gradients computed by BP.
