
VD1: Max x+2y+3z over the set: x^2+y^2+z^2=3

Let f(x, y, z) = x+2y+3z denote the objective function and g(x, y, z) = x^2+y^2+z^2 ....

---
We want to maximize

$$
f(x,y,z)=x+2y+3z
$$

subject to the constraint

$$
x^2+y^2+z^2=3.
$$

### Using Lagrange Multipliers

Define the constraint function

$$
g(x,y,z)=x^2+y^2+z^2-3=0.
$$

Introduce a Lagrange multiplier \(\lambda\) and form the Lagrangian:

$$
\mathcal{L}(x,y,z,\lambda)= x+2y+3z - \lambda (x^2+y^2+z^2-3).
$$

#### Step 1. Compute the Gradients

The gradient of \(f\) is

$$
\nabla f = (1,\, 2,\, 3).
$$

The gradient of \(g\) is

$$
\nabla g = (2x,\, 2y,\, 2z).
$$

#### Step 2. Set Up the Equations

Setting \(\nabla f = \lambda \nabla g\) gives:

$$
\begin{cases}
1 = 2\lambda x, \\
2 = 2\lambda y, \\
3 = 2\lambda z.
\end{cases}
$$

Solve each equation for \(x\), \(y\), and \(z\):

$$
x = \frac{1}{2\lambda}, \quad y = \frac{1}{\lambda}, \quad z = \frac{3}{2\lambda}.
$$

#### Step 3. Substitute into the Constraint

Substitute \(x\), \(y\), and \(z\) into \(x^2+y^2+z^2=3\):

$$
\left(\frac{1}{2\lambda}\right)^2 + \left(\frac{1}{\lambda}\right)^2 + \left(\frac{3}{2\lambda}\right)^2 = \frac{1}{4\lambda^2}+\frac{1}{\lambda^2}+\frac{9}{4\lambda^2}.
$$

Combine the terms by writing them over a common denominator:

$$
\frac{1}{4\lambda^2} + \frac{4}{4\lambda^2} + \frac{9}{4\lambda^2} = \frac{14}{4\lambda^2} = \frac{7}{2\lambda^2}.
$$

Set equal to 3:

$$
\frac{7}{2\lambda^2} = 3 \quad \Longrightarrow \quad \lambda^2 = \frac{7}{6}.
$$

For a maximum, choose the positive square root:

$$
\lambda = \sqrt{\frac{7}{6}}.
$$

#### Step 4. Find the Coordinates

Now substitute \(\lambda\) back into the expressions for \(x\), \(y\), and \(z\):

$$
x = \frac{1}{2\sqrt{\frac{7}{6}}} = \frac{\sqrt{6}}{2\sqrt{7}},
$$

$$
y = \frac{1}{\sqrt{\frac{7}{6}}} = \frac{\sqrt{6}}{\sqrt{7}},
$$

$$
z = \frac{3}{2\sqrt{\frac{7}{6}}} = \frac{3\sqrt{6}}{2\sqrt{7}}.
$$

#### Step 5. Calculate the Maximum Value

Substitute these values into \(f(x,y,z)= x+2y+3z\):

$$
f(x,y,z)= \frac{\sqrt{6}}{2\sqrt{7}} + 2\cdot\frac{\sqrt{6}}{\sqrt{7}} + 3\cdot\frac{3\sqrt{6}}{2\sqrt{7}}.
$$

Simplify term by term:

- The first term is \(\frac{\sqrt{6}}{2\sqrt{7}}\).
- The second term is \(\frac{2\sqrt{6}}{\sqrt{7}} = \frac{4\sqrt{6}}{2\sqrt{7}}\).
- The third term is \(\frac{9\sqrt{6}}{2\sqrt{7}}\).

Adding these:

$$
f(x,y,z)= \frac{\sqrt{6} + 4\sqrt{6} + 9\sqrt{6}}{2\sqrt{7}} = \frac{14\sqrt{6}}{2\sqrt{7}} = \frac{7\sqrt{6}}{\sqrt{7}}.
$$

Rationalize or simplify further:

$$
\frac{7\sqrt{6}}{\sqrt{7}} = 7\sqrt{\frac{6}{7}} = \sqrt{42}.
$$

### Alternative Geometric Interpretation

Since \(f(x,y,z)\) is a linear function, its maximum on the sphere \(x^2+y^2+z^2=3\) is attained when \((x,y,z)\) points in the direction of \((1,2,3)\). The norm of \((1,2,3)\) is

$$
\sqrt{1^2+2^2+3^2}=\sqrt{14},
$$

and the sphere has radius \(\sqrt{3}\). Thus, the maximum value is

$$
\sqrt{14}\cdot \sqrt{3}=\sqrt{42}.
$$

### Final Answer

The maximum value of \(x+2y+3z\) on the sphere \(x^2+y^2+z^2=3\) is

$$
\boxed{\sqrt{42}},
$$

attained at

$$
\left(\frac{\sqrt{6}}{2\sqrt{7}},\, \frac{\sqrt{6}}{\sqrt{7}},\, \frac{3\sqrt{6}}{2\sqrt{7}}\right),
$$

or equivalently at

$$\left(\sqrt{\frac{3}{14}},\, 2\sqrt{\frac{3}{14}},\, 3\sqrt{\frac{3}{14}}\right)
$$
---
![[Pasted image 20250228110443.png]]

![[Pasted image 20250228110453.png]]

![[Pasted image 20250228110505.png]]


- https://chatgpt.com/share/e/67c13709-fbc0-800b-ba1f-ffaacb365a7a
- 