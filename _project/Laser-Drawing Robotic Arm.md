---
title: "Laser Drawing Robot Arm"
img: kino_shot.webp
collection: project
date: 2022-04-03
---

<center>
    <iframe width="640" height="400" src="https://www.youtube.com/embed/E3bSRnSi4Ag" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>






## KOMO (K-Order Markov Optimization) - Mathematical Overview

KOMO is a framework for solving motion optimization problems in robotics by focusing on configurations rather than explicit dynamics like velocity or acceleration.

### Core Concepts

- **Trajectory Representation**: In KOMO, trajectories are represented directly in the configuration space. This approach differs from traditional dynamics representation, which uses both position and velocity.

- **Optimization Problem Formulation**: The key idea in KOMO is formulating the problem as a k-order non-linear optimization problem. The goal is to minimize a sum-of-squares cost function, subject to certain constraints. Mathematically, it is:

  $$
  \min_{x_{0:T}} \sum_{t=0}^{T} f_t(x_{t-k:t})^T f_t(x_{t-k:t}) + k(t, t') x_t^T x_{t'}
  $$
  $$
  \text{subject to } g_t(x_{t-k:t}) \leq 0 \text{ and } h_t(x_{t-k:t}) = 0
  $$

  Here, `x_{t-k:t}` represents tuples of consecutive configurations, and `f_t`, `g_t`, `h_t` are differentiable functions defining costs and constraints.

- **Cost and Constraints**: The framework is flexible, allowing various elements in the cost vectors 'f_t', including transition and task-related costs. The constraints `g_t` and `h_t` ensure the solution adheres to specific requirements.

- **Gauss-Newton Optimization**: KOMO utilizes the Gauss-Newton method for optimization, focusing on the global Jacobian and the pseudo-Hessian to efficiently find solutions.

### Application in Robotics

KOMO is particularly useful in robotics for planning and optimizing motions. By focusing on configurations and using k-order Markov optimization, KOMO efficiently handles complex robotic tasks without the need for explicitly representing dynamic aspects like velocity and acceleration.

## Mathematical Formulations


### Camera Calibration and Spatial Calculations

1. **Transformation of 2D Image Data to 3D Coordinates**:
   - Using intrinsic camera parameters `f` (focal length), `p_x`, and `p_y` (principal point coordinates), the transformation from image coordinates to world coordinates can be represented as:
   $$
   \begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} \frac{(u - p_x) \cdot z}{f} \\ \frac{(v - p_y) \cdot z}{f} \\ z \end{pmatrix}
   $$
   where `(u, v)` are the pixel coordinates in the image, and `z` is the depth value at those coordinates.  

In this project, the steps I used to achieve this movement was to:
1. Filter the points related to the flashlights.
2. Get the depth data for those pixel values and convert them to 3d position.
3. From the pointclouds apply a PCA, get the orientation and the center point.
4. Use KOMO to find the correct way to grasp the flashlight.
5. Try to hold at same point and by phytagorean theorem calculate the angle to hold.





---

