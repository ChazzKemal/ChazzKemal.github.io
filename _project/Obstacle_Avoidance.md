---
title: "Target Following Robot"
img: following_robot.webp
collection: project
date: 2022-04-03
---


<center>
    <iframe width="640" height="400" src="https://www.youtube.com/embed/jn4fmIsK9Mw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>




# Artificial Potential Fields

## Introduction

Artificial Potential Fields (APFs) are used in path planning and trajectory planning, particularly for robotic navigation. This method involves conceptualizing a surface, denoted as $$\phi$$, defined in the workspace. The robot is visualized as moving down the gradient of this surface.

## Key Concepts

- **Robot Position:** The robot is considered to be at a position $$ b \in \mathbb{R}^3 $$ with a certain radius $$ \rho_r $$.
- **Goal Configuration:** The goal or final configuration is treated as an attractive point in the potential field.
- **Obstacle Boundaries:** Obstacles are located at $$ o_i $$ with radii $$ \rho_i > 0 $$. These create repelling effects in the potential field.
- **Critical Points:** The goal is to have one minimum (attractive point) and ensure that every other critical point is nondegenerate.

## APF Definition

The potential field $$\phi$$ is a function from a field $$ F $$ to the interval [0, 1], defined as a composition:

$$
\phi(b) = \sigma_d \circ \sigma \circ \hat{\phi}(b) \quad \text{(1)}
$$

Where $$\hat{\phi}$$ is another function from $$ F $$ to [0, ∞), encoding the goal point and obstacles:

$$
\hat{\phi}(b) = \Delta \gamma_k(b) \beta(b) \quad k \in \mathbb{Z}^+ \quad \text{(2)}
$$

- **Goal Function $$ \gamma $$:** For $$ \gamma : F \rightarrow [0, \infty) $$, it is defined as $$ \gamma(b) = (b - g)^T (b - g) $$, where $$ g $$ is the goal position.
- **Obstacle Function $$ \beta $$:** The obstacle function $$ \beta : F \rightarrow [0, \infty) $$ is defined in terms of distances to obstacles, $$ \beta(b) = \Delta_{j=1}^N \beta_j(b) $$, where each $$ \beta_j(b) = (b - o_j)^2 - (\rho_r + \rho_j)^2 $$.
- **Parameter $$ k $$:** Represents the balance between goal attraction and obstacle repulsion.

### Handling Freespace Boundaries

The freespace boundary $$ \partial F $$ is the zero-level set of $$ \beta^{-1}(0) $$. Since $$ \hat{\phi} $$ can blow up on $$ \partial F $$, it's not admissible. This is remedied by squashing the function using $$ \sigma : [0, \infty] \rightarrow [0, 1] $$, defined as $$ \sigma(x) = \frac{x}{1 + x} $$.

To avoid degenerate goal points, a sharpening function $$ \sigma_d : [0, 1] \rightarrow [0, 1] $$ is applied, where $$ \sigma_d(x) = x^{1/k} $$. This results in $$ \phi $$ becoming admissible with a non-degenerate minimum at $$ b = g $$.

---
Here we implemented the APF by getting the obstacle positions through RGB-D cameras. Target point was selected from the initial position. The remaining robots were responsible to follow the robot in front from a distance with the same algorithm.





---

