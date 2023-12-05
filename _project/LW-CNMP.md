---
title: "Locally-Weighted CNMP"
img: LW-CNMP_basarili_paint3_400.png
collection: project
date: 2023-04-03
---

## CNMP, and how to solve it's weaknesses:
CNMP is a learning-from-demonstration model that can given the conditions,(task specific information, positions at certain time) create a trajectory where each point in time is represented with a mean and and standard deviation(how unsure the model is):
<center>
<img src="/images/CNMP_explaination.png" alt="YOLOv3 Model in Simulation">
</center>
<br />

For each condition point the encoder creates a latent vector, and after every condition point is encoded in latent space, these vectors are aggregated. Aggregated vector is concatenated with the query time point and the decoded vector output becomes the trajectory output at that certain time.
CNMP has some some room to grow as such:

- **Blending**: Since you want to find the trajectory that is represented by condition points, if the trajectory is a mixture of primitives,the model fails. You can see it in the figure below. When you teach the orange and blue demonstrations to the model, the trajectory is guessed wrong if you give the start of the orange and the end as blue. 
<br />
The solution we thought is that, we can aggregate the latent vectors in a way that queried points should be affected by closer conditions more.


The equation given is:

$$ r(t) = \frac{\sum w_n \cdot r_{c_n}}{\sum w_n} \quad \text{where} \quad w_n = \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(r_{c_n} - \mu_t)^2}{2\sigma^2}} $$

$$
\begin{align*}
&\text{where:} \\
&\text{- } r(t) \text{ represents the weighted sum at time } t. \\
&\text{- } w_n \text{ is the weight for each component } r_{c_n}. \\
&\text{- } \mu_t \text{ and } \sigma \text{ represent the mean and standard deviation of the Gaussian distribution, respectively.} \\
&\text{- The exponential term } e^{-\frac{(r_{c_n} - \mu_t)^2}{2\sigma^2}} \text{ is the Gaussian probability density function,} \\
&\text{  which calculates the weight } w_n \text{ for each component based on its distance from the mean } \mu_t. \\
&\text{- The sum } \sum w_n \cdot r_{c_n} \text{ calculates the weighted sum of the components, and this sum} \\
&\text{  is then normalized by dividing by the sum of the weights } \sum w_n.
\end{align*}
$$



<center>
<img src="/images/tanh-1.png" alt="YOLOv3 Model in Simulation">
</center>
<br />


  
- **Multimodality**: Basicly when you represent each point as a gaussian distribution, you cannot represent multimodal distributions. Think it this way, If your demonstrations are only going vertical and going horizontal from a certain position,the model will learn to go diagonally given there are same amount of diagonal and horizontal demonstrations. My solution for this part was to implement a vector quantized model. 
* Initialize memory vectors in arbitrary number bigger than the amount of different primitives you will show.
* The model will be trained in a way to compare the encoded latent vector to memory vectors and get similarity score by taking dot product of the vectors.
* Select the closest demonstration from the memory and execute it.


<center>
<img src="/images/grid_lw.jpg" alt="YOLOv3 Model in Simulation">
</center>
<br />


- **Uncertainity**: Information doesn't necessarily have to be complete. In CNMP, your conditioning points needs to give every type of information while training. So basically, I will train the model to have a drop out at the initial layer depending on a condition. This way I can also execute a correctifying trajectory between the condition points, where when standard deviation is high sudden jumps could occur. This part is why I still didn't published a paper. 


We can use the current model to creates a dance choreography by teaching every dance move seperately like the image below:

<center>
<video class="projectVideo" muted autoplay loop>
  <source src="/videos/lw_cnmp_mix_dance.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>
</center>



---

