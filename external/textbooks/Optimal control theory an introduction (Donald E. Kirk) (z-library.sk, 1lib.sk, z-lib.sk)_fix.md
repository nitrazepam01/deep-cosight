> OCR by deepseek-ai/DeepSeek-OCR | 472 pages

### Page 1

### Page 2

答道：Donald E. Kirk

---

**Donald E. Kirk**

*Professor Emeritus of Electrical Engineering*
*San José State University*
*San José, California*

---

Dover Publications, Inc.
 Mineola, New York

### Page 3

value for this important subject.

AUTHOR

STEPHEN GORDON 1943-1955 especially during the time when he was a Research Economist at the Industrial Prices Research Bureau.

© Copyright 1966, 1970, and 1998 by Edward E. Kirk. All rights reserved.

Distributed by letter to whoever had the STERC/SOC LATIN/CP standards in their computer center project.

We thank Joe Schultz, Kip Stoddard, Richard Jensen, Ed Wiklund, and Charles Paquette for help in foot patent file preparation and search. We thank Gene Fredricks for unterstützung of trees encontrada printing and making our copy, and Daniel Marsannay for graph.

Typographical demands were met with patience by those who served as reporters and proofers. The listing remarks in the original publishing were omitted because the index was prepared from the published list. The journal was printed by the Stockton Press in Stockton, California.

Library of Congress Cataloging-in-Publication Data

Kirk, Donald E., 1937-- Optimal control theory : an introduction / Donald E. Kirk. p. cm. Originally published: Englewood Cliffs, N.J. : Prentice-Hall, 1970 (Prentice Hall networks series)

Includes bibliographical references and index. ISBN 0-486-43484-2 (pbk.) 1. Control theory. 2. Mathematical optimization. I. Title.

QA402.3.K52 2004

003'.5—dc22

Manufactured in the United States of America

Dover Publications, Inc., 31 East 2nd Street, Mineola, N.Y. 11501

### Page 4

The optimal control theory—which is playing an increasingly important role in the design of modern systems—has as its objective the maximization of the return from, or the minimization of the cost of, the operation of physical, social, and economic processes.

This book introduces three facets of optimal control theory—dynamic programming, Pontryagin’s minimum principle, and numerical techniques for trajectory optimization—at a level appropriate for a first- or second-year graduate course, an undergraduate honors course, or for directed self-study. A reasonable proficiency in the use of state variable methods is assumed; however, this and other prerequisites are reviewed in Chapter 1. In the interest of flexibility, the book is divided into the following parts:

Part I: Describing the System and Evaluating Its Performance
(Chapters 1 and 2)

Part II: Dynamic Programming
(Chapter 3)

Part III: The Calculus of Variations and Pontryagin’s Minimum Principle
(Chapters 4 and 5)

Part IV: Iterative Numerical Techniques for Finding Optimal Controls and Trajectories
(Chapter 6)

Part V: Conclusion
(Chapter 7)

Because of the simplicity of the concept, dynamic programming (Part II) is presented before Pontryagin’s minimum principle (Part III), thus enabling

### Page 5

DONALD E. KIRK
Carmel, California

\centerline{\heiti Preface}
the reader to solve meaningful problems at an early stage, and providing motivation for the material which follows. Parts II and III are self-contained; they may be studied in either order, or either may be omitted without affecting the treatment in the other. The problems provided in Parts I through IV are designed to introduce additional topics as well as to illustrate the basic concepts. My experience indicates that it is possible to discuss, at a moderate pace, Chapters 1 through 4, Sections 5.1 through 5.3, and parts of Sections 5.4 and 5.5 in a one-quarter, four-credit-hour course. This material provides adequate background for reading the remainder of the book and other literature on optimal control theory. To study the entire book, a course of one semester's duration is recommended. My thanks go to Professor Robert D. Strum for encouraging me to undertake the writing of this book, and for his helpful comments along the way. I also wish to express my appreciation to Professor John R. Ward for his constructive criticism of the presentation. Professor Charles H. Rothauge, Chairman of the Electrical Engineering Department at the Naval Postgraduate School, aided my efforts by providing a climate favorable for preparing and testing the manuscript. I thank Professors Jose B. Cruz, Jr., William R. Perkins, and Ronald A. Rohrer for introducing optimal control theory to me at the University of Illinois; undoubtedly their influence is reflected in this book. The valuable comments made by Professors James S. Demetry, Gene F. Franklin, Robert W. Newcomb, Ronald A. Rohrer, and Michael K. Sain are also gratefully acknowledged. In proofreading the manuscript I received generous assistance from my wife, Judy, and from Lcdr. D. T. Cowdrill and Lcdr. R. R. Owens, USN. Perhaps my greatest debt of gratitude is to the students whose comments were invaluable in preparing the final version of the book.

### Page 6

导向

###### Contents
Contents

Part I: Describing the system and evaluating its performance

1. Introduction

   1.1 Problem Formulation  3
   1.2 State Variable Representation of Systems  16
   1.3 Concluding Remarks  22
    References  23
    Problems  23

2. The Performance Measure

    2.1 Performance Measures for Optimal Control Problems  29
    2.2 Selecting a Performance Measure  34
    2.3 Selection of a Performance Measure: The Carrier Landing of a Jet Aircraft  42
     References  47
     Problems  47

Part II: Dynamic Programming

3. Dynamic Programming

   3.1 The Optimal Control Law  53
   3.2 The Principle of Optimality  54

vii

### Page 7

### Page 8

listing }

### Page 9

}})

### Page 10

leaving a shadow in the unlit side of the one-way street of which you doubtless have heard. It slists almost directly across the street. However, a pedestrian or a bicyclist who knows or should know better is tempted to try to cross at the time and to the best of his ability, since the pedestrian or bicyclist is no longer legally in the illuminated zone of that one-way street. The probability that the danger he feels is lamp light is clearly diminished about a factor of a million. And having no other means at hand to fire a gun, he can only rail against the light-bearing Law. There is a disposition of the body this way. ___int Sinclair _1981. Perhaps it is unusual that the pedestrian is only responsible for his own safety since the negligent bicyclist often fails to mention his bicycle when he forgives the violator.

### Page 11

\[ \mathbf{x}(t) \triangleq \begin{bmatrix} x_1(t) \\ x_2(t) \\ \vdots \\ x_n(t) \end{bmatrix} \]The student is too thick</td></tr></table>

### Page 12

Selecting position and velocity as state variables, that is,\[ x_1(t) \triangleq d(t) \quad \mathrm{and} \quad x_2(t) \triangleq d'(t), \] and letting\[ u_1(t) \triangleq \alpha(t) \quad \mathrm{and} \quad u_2(t) \triangleq \beta(t), \] we find that the state equations become\[ \dot x_1(t) = x_2(t) \\ \dot x_2(t) = u_1(t) + u_2(t), \tag {1.1-3}\] or, using matrix notation,\[ \dot \pmb{x}(t) = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \pmb{x}(t) + \begin{bmatrix} 0 & 0 \\ 1 & 1 \end{bmatrix} \pmb {u}(t). \] The following relations hold true for full-wides systems with different: This is the mathematical model of the process in state form.

### Page 13

### Page 14

ather the car does not back up, then the additional constraints

If we assume that the car does not back up, then the additional constraints
$$
0 \leq x_{1}(t) \leq e
$$
are also imposed.
What are the constraints on the control inputs (acceleration)? We know that the acceleration is bounded by some upper limit which depends on the capability of the engine, and that the maximum deceleration is limited by the braking system parameters. If the maximum acceleration is $M_{1} > 0$, and the maximum deceleration is $M_{2} > 0$, then the controls must satisfy
$$
0 \leq u_{1}(t) \leq M_{1}
$$
- $M_{2} \leq u_{2}(t) \leq 0$.
In addition, if the car starts with $G$ gallons of gas and there are no service stations on the way, another constraint is
$$
\int_{t_{0}}^{t_{f}} [k_{1} u_{1}(t) + k_{2} x_{2}(t)] dt \leq G
$$
which assumes that the rate of gas consumption is proportional to both acceleration and speed with constants of proportionality $k_{1}$ and $k_{2}$.
Now that we have an idea of typical constraints that may be encountered, let us make these concepts more precise.

### Page 15

represents in Darcy's law

We shall denote the set of admissible controls by \( U \), and the notation \( u \in U \) means that the control history \( u \) is admissible.

To illustrate the concept of admissibility Fig. 1-3 shows four possible acceleration histories for Example 1.1-2. \( u_1^{(2)} \) and \( u_1^{(4)} \) are not admissible;

\[
\begin{align*}
u_1^{(1)}(t) \\
M_1 \\
\begin{array}{cccccc}
t_0 & & & & & t_f \\
\end{array} \\
(a)
\end{align*}
\]

\[
\begin{align*}
u_1^{(2)}(t) \\
M_1 \\
\begin{array}{cccccc}
t_0 & & & & & t_f \\
\end{array} \\
(b)
\end{align*}
\]

\[
\begin{align*}
u_1^{(3)}(t) \\
M_1 \\
\begin{array}{cccccc}
t_0 & & & & & t_f \\
\end{array} \\
(c)
\end{align*}
\]

\[
\begin{align*}
u_1^{(4)}(t) \\
M_1 \\
\begin{array}{cccccc}
t_0 & & & & & t_f \\
\end{array} \\
(d)
\end{align*}
\]

Figure 1-3 Some acceleration histories

\( u_1^{(1)} \) and \( u_1^{(3)} \) are admissible if they satisfy the consumed-fuel constraint of Eq. (1.1-9). In this example, the set of admissible controls \( U \) is defined by the inequalities in (1.1-8) and (1.1-9).

DEFINITION 1-4

A state trajectory which satisfies the state variable constraints during the entire time interval \([t_0, t_f]\) is called an admissible trajectory.

### Page 16

2. (a) (b)

*These slopes are all 4 because they intersect the x-axis about 1 and 2 respectively. They make it so that the area under the curve is the same as has the area under the red line. If we make the red line parallel to x axis, Then we get the small area. This is one of the benefits of using positive values of the slopes of the present method. This method also produces shorter trajectories than the old method in which the slope is the negative slope. If we make the red line y axis, then we get the sloped of sothe medlinear sloping of the present method is 0.632394612462 which is %180.632 times that of the old method.+

### Page 17

### Page 18

represents the power law exponent.Find an admissible control $\mathbf{u}^*$ which causes the system

### Page 18

represents the power law exponent.

Find an admissible control $\mathbf{u}^*$ which causes the system

$$\dot{\mathbf{x}}(t) = \mathbf{a}(\mathbf{x}(t), \mathbf{u}(t), t) \tag{1.1-12}$$

to follow an *admissible trajectory* $\mathbf{x}^*$ that minimizes the performance measure

$$J = h(\mathbf{x}(t_f), t_f) + \int_{t_0}^{t_f} g(\mathbf{x}(t), \mathbf{u}(t), t) dt. \tag{1.1-13}$$

$\mathbf{u}^*$ is called an *optimal control* and $\mathbf{x}^*$ an *optimal trajectory*.

Several comments are in order here. First, we may not know in advance that an optimal control *exists*; that is, it may be impossible to find a control which (a) is admissible and (b) causes the system to follow an admissible trajectory. Since existence theorems are in rather short supply, we shall, in most cases, attempt to find an optimal control rather than try to prove that one exists.

Second, even if an optimal control exists, it may not be *unique.* Nonunique optimal controls may complicate computational procedures, but they do allow the possibility of choosing among several controller configurations. This is certainly helpful to the designer, because he can then consider other factors, such as cost, size, reliability, etc., which may not have been included in the performance measure.

Third, when we say that $\mathbf{u}^*$ causes the performance measure to be minimized, we mean that

$$J^* \triangleq h(\mathbf{x}^*(t_f), t_f) + \int_{t_0}^{t_f} g(\mathbf{x}^*(t), \mathbf{u}^*(t), t) dt \\
\leq h(\mathbf{x}(t_f), t_f) + \int_{t_0}^{t_f} g(\mathbf{x}(t), \mathbf{u}(t), t) dt \tag{1.1-14}$$

for all $\mathbf{u} \in U$, which make $\mathbf{x} \in X$. The above inequality states that an optimal control and its trajectory cause the performance measure to have a value smaller than (or perhaps equal to) the performance measure for *any other* admissible control and trajectory. Thus, we are seeking the *absolute* or *global minimum* of $J$, not merely *local minima*. Of course, one way to find the global minimum is to determine all of the local minima and then simply pick out one (or more) that yields the smallest value for the performance measure.

It may be helpful to visualize the optimization as shown in Fig. 1-5. $\mathbf{u}^{(1)}$, $\mathbf{u}^{(2)}$, $\mathbf{u}^{(3)}$, and $\mathbf{u}^{(4)}$ are “points” at which $J$ has local, or relative, minima; $\mathbf{u}^{(1)}$ is the “point” where $J$ has its global, or absolute, minimum.

Finally, observe that if the objective is to maximize some measure of system performance, the theory we shall develop still applies because this

### Page 19

reflecting the early 20th cen- 16

### Page 20

composed of two parts by Chernishko and Indjik (2003):

The inequality constraint

\[\int_{t_0}^{t_f} [k_1 u_1(t) + k_2 x_2(t)] dt \leq G\]

completes the description of the admissible states and controls.

The solution to this problem (which is left as an exercise for the reader at the end of Chapter 5) is shown in Fig. 1-6 for the situation where \( M_1 = M_2 \) \(\triangleq M\). We have also assumed that the car has enough fuel available to reach point \( e \) using the control shown.

---

**Figure 1-6** The optimal control and trajectory for the automobile problem

**Example 1.1-5.** Let us now consider what would happen if the preceding problem had been improperly formulated. Suppose that the control constraints had not been recognized. If we let

\[a(t) + \beta(t) = e \frac{d}{dt} [\delta(t - t_0)]\]

### Page 21

value that occurs after 1, but not before .862 .4156 .373 0.3658 062 0.4130 0 0.3545 0.3347 0.3427 0.3404 0.3315 0.3298 0.3276 0.3251 0.3236 0.3213 0.3196 0.3179 0.3163 0.3148 0.3135 0.3123 0.3111 0.3100 0.3090 0.3080 0.3078 0.3075 0.3073 0.3071 0.3069 0.3068 0.3066 0.3065 0.3064 0.3063 0.3062 0.3061 0.3060

The plot has accompanying text beneath it. Line representing weight of air in a frigid snow land. Radial. (Observers must be cautious in probe measurements. Technical details may not be easy to understand. Threading .227300 .80488 .127058 .396654 .236885 .11847 .051817 .500325 .250162 .123802 .097035 .049767 .024131 .000614

from the 1st5 range and that the 2nd65 range does not begin until around .733 or .773, or approximately 13.6% of the density of light throughout the graph. That is about where all other information about light missed when taken into account; this could be a significant problem if extrapolated or linearized.

[see the blue trace in the middle graph, which shows ”The graph is horizontal at an angle of 32.0;2 degrees.”.]

If e is critical, all parts fail at the same time, we then have. \(e\nu_{1}(t) e\nu_{k}\) \(\nu_{1}\nu_{k}\) \(e\nu_{1}(t) e\nu_{k}\) \(\nu_{1}\nu_{k}\) \(\frac{\nu_{1\nu_{k}t}}{e\nu_{1\nu_{k}}(l)}\) \(t\) \(e\nu_{1\nu_{k}}(l)\) \(\nu_{1}\nu_{k}\) Since the average number of deaths corresponds to the Poisson distribution with parameter \(\nu_{1}\). The variable \(t\) is the temperature, and so is a natural number. For these reasons, the problem is a small but significant problem. The observation violates the truth of all the real situations that are involved in the event, because a vacation is not necessary. The true value is the reason for this problem. The knowledge of all possibilities is the value when exploring a considered object. However, since the order of the values is negligible, \(\nu_{1}\) the sum of all the values is accurately calculated: the value calculated is the total number of times that this is the closest around .13, the same result is obtained with the first-order of the value. \(\nu_{k}\) of 0.134, the maximum of the distribution: =0.3, the value of the evaluation is concentrated to find the correct value. The calculation result is complete: for the numbers of calculation, it is necessary to make it \(\nu_{1}\) and the maximum of the distribution: 0.1. There are some difficulties in this problem and different simply, because the distances greater than sol and ice are more than 0. which makes the

### Page 22

-responsive control.

If the optimal control is determined as a function of time for a specified initial state value, that is,

\[ u^*(t) = e(x(t_0), t), \] (1.1-20)

then the optimal control is said to be in *open-loop form*.

Thus the optimal open-loop control is optimal only for a *particular* initial state value, whereas, if the optimal control *law* is known, the optimal control history starting from *any* state value can be generated.

Conceptually, it is helpful to imagine the difference between an optimal control law and an open-loop optimal control as shown in Fig. 1-8; notice, however, that the mere presence of connections from the states to a controller does not, in general, guarantee an *optimal* control law.†

† The terms *optimal feedback control, closed-loop optimal control*, and *optimal control strategy* are also often used.

‡ This is pursued further in reference [K-1].

### Page 25
23k2+3l2=Ccount. For 𝛾 (k), − 18

### Page 26

### Page 27

### Page 28
around 7nm in size.Determine the time \(\Delta t\) for sufficient approximation of the transfer function. The results of the calculations are given as follows:

    $$
    \dot{\mathbf{x}}(t) = \mathbf{Ax(t)} + Bu(t)
    \tag{1.2-12}
    $$

Write the equation of the state space \(x(t)\):

$$
x(t) = \begin{bmatrix} x_{1}(t) \\ x_{2}(t) \end{bmatrix}
$$

Using the transformation:

$$
\begin{aligned}
& x_{1} = \omega_{1} t + \omega_{2} t^{2} \\
& x_{2} = \omega_{2} t + \omega_{2} t^{2}
\end{aligned}
$$

The state space of the linear system is:

$$
\begin{aligned}
& \dot{x}_{1} = \omega_{1} x_{2} - \omega_{2} x_{1} \\
& \dot{x}_{2} = \omega_{2} x_{1} + 2\omega_{2} x_{2}
\end{aligned}
$$

Equation of the system under the Laplace transformation:
$$
\begin{aligned}
& X(s) = \mathcal{L}(x) = \int_{0}^{\infty} x(t) e^{-st} dt \\
& \mathcal{L}(x) = \int_{0}^{\infty} x(t) \cdot e^{-st} dt
\end{aligned}
$$

Using the Laplace operation:

$$
\begin{aligned}
& X(s) = K \cdot [\mathscr{L} (F(s))]^{-1} = \frac{K}{s+2s+2}
\end{aligned}
$$

Given the real numbers: 
$$
\begin{aligned}
& \omega_{1} = 3 \\ 
& \omega_{2} = 15
\end{aligned}
$$

And, the Laplace transform of the transfer function is:

$$
\begin{aligned}
& \mathcal{L} \left( \frac{\omega_{2}}{s^{2} + 2s + 2} \right) = \frac{1}{25}
\end{aligned}
$$

Hence, the undamped natural frequency of the secondary system is:

$$
\text{Note: for the details of}
$$
$$
\omega_{2} = 15
$$
$$
\text{please refer to textbook Question 1.15 of J. D. Lee or the迎新教学视频:}
$$
$$
\```
$$
evaluating the inverse Laplace transform of the system will give the secondary system.

### Page 29
合适点 要： 位D x:u) are all too large. 2 3 S t i. (r')
我认为，对于应用问题是组
可以表示枚举实数地出现并代价大为0的最后
仍 C Lemma
和C紧反， 而且。
即边界条件\(ε)
一段对ζRadius里的 Hamilton 路径系
涟：导体参数O(λ,a),函数
Mathematics’

& \omega_{1} = 3 \\ 
& \omega_{2} = 15
\end{aligned}
$$

And, the Laplace transform of the transfer function is:

$$
\begin{aligned}
& \mathcal{L} \left( \frac{\omega_{2}}{s^{2} + 2s + 2} \right) = \frac{1}{25}
\end{aligned}
$$

Hence, the undamped natural frequency of the secondary system is:

$$
\text{Note: for the details of}
$$
$$
\omega_{2} = 15
$$
$$
\text{please refer to textbook Question 1.15 of J. D. Lee or the迎新教学视频:}
$$

evaluating the inverse Laplace transform of the system will give the secondary system.

### Page 29

### Page 30

going in and out of the water." tested against various conditions provided a more reliable testing methodology.

Proceedings

A-1 Athans, M., "The Status of Optimal Control Theory and Applications for Deterministic Systems," IEEE Trans. Automatic Control (1966), 580-596.
D-1 Derusso, P. M., R. J. Roy, and C. M. Close, State Variables for Engineers. New York: John Wiley & Sons, Inc., 1965.
K-1 Kliger, I., "On Closed-Loop Optimal Control," IEEE Trans. Automatic Control (1965), 207.
K-2 Kalman, R. E., "On the General Theory of Control Systems," Proc. First IFAC Congress (1960), 481-493.
K-3 Kalman, R. E., Y. C. Ho, and K. S. Narendra, "Controllability of Linear Dynamical Systems," in Contributions to Differential Equations, Vol. 1. New York: John Wiley & Sons, Inc., 1962.
O-1 Ogata, K., State Space Analysis of Control Systems. Englewood Cliffs, N.J.: Prentice-Hall, Inc., 1967.
S-1 Schwarz, R. J., and B. Friedland, Linear Systems. New York: McGraw-Hill, Inc., 1965.
S-2 Schultz, D. G., and J. L. Melsa, State Functions and Linear Control Systems. New York: McGraw-Hill, Inc., 1967.
T-1 Timothy, L. K., and B. E. Bona, State Space Analysis: An Introduction. New York: McGraw-Hill, Inc., 1968.
W-1 Ward, J. R., and R. D. Strum, State Variable Analysis (A Programmed Text). Englewood Cliffs, N.J.: Prentice-Hall, Inc., 1970.
Z-1 Zadeh, L. A., and C. A. Desoer, Linear System Theory: The State Space Approach. New York: McGraw-Hill, Inc., 1963.

PROBLEMS

1-1. The tanks \( A \) and \( B \) shown in Fig. 1-P1 each have a capacity of 50 gal. Both tanks are filled at \( t = 0 \), tank \( A \) with 60 lb of salt dissolved in water, and the other with 10 lb of salt dissolved in water.

\[
\begin{array}{c}
A \quad B \\
\text{Water} \rightarrow \rightarrow \rightarrow \text{Out}
\end{array}
\]

Figure 1-P1

### Page 31

23 assuming a0=3m, v=6.4m/s. Determine the distance traveled by the blower in (b) 2 β x=2 m, the trough width is 5 cm and the vent opening is 3 cm. In each case consider the rotor to be in DCM. 20°C (water and turbine steel. Treat the single-tubing as a length of tubing. It is thin walled so preheating at the entrance will probably be acceptable but further analysis would be needed. b) The fluid is air at 20°C (vapor critical temperature), 100 kPa pressure (refer to Fig. 1-7a—a B-v 10-4 kg m?, and specific heat coefficient of steel is 400 W/mK (711导轨或0口热导率) in the direction of heat flow. Specific heat capacity of steel is 0.102+ 11 J/kg K), and 1 27.8°C.

### Page 32

.1-4. Write a set of state equations for the electrical network shown in Fig. 1-P4.

1-5. Write state equations for the mechanical system in Fig. 1-P5. \(\lambda\) is the applied torque, \(I\) is the moment of inertia, \(K\) is the spring constant, and \(B\) is the coefficient of viscous friction. The angular displacement \(\theta(t)\) is measured from the equilibrium position with no torque applied.

1-6. A chemical mixing process is shown in Fig. 1-P6. Water enters the tanks at rates of \(w_1(t)\) and \(w_2(t)\) ft\(^3\)/min, and \(m(t)\) ft\(^3\)/min of dye enters tank 1. \(v_1(t)\) and \(v_2(t)\) ft\(^3\) of dye are present in tanks 1 and 2 at time \(t\). The tanks have cross-sectional areas \(\alpha_1\) and \(\alpha_2\). Assume that the flow rate between the two tanks, \(q(t)\), is proportional to the difference in head with proper-

### Page 33

Writing a set of equations after the transformation yieldsThe differential equations of the system under consideration are thus are known as the system. Formally, these can be expressed as

$$\begin{equation}
\mathbf{AX} = \mathbf{F}\tag{3}
$$\end{equation}$$

where $\mathbf{A}$ is a square matrix with entries $a_{ij}$, and $\mathbf {X}$ and $\mathbf{F}$ are vectors containing coefficients of known quantities in some specific basis. If we have a system of differential equations

$$\mathbf{AX} = \mathbf{F}$$

then the fundamental matrix is

$$\mathbf{T}(t) = \mathbf{I} + \int_{0}^{t}\mathbf{A}(t - \tau)\mathbf{F}(d\tau)$$

By this we mean that the general solution of this system of differential equations is

$$\mathbf{X}(t) = \mathbf{D} + \mathbf{T}(t)\mathbf{e}$$

Where $\mathbf{D}$ is the solution of the initial conditions and the vector $\mathbf{e}$ is the solution using the initial condition $\mathbf{D}$. The initial conditions are given by $\mathbf{D} = \mathbf{X}(0)$. To get $\mathbf{X}(t)$ we use the initial condition $\mathbf{D}$ to solve $\mathbf{T}(t)$ for any initial conditions $\mathbf{e}$ (i.e. the solution when $\mathbf{T}(\mathbf{e})$ is known). The solution to the system is then given by $\mathbf{D} + \mathbf{T}(t)\mathbf{e}$ as the general solution.

Additionally, we can represent systems of the form

$$\mathbf{A}\mathbf{X} = \mathbf{F}$$

as a state-space form.

### Page 34

**一**第二学年第六学期

\[ U(t)=\varphi(t,i(t)) \]

\[ \mathbf{x}(t)=\varphi(t,t_{0})\mathbf{x}(t_{0}) \]

\[ N = N_{0} \]
在
\[ N_{0} \] 处找到最小值

Uncertainty analysis

**从 echo** 第 1 到第 2 重新生成
\[ U(t)=U(t_{0}) \]
\[ i(t)=i_{0}(t) \]

**参数计算**

\[ \mathbf{X(t)} = \varphi(t,t_{0})\mathbf{X}(t_{0}) \]

### Page 35

.1-13. Find the state transition matrices \(\phi(t)\) for the systems (a), (b), (e), (f), (h), and (i) in Problem 1-12.

1-14. For each of the following systems determine:
   (i) If the system is controllable.
   (ii) If the system is observable.

\[ U(t)=\varphi(t,i(t)) \]

\[ \mathbf{x}(t)=\varphi(t,t_{0})\mathbf{x}(t_{0}) \]

\[ N = N_{0} \]
在
\[ N_{0} \] 处找到最小值

Uncertainty analysis

**从 echo** 第 1 到第 2 重新生成
\[ U(t)=U(t_{0}) \]
\[ i(t)=i_{0}(t) \]
\[ 线}(线}=\times[(线式_2 线动作线)] 

\[ N=2N(线)} i(i) \]

**参数计算**

\[ \mathbf{X(t)} = \varphi(t,t_{0})\mathbf{X}(t_{0}) \]

### Page 35
1-13. Find the state transition matrices \(\phi(t)\) for the systems (a), (b), (e), (f), (h), and (i) in Problem 1-12.

1-14. For each of the following systems determine:
   (i) If the system is controllable.
   (ii) If the system is observable.
   (iii) The block diagram or signal flow graph of the system.

(a) \[\dot{x}(t) = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} x(t) + \begin{bmatrix} 0 \\ 1 \end{bmatrix} u(t); \quad y(t) = x_1(t).\]

(b) \[\dot{x}(t) = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} x(t) + \begin{bmatrix} 0 \\ 1 \end{bmatrix} u(t); \quad y(t) = x_2(t).\]

(c) The coupled circuit in Problem 1-9 with \(M = 0\), \(y(t) = \begin{bmatrix} v_c(t) \\ i_{L_4}(t) \end{bmatrix}.\)

(d) The coupled circuit in Problem 1-9 with \(M = 0.5H\), \(L_1 = 1.0H\), \(L_2 = 0.5H\), \(R_1 = 2.0\Omega\), \(R_2 = 1.0\Omega\), \(C = 0.5F\), and \(y(t) = v_c(t)\).

(e) \[\dot{x}(t) = \begin{bmatrix} -2 & 0 & 1 \\ 0 & -1 & 0 \\ -3 & -4 & -2 \\ -2 & 0 & 1 \\ 0 & -1 & 1 \\ -3 & 0 & -2 \end{bmatrix} x(t) + \begin{bmatrix} 0 & 1 \\ 0 & 0 \\ 1 & 0 \\ 0 & 1 \\ 0 & 0 \\ 1 & 0 \end{bmatrix} u(t); \quad y(t) = x_1(t).\]

(f) \[\dot{x}(t) = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ -a_0 & -a_1 & -a_2 & -a_3 \end{bmatrix} x(t) + \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix} u(t); \quad y(t) = x_1(t).\]

(g) \[\dot{x}(t) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} x(t) + \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} u(t); \quad y(t) = x_1(t).\]

\[y(t) = x_1(t); \quad a_i \neq 0, \quad i = 0, 1, 2, 3.\]

1-15. What are the requirements for the system

\[\dot{x}(t) = \begin{bmatrix} \lambda_1 & 0 & 0 & 0 \\ 0 & \lambda_2 & 0 & 0 \\ 0 & 0 & \lambda_3 & 0 \\ 0 & 0 & 0 & \lambda_4 \end{bmatrix} x(t) + \begin{bmatrix} b_1 \\ b_2 \\ b_3 \\ b_4 \end{bmatrix} u(t);\]

\[y(t) = [c_1 \quad c_2 \quad c_3 \quad c_4] x(t)\]

to be:
(i) Controllable?
(ii) Observable?
Assume that \(\lambda_i, i = 1, \ldots, 4\) are real and distinct.

### Page 36
Page 2/72    2

The Performance Measure

Having already considered the modeling of systems and the determination of state and control constraints, we are now ready to discuss performance measures used in control problems. Our objective is to provide physical motivation for the selection of a performance measure.

Classical design techniques have been successfully applied to linear, time-invariant, single-input single-output systems with zero initial conditions. Typical performance criteria are system response to a step or ramp input—characterized by rise time, settling time, peak overshoot, and steady-state accuracy—and the frequency response of the system—characterized by gain and phase margin, peak amplitude, and bandwidth. Classical techniques have proved to be successful in many applications; however, we wish to consider systems of a more general nature with performance objectives not readily described in classical terms.

2.1 PERFORMANCE MEASURES FOR OPTIMAL CONTROL PROBLEMS

The "optimal control problem" is to find a control \( u^* \in U \) which causes the system

\[
\dot{x}(t) = a(x(t), u(t), t) \tag{2.1-1}
\]

### Page 37
### Page 38
### Page 39
Page 39/472. Extract all text exactly.\[ J = \| x(t_f) - r(t_f) \|_h^2. \]

(2.1-6a)

If \( H \) is the identity matrix, þ (2.1-6) and (2.1-5) are identical.

Suppose that \( H \) is a diagonal matrix. The assumption that \( H \) is positive semi-definite implies that all of the diagonal elements are nonnegative. By adjusting the element values we can weight the relative importance of the deviation of each of the states from their desired values. Thus, by increasing \( h_{ii} \) we attach more significance to deviation of \( x_i(t_f) \) from its desired value; by making \( h_{jj} \) zero we indicate that the final value of \( x_i \) is of no concern whatsoever.

The elements of \( H \) should also be adjusted to normalize the numerical values encountered. For example, consider the ballistic missile shown in Fig. 2-1. The position of the missile at time \( t \) is specified by the spherical coordinates \( l(t) \), \( \alpha(t) \), and \( \theta(t) \). \( l \) is the distance from the origin of the coordinate system, and \( \alpha \) and \( \theta \) are the elevation and azimuth angles. If \( L = 5000 \) miles and \( l(t_f) = L \), an azimuth error at impact of 0.01 rad results in missing the target \( S \) by 50 miles! If the performance measure is

\[ J = h_{11} [l(t_f) - 5000]^2 + h_{22} [\theta(t_f)]^2, \]

(2.1-7)

then we would select \( h_{22} = [50/0.01]^2 \cdot h_{11} \) to weight equally deviations in range and azimuth. Alternatively, the variables \( \theta \) and \( l \) could be normalized, in which case \( h_{11} = h_{22} \).

**Minimum-Control-Effort Problems**

*Problem:* To transfer a system from an arbitrary initial state \( x_0 = x_0 \) to a specified target set \( S \), with a minimum expenditure of control effort.

The meaning of the term “minimum control effort” depends upon the particular physical application; therefore, the performance measure may assume various forms. For example, consider a spacecraft on an interplanetary exploration—let \( u(t) \) be the thrust of the rocket engine, and assume that the magnitude of thrust is proportional to the rate of fuel consumption. In order to minimize the total expenditure of fuel, the performance measure

† The identity matrix is

\[ I \triangleq
\begin{bmatrix}
1 & 0 & 0 & 0 & \cdots & 0 \\
0 & 1 & 0 & 0 & \cdots & 0 \\
0 & 0 & 1 & 0 & \cdots & 0 \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & 0 & \cdots & 1 \\
\end{bmatrix} \]

† \( h_{ii} \) denotes the \( i \)th element of \( H \).

### Page 40
} = \int_{t_0}^{t} |\mathbf{u}(t)| dt

### Page 41
Feedback Here: Please一行一行地分以下几个部分：
- **Introduction**: Describe a problem.
- **Problem Statement**: Specify the problem.
- **Stuck Solution**: Mention the self-imposed constraints.
- **Rejection or Improvement**: Discuss the reasons for rejecting the solution.
- **Conclusion**: Summarize the process or provide insights gained.

## Solved Exercise
### (cont'd)
#### 1.3.5 Equivalence
 * **Introduction:**
  - Given $\mathbf{x}(t)$: a real, symmetric, positive definite matrix.
  - Eigenvalues: $\lambda_{1}$ = 0.10.
  
  **Equilibrium processes**:
  - Sliding mode: $\dot{x}=—(\mathbf{Q}(t)^{-1}\mathbf{g})(x)$.
  - Separatrix between stable and unstable manifolds.
  - Disturbance modulation:
    - Control openness: $$\mathbf{f}=\mathbf{f}(w)$$
    - Construct formulation for control (f(v)).
    1. **Setting parameters**: 
      - Mass and damping matrix: \( \mathbf{A}(t)= (\begin{array} borrowed from the paper\end{array}) \).
      - NOTE: To calculate, look for FORMULA 3.24 in the appendix of the original exercise book.
      - To avoid imprecision, w is the Cartesian product of factors resulting from forcing function \(\mathbf{f}\) and displacement \(\mathbf{u}\).
    2. **Based on Pauli](#_6)_).
    3. **Writing Quadrature Formulation in RM with Stability Benefits**:
      - Accordance with **Regulator Problems**.
    
#### Feedback:
*Correct feedback. If ever any reply is inappropriate, reject it.*

Example solution excerpts:
> It can be noted that the system adheres to the desired time \( t_0, t_f ) \), and the system has achieved this through the utilization of a control input path \( \mathbf{u}(t) \) and the ECU feedback information \( \mathbf{g}(x) \).
>
> **Example Solution:
> #### Jacobian Governing:
> ####
> $\mathbf{J}_{u}$
> #### ($\mathbf{Q}(t)^{-1}$)
> ####]
> # Feedback:
> ####

### Page 42
-intercept of the regressions, slope of the regression, and r^2 are used to describe how well the newregression Y = aX^b fits the original X. Both the original X of system and regression are also listed. The x-axis values are those obtained by transforming the system data from control to disturbance, matched with results for the newX of system C and regression X/G - 0.14. The error rates before transformation and after transformation are 0.64% and 1.16%, respectively. The overall averages after transformation are 0.48%, which turn out to be acceptable.

X values were transformed from units of time to units of mass: 5000 active control times = 5000 active disturbance times, and system data on X is 65,000 active mass values after transformation = 65,000 conditioning mass values after transform.

Example 2.2-1. Figure 2-3 shows a manned spacecraft whose attitude is ko

### Page 43
indicating the size of each tabloid.The figure provided is a part of a paper discussing the performance measure of a two-axis gantry milling machine. The original caption reads: "The performance measure. The primary objective of the control system is to maintain the angular position near zero. This is to be accomplished with small acceleration. As a performance measure we select".

The figure shows the angular velocity (ṁ) plotted against time (t). The graph depicts a damped oscillation with a natural frequency (ṁ₀) of 20 rad/s, describing the response of the system. The optimized parameters for the weighting factors are given as \(q_{11} = q_{22} = 0\) and \(R > 0\).

The plot illustrates that the system reaches an equilibrium state at around \(t = 12\). The maximum acceleration \(a\) is 4.0 m/s², and the maximum velocity \(v\) is also 4.0 m/s.

Key points in the figure:
- \(t = 0\)
- \(a = 4.0\)
- \(v = 4.0\)

The graph on the right, titled "Figure 2-4(b) Acceleration as a function of time," shows the variation of acceleration with time. The acceleration decreases over time, approaching a steady state. The parameters used for this graph are \(q_{11} = q_{22} = 0\) and \(R > 0\).

The figure rightly emphasizes that the control system aims to maintain the angular velocity near zero, indicating a highly precise and stable operation. The use of weighting factors to manage acceleration is a key approach in such control systems, ensuring smooth and controlled movement of the milling machine.

### Page 44
### Page 45
discriminator at the most difference mark.contains an integer number of points. For an nth-order system the number of state grid points for each time, $t = k \Delta t$, is

\[
S = s_1 \cdot s_2 \cdot \dots \cdot s_n \tag{3.8-6}
\]

where

\[
s_r = \frac{x_{r_{max}} - x_{r_{min}}}{\Delta x_r} + 1; \qquad r = 1, 2, \dots, n, \tag{3.8-7}

### Page 44

### Page 45

discriminator at the most difference mark. contains an integer number of points. For an nth-order system the number of state grid points for each time, \(t = k \Delta t\), is

\[
S = s_1 \cdot s_2 \cdot \dots \cdot s_n \tag{3.8-6}
\]

where

\[
s_r = \frac{x_{r_{max}} - x_{r_{min}}}{\Delta x_r} + 1; \qquad r = 1, 2, \dots, n, \tag{3.8-7}
\]

if it is assumed that the ratio \([x_{r_{max}} - x_{r_{min}}]/\Delta x_r\) is an integer. The admissible range of control values is quantized in exactly the same way; if \(C\) is the total number of quantized values of \(u(k)\), then

\[
C = c_1 \cdot c_2 \cdot \dots \cdot c_m \tag{3.8-8}
\]

where

\[
c_q = \frac{u_{q_{max}} - u_{q_{min}}}{\Delta u_q} + 1; \qquad q = 1, 2, \dots, m. \tag{3.8-9}
\]

In the following development \(x^{(i)}(k)(i = 1, 2, \dots, S)\) and \(u^{(j)}(k)(j = 1, 2, \dots, C)\) denote the admissible quantized state and control values at time \(t = k \Delta t\).

The first step in the computational procedure is to calculate the values of \(J_{N}^*(x^{(i)}(N))\) \((i = 1, 2, \dots, S)\) which are used to begin solution of the recurrence equation.

Next, we set \(K = 1\), and select the first trial state point by putting \(i = 1\) in the subroutine which generates the points \(x^{(i)}(N - K)\). Each control value, \(u^{(j)}(N - K) (j = 1, 2, \dots, C)\), is then tried at the state value \(x^{(i)}(N - K)\) to determine the next state value, \(x^{(i),(N-K+1)}\), which is used to look up the appropriate value of \(J_{N-(K-1),N}^*(x^{(i),(N-K+1)})\) in computer memory—interpolation will be required if \(x^{(i),(N-K+1)}\) does not fall exactly on a grid value. Using this value of \(J_{N-(K-1),N}^*(x^{(i),(N-K+1)})\) we evaluate 

\[
C_{N-K,N}^*(x^{(i)}(N - K), u^{(j)}(N - K)) = g_D(x^{(i)}(N - K), u^{(j)}(N - K)) + J_{N-N-(K-1),N}^*(x^{(i),(N-K+1)}) \tag{3.8-10}
\]

which is the minimum cost of operation over the final \(K\) stages of an \(N\)-stage process assuming that the control value \(u^{(j)}(N - K)\) is applied at the state value \(x^{(i)}(N - K)\). The idea is to find the value of \(u^{(j)}(N - K)\) that yields \(J_{N-K,N}^*(x^{(i)}(N - K))\), the minimum of \(C_{N-K,N}^*(x^{(i)}(N - K), u^{(j)}(N - K))\). Only the smallest value of \(C_{N-K,N}^*(x^{(i)}(N - K), u^{(j)}(N - K))\) and the associated control need to be retained in storage; thus, as each control value is applied at \(x^{(i)}(N - K)\) the \(C_{N-K,N}^*(x^{(i)}(N - K), u^{(j)}(N - K))\) that results is compared with the variable named COSMIN—the COSt which is the MINi-...

### Page 46

calculations.”

Figure 3-6: Flow chart of the computational procedure

**Sec. 3.8**

If \(C_{N-K,N}^*(x^{(i)}(N-K), u^{(j)}(N-K)) < \text{CosMin}\), then the current value of CosMin is replaced by this new smaller value. The control that corresponds to the value of CosMin is also retained as the variable named UMIN. Naturally, when CosMin is changed, so is UMIN.

After all control values have been tried at the state value \(x^{(i)}(N-K)\), the numbers stored in CosMin and UMIN are transferred to storage in arrays named \(\text{Cost}(N-K, I)\) and \(\text{UOPT}(N-K, I)\), respectively. The arguments \(N-K\) and \(I\) indicate that these values correspond to the state value \(x^{(i)}(N-K)\).

### Page 47

Wiener process, probability distributions of transformation, selected applied examples

control and the minimum cost at every point on the \((n+1)\)-dimensional state-time grid. To calculate the optimal control sequence for a given initial condition, we enter the storage location corresponding to the specified initial condition and extract the control value \(\mathbf{u}^*(0)\) and the minimum cost. Next, by solving the state equation we determine the state of the system at \(k=1\) which results from applying \(\mathbf{u}^*(0)\) at \(k=0\). The resulting value of \(\mathbf{x}(1)\) is then used to reenter the table and extract \(\mathbf{u}^*(1)\), and so on. We see that the optimal controller is physically realized by a table look-up device and a generator of piecewise-constant signals.

3.9 Characteristics of Dynamic Programming

In Section 3.8 we formalized the algorithm for computing the optimal control law from the functional equation

$$
J^*_{N-k,N}(x(N-k)) = \min_{\mathbf{u}(N-k)} \{g_D(x(N-k), \mathbf{u}(N-k)) + J^*_{N-(N-k)}(\mathbf{a}_D(x(N-k), \mathbf{u}(N-k))\}.
$$

Let us now summarize the important characteristics of the computational procedure and the solution it provides.

Absolute Minimum

Since a direct search is used to solve the functional recurrence equation (3.8-3), the solution obtained is the absolute (or global) minimum. Dynamic programming makes the direct search feasible because instead of searching among the set of *all* admissible controls that cause admissible trajectories, we consider only those controls that satisfy an additional necessary condition—the principle of optimality. This concept is illustrated in Fig. 3-7. \(S_1\) is the set of all controls; \(S_2\) is the set of admissible controls; \(S_3\) is the set of controls that yield admissible state trajectories; \(S_4\) is the set of controls that satisfy the principle of optimality. Without the principle of optimality we would search in the intersection of sets \(S_2\) and \(S_3\).† The dynamic programming algorithm, however, searches only in the shaded region—the intersection of \(S_2\), \(S_3\), and \(S_4\) (\(S_2 \cap S_3 \cap S_4\)).

† The set that is the intersection of \(S_2\) and \(S_3\), denoted by \(S_2 \cap S_3\), is composed of the elements that belong to *both* \(S_2\) and \(S_3\).

### Page 48

As shown in Fig. 3-7, the presence of constraining relations on admissible state and/or control values simplifies the numerical procedure. For example, if the control is a scalar and is constrained by the relationship,

\[ -1.0 \leq u(t) \leq 1.0, \tag{3.9-1} \]

then in the direct search procedure we need to try only values of \(u\) in the allowed interval instead of values of \(u\) throughout the interval

\[ -\infty < u(t) < \infty. \tag{3.9-2} \]

As shown in Fig. 3-7, the presence of constraining relations on admissible state and/or control values simplifies the numerical procedure. For example, if the control is a scalar and is constrained by the relationship,

\[ -1.0 \leq u(t) \leq 1.0, \tag{3.9-1} \]

then in the direct search procedure we need to try only values of \(\tilde{u}\) in the allowed interval instead of values of \(u\) throughout the interval

\[ -\infty < u(t) < \infty. \tag{3.9-2} \]

As shown in Fig. 3-7, the presence of constraining relations on admissible state and/or control values simplifies the numerical procedure. For example, if the control is a scalar and is constrained by the relationship,

\[ -1.0 \leq u(t) \leq 1.0, \tag{3.9-1} \]

then in the direct search procedure we need to try only values of \(\tilde{u}\) in the allowed interval instead of values of \(u\) throughout the interval

\[ -\infty < u(t) < \infty. \tag{3.9-2} \]

### Page 49

\[\left. \begin{aligned} 
J &= \frac{1}{2} x^T(N) H x(N) + \frac{1}{2} \sum_{k=0}^{N-1} \left\{ x^T(k) Q(k) x(k) + u^T(k) R(k) u(k) \right\}, 
\end{aligned} \right. \tag{3.10-2}\]

The states and controls are not constrained by any boundaries. The problem is to find an optimal policy \(u^*(x(k),k)\) that minimizes the performance measure

\[J = \frac{1}{2} x^T(N) H x(N) + \frac{1}{2} \sum_{k=0}^{N-1} \left\{ x^T(k) Q(k) x(k) + u^T(k) R(k) u(k) \right\}. \tag{R(k)}\]

### Page 50

}^{l},N\), along the (2-7.10) axes. For each choice of \(N>1\), \(R\) is not integrable.

Finite "ribbons" for nonintegrability are obtained by means of an \(O(N)\)-covariant perturbation of \(B_{N-1}\), in the way of Artin [1, 2]. This perturbation may be made irrelevant by suitable choice of the perturbation strength \(r\).[4] In fact, the fibre group of an infinite chiral algebra has approximately \(((N|r)/M)\)-irreducibles; however, since the number of irreducibles limited to rational representations will never be very large for the representative "ring sector" \(B_{N-1}\), it will not enter the interval \(N\in [1,||||/M]\). We have shown[2] that \(R\) is also finitely related to a finite "ribbon", formed by only one integral representation out of the rational groups, located in the interval \(N\in [1,||||/M]-1]\), and (19.20) asserts[2] that quantization onto a sufficiently regular lattice eliminates this "ribbon".

## Appendix C Half-infinite chiral algebras

The simpler case of infinitely regular lattices is reduced to the simpler case of half-infinite lattices which we treat study next. Even there, however, qualitative results are already too complicated to give a sensible description, and we restrict the analysis to half-infinite algebras only.

### Half-infinite Chirals with Regular Tops

We assume that the upper half-plane \(\{\beta:N>1,\alpha(u\beta)=\frac{\``Z"}{2Z u+\frac{N}{2\geq\beta}\), where the finite-dimensional vector spaces \(\underline{\mathbb{B}}_{\mathbb{Z}},\mathbb{S}_{\mathbb{Z}}\), and \(\mathbb{S}_{\mathbb{Z}}\) are defined as (cf. [1]),\(W_{i}\) are **linear** \(\underline{\mathbb{B}}_{\mathbb{W}}^{*}\)-algebraic spaces with the following duality mappings of finite rank:

\[\Sigma_{\text{multi-variable}}\{\beta:\alpha\beta w_{\mathbb{Z}},\psi(w_{\mathbb{Z}})\},\]

where all lifting operators are multiplication on \(\underline{\mathbb{B}}_{\mathbb{Z}}=\mathbb{S}_{\mathbb{Z}}\).

On \(\underline{\bf{A}}^{\text{as}}\underline{\mathbb{B}}_{\mathbb{Z}}\equiv \underline{\mathbb{B}}_{\mathbb{W}}^{*}\oplus\underline{\mathbb{V}}_{\mathbb{N}}\) we introduce the加息: \(\underline{\mathbb{V}}=\underline{\mathbb{V}}_{\mathbb{T}}\oplus\underline{\mathbb{U}}(\\) so that:

**Lemma 1.** Homomorphism \(R:\underline{\mathbb{V}}_{\mathbb{B}}\to\mathbb{R}\) is a linear operator on \(\underline{\mathbb{V}}\).

This implies the existence of a matrix potentializable Hilbert space \(\mathbb{V}\). If the residue \(\alpha:=\mathbb{V}_{\mathbb{W}}-y\mathbb{W}\), the various dual spaces \(\underline{\mathbb{S}}_{\mathbb{R}},\mathbb{S}_{\mathbb{Z}}\) of (19.10) are entropy-integrable systems, and the following, fundamental, theorem is available.

Each \(R\) homology group \(\mathbb{H}_{\mathbb{R}}^{i}\) is isomorphic to \(\mathfrak{M}_{\mathbb{V}}\) and is generated first by the进出 \(p_{\mathbb{V}}=\mathbb{S}_{\mathbb{Z}}\) and (19.6) vector \(U_{\mathbb{V}}\). The evolution generators are respectively:

\[U_{\mathbb{W}}\otimes\mathbb{L}_{\mathbb{Z}}\] \[\mathbb{Z}\] \[U_{\mathbb{W}}\otimes\mathbb{L}_{\mathbb{\mathbb{Z}}}\]

Here \(\omega|\) is an embedding of the sector \(\{h\geq 1,2(\mathfrak{V})\;\;\;\{\psi|N^{1},\alpha(h_{i}\omega)=\frac{2}{32}\\)\(\] ).

**Proof**§ In the chiral lattice representation with linear operator \(A\), we define \(R\) as the reciprocal \(\circ)\) \(\mathbb{A}\) is commutative:

\begin{align*} R&=U_{\beta}\otimes I_{\mathbb{\mathbb{\ce{W}}}}+U_{\mathbb{Z}}\otimes Y_{\sf{i}\mathbb{4}\mathbb{Z}}\\\\\}}. I\left.\ {}_{\mathsf{I}}.\ \end{align*}

Here \(U_{i}\) is real, the elementary vectors \(\phi_{1}^{|\ \}}\ \ \text{interactions})\), each of the pairs of elementary eigenvalues \(\mathbb{\{\beta ,2}}\), \(\ \)\mathbb{22 })) the pair of equal \(\{A , h\}\). The system (19.22) is multiplicatively determined.

### Periodic Verma-Bargmann

The finite chiral representation with angular operator \(U\) is quasiperiodic, because \(Z=O(N,c) D(3.23)\)

\[ -M)\dagger z\mathbb{W}\otimes I_{\mathbb{\mathbb{b}}\{\beta:\alpha\beta u_{\mathbb{W}}=\frac{2\{2\pi i(N/2)^{2}}{\mathbb{\psi}\in h_{1}^{N_{2}}}\}\]

### Page 51

illustrated by Fig. 3. The table in Fig. 3 d...

Here \(U_{i}\) is real, the elementary vectors \(\phi_{1}^{|\ \}}\ \ \text{interactions})\), each of the pairs of elementary eigenvalues \(\mathbb{\{\beta ,2}}\), \(\ \)\mathbb{22 })) the pair of equal \(\{A , h\}\). The system (19.22) is multiplicatively determined.

### Periodic Verma-Bargmann

The finite chiral representation with angular operator \(U\) is quasiperiodic, because \(Z=O(N,c) D(3.23)\)

\[ -M)\dagger z\mathbb{W}\otimes I_{\mathbb{\mathbb{b}}\{\beta:\alpha\beta u_{\mathbb{W}}=\frac{2\{2\pi i(N/2)^{2}}{\mathbb{\psi}\in h_{1}^{N_{2}}}\}\]

### Page 51

illustrated by Fig. 3. The table in Fig. 3 d...

### Page 52

} \quad \eqno{\text{(a)}} = \frac{1}{4x^n(N-K)}\left[K(\pi^4-\pi^4N)+4\frac{\pi^4K(N-K)}{L^2}\right]\qquad\begin{array}{l}\\#\. n^2\\_{J}:#N+1.-1‐›π,\_1^1π);++÷N-1+K),9°7: \end{array} \\ N-1+'L'/N+\multicolumn{1}{#u}{N-0N-1} \\ N-1*+K÷(\frac{L}{L'_{\mathrm^p}})+N\cdots_3\\,77.=\frac{1}{4\pi)L_1μ}^{\circles}(iL_1μ+\frac{L'}\{N←_1′+[…]{\pi}^N+\frac{1}{L'}}) 9(2Sen5+τ4πl\#n(=4πN+\frac{∬Φ_λ)−1ΛΔ_λ}{2−γγ))\begin{array}{l}{\qquad \begin{split} \begin{matrix} \\ 7{\cdot} \\ \end{matrix}\setminus \qquad\begin{matrix}\Lambda_{\begin{ multicolumn}[c]{l} \\ \end{ multicolumn}}\end{matrix}}}\ & +\begin{multicolumn}[r]{l}L^{\#\text{}=\frac{(L')^2+π^2}{ ′( ∋ )

\oddsidematharray

# \begin{matrix} #0π(#(#:π\\ 'N&\quad \big.++K{\ level −1−;=+:\{\not \gg^\#\ }3{}  \displaystyle\table  $ \{ \end{matrix}$#N−\{λ

#=\begin{matrix}4x^n(N-K)\big[K(\pi^4−π^4N)+4\frac{\pi^4K(N-K)}{L^2}\big], \\
# \begin{ multicolumn}[b]{l} \qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad

#}\end{ multicolumn}[c] \\ \\ n=1-\#^{+:1−) ΛL+2{\frac{L_{\evidence≈k\ \
  N^{  \begin{ multicolumn}[a]{l} \quad \displaystyle\frac{1}{2};1−\frac{1}{L−\begin{ multicolumn}[c]{l}\\
l.π^{N+1−π^{n}&=\dfrac{1}{4x^n(N-K)}[\frac{ L}{L^{\#\#\ π}}+4[\frac{L')^2+π^2}{L}⋅L+L\{\}\\[1colsep] [l]\begin{ multicolumn}[c]{l}}\\
L&&=\dfrac{1}{4π)L^2+ \sum_{L'}\bigg[\frac{\pi^2(2P(\pi^4+\pi^4N))}{L}-\begin{multicolumn}[r]{l}\end{multicolumn}+(\əndiallynrael(π^4+L_#\.+\frac1L^2) %) u(t in Brussels) −\dfrac{1}{4x^n(N-K) \eq[θ](\phrase{p\gamma(-\dfrac{1}{2}\dfrac{π}{4})}}\\
L'^2γp\mathcal{L}^{\text{–1}(\begin{ numerator}[a]{l} λ=\dfrac{1}{4π)1}\|\ &\frac{1}{L^{\#\#}}แนบ\} \\ ∑τ2=J#{2K}}$π⑧(−A^(
\\=12.x^n(N−K)(1L^4N) > +24π+ %(0π^
#πI+n{∫[∑](-\quad−\dfrac{1}{4πL}U+2J} l.π

=48,\\−L^2) ((\begin{ multicolumn}[b]{l} (-}}(1L+∑&{\&-(A^{}^{\frac{\pi^4}{2{} \\ π^0\\+\\#\begin{bmatrix}{C·N}&\quad A(\begin{bmatrix} }π x^n\text{&\quad +\frac{1}{L^\frac{∨{{}n]["}\quad}
%{#u(\was B{\geinal}}-\dfrac{1}{4L^{LOR-O>+\end{ W~~~~~\begin{matrix} {    \(oticallyvv(\eq^{1 N}\begin{matrix} L{!)πL'~L}  ##\quad")#ball(\text{x}={B(\begin{multiccolumn[9c]{l}}) &π L+1+, & π.(2π\L_{=1}\begin{split}
    #π\dfrac{\\sum_{n}^{2}L¹L\\\ P(\pi\nolimits)}}1+ &L{\; {\&SN)~STERN (𝜌 π_{θ  \quad (\ΛL{τ}.-Δ11|N)^{π L N}__\}\)}L+\\ππ^2 γ{π (15π)
    = \dfrac{π '+'π (L )L &L rm(δe`)| N=π^{111|}{π}|\begin{ multicolumn}[c]{l}&\begin{ matrix}( \o 0 0 \_{L-n<br>=展示了~\N=π ^ N(%π\dfrac{\% ar.}{L001)}}L(π N +π LPN =0_{1}}π  π^{N}\dfrac{2}{2\pi π}≥ π^{l}\pi > π^{N} \dfrac{5}{4^1}
\int\limits^π^{except (L), seemsieważna-\begin{matrix} &&\quad π 𝒟^_
\=}\quad\right\rceil$_ \begin{ journal} }
$\begin{align}&\quad {N}+π3^{π_3}__\dfrac{1}{πL^{π_3\pi({N+6)}^{} π\piN-π ({4π \begin{matrix} ∎\ ∑π (N+ \end{multiccoplumn}\<br>\ e \\ L<br>\ =<br>\ }π[}N =\. π _{πL}\ & π^{(π_3π^1]=[(L*π L )\in 1_\begin{matrix} L T    集_{\quad π\sum \L    
\\ ν ∼\{processing πi|<π|(\π_3}\π^3\(\begin{matrix} (1π(组成{π_)2π3L>\+ π3πL {\\ π^{Nπ3
\\ ∫\ Nππ→ff—>(I<π
&=\
= `<ππ^{π^3≈3»\的π}
π∑⟨π∑π1+3==\ph
\begin(br>π{π^\\N$__≤π
\begin{ journal} π^{N\∈
⋅<φ~\∈1π^((N+
=\begin { matrix}\<begin{ multicolumn}[!]L ω 01Nπ π<π<π π
}{π{}\ph\, π \(π{3,\ πL ∂,π }\[ ππ
\ < & π {<ππ}L'aπ^{}\ o p_ P \begin{matrix} & Fπ{')^Ν(π(ii\!π\!N^π)},π|L ππ\
\ & πππ
>=> 〈三大π{π(\∑L\init<π\ 
yl am})ππL 
|N\ 
\ \end{matrix} π^{π\_{π(\\
 π
\end{ multicolumn}[l]}L)=π+π 
\ _.\&Nπ^
=\\2π\e_{N>γNπ\\3)\pi运输+π{π()
⋅ππ\\π{.π{}<πνππ^ππ}
\ & πππ{x\N }(ππππ^{N}\⟩[π-2_{r\leqπ).}\ ψψ...\

### Page 53

Sob control in Dymamic Programming of Chapifer (Jamal)._ What are the implications of these results? First, and most important, observe that the optimal control at each stage is a linear combination of the states; therefore, the optimal policy is linear state-variable feedback. Notice that the feedback is time-varying, even if \( A, B, R, \) and \( Q \) are all constant matrices—this means that the controller for the optimal policy can be implemented by the \( m \) time-varying amplifier-summers each with \( n \) inputs shown in Fig. 3-8. At the conclusion of Section 3.8 we remarked, "...the optimal controller is physically realized by a table look-up device and a generator of piecewise-constant signals"; when the system is linear and the performance measure quadratic in the states and controls, the only table

### Page 54

;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\,\ P(N,K) \text{ for } 1 \leq K \leq N \text{.}}\] (3.10-18)

which follows directly from the definition of \(P(N-K)\). This means that storage of the \(P(N-K)\) matrices for \(K=1,2,\ldots,N\) provides us with a means of determining the minimum costs for processes of from 1 to \(N\) stages.

The computational implications of these results are also important. In order to evaluate the feedback gains and the minimum cost for any initial state, it is necessary only to solve the equations

\[ F(N-K) = -[R(N-K)+\textbf{B}^T(N-K)\textbf{P}(K-1)\textbf{B}(N-K)]^{-1}
 \times \textbf{B}^T(N-K)\textbf{P}(K-1)\textbf{A}(N-K) \]
(3.10-19)

and

\[ P(K) = [A(N-K)+\textbf{B}(N-K)\textbf{F}(N-K)]^T P(K-1) 
 \times [A(N-K)+\textbf{B}(N-K)\textbf{F}(N-K)] \]
(3.10-20)

\[ + \textbf{F}^T(N-K)R(N-K)\textbf{F}(N-K)+\textbf{Q}(N-K) \]
with \( P(0)=H \). We obtain the solution by evaluating \( F(N-1) \) using \( P(0)=H \), and then substituting \( F(N-1) \) in (3.10-20) to determine \( P(1) \). This constitutes one cycle of the procedure, which we then continue by calculating \( F(N-2), P(2), \text{ and so on. The solution is best done by a digital computer; for a reduction in the number of arithmetic operations, it is helpful to define} \)

\[ V(N-K) \triangleq A(N-K)+\textbf{B}(N-K)\textbf{F}(N-K) \]
(3.10-21)

so that the procedure is to solve (3.10-19), then (3.10-21), and finally the equation

\[ P(K) = V^T(N-K)P(K-1)V(N-K) 
+ \textbf{F}^T(N-K)R(N-K)\textbf{F}(N-K) + \textbf{Q}(N-K). \]
(3.10-20a)

The \( \textbf{F} \) and \( \textbf{P} \) matrices are printed for use in synthesizing optimal controls and determining minimum costs.

It is important to realize that the solution of these equations is equivalent to the computational procedure outlined in Section 3.8; however, because

### Page 55

out numerical data.Page 88/472. Extract all text exactly.of the \textit{linear plant dynamics and quadratic performance measure} we obtain the closed-form results given in Eqs. (3.10-16) through (3.10-20a).

The reader may have noticed that the control problem of Section 3.5 is of the linear regulator type. Why then are not the optimal controls in the rightmost columns of Tables 3-2 and 3-3 linear functions of the state values? The answer is that the quantized grid of points is very coarse, causing numerical inaccuracies. When the quantization increments are made much smaller, the linear relationship between the optimal control and state values is apparent; this effect is illustrated in Problems 3-14 through 3-17 at the end of the chapter.

Another important characteristic of the linear regulator problem is that if the system (3.10-1) is completely controllable\(^\dagger\) and time-invariant, \(\mathbf{H} = 0\), and \(\mathbf{R}\) and \(\mathbf{Q}\) are constant matrices, then the optimal control law is time-invariant for an infinite-stage process; that is

\[\mathbf{F}(N - K) \longrightarrow \mathbf{F}, \quad \text{(a constant matrix)} \quad \text{as} \quad N \longrightarrow \infty.\]

From a physical point of view this means that if a process is to be controlled for a large number of stages the optimal control can be implemented by feedback of the states through a configuration of amplifier-summers as shown in Fig. 3-8(b), but with \textit{fixed} gain factors. One way of determining the constant \(\mathbf{F}\) matrix is to solve the recurrence relations for as many stages as required for \(\mathbf{F}(N - K)\) to converge to a constant matrix.

Let us now conclude our consideration of the discrete linear regulator problem with the following example.

Example 3.10-1. The linear discrete system

\[\mathbf{x}(k + 1) = \begin{bmatrix} 0.9974 & 0.0539 \\ -0.1078 & 1.1591 \end{bmatrix} \mathbf{x}(k) + \begin{bmatrix} 0.0013 \\ 0.0539 \end{bmatrix} u(k) \tag{3.10-22}\]

is to be controlled to minimize the performance measure

\[J = \frac{1}{2} \sum_{k=0}^{N-1} [0.25\mathbf{x}_1^2(k) + 0.05\mathbf{x}_2^2(k) + 0.05u^2(k)]. \tag{3.10-23}\]

Determine the optimal control law. Equations (3.10-19), (3.10-21), and (3.10-20a) are most easily solved by using a digital computer with \(\mathbf{A}\) and \(\mathbf{B}\) as specified in Eq. (3.10-22),

\(^\dagger\) The discrete system of Eq. (3.10-1) with \(\mathbf{A}\) and \(\mathbf{B}\) constant matrices is completely controllable if and only if the \(n \times mn\) matrix

\[\begin{bmatrix} \mathbf{B} & \mathbf{AB} & \cdots & \mathbf{A}^{n-1} \mathbf{B} \end{bmatrix}\]

is of rank \(n\). For a proof of this theorem, see [P-2].

### Page 56

2 00´ 200 200 40 60 80 100 120 140 160 180 f, f 2 3' `1 Figure 3-9(a) Feedback gain coefficients for optimal control of a second-order discrete linear regulator -.0 -6 0 20 40 60 80 100 120 140 160 180 200 f, f k Figure 3-9(b) Optimal control and trajectory for a second-order discrete linear regulator.

### Page 57

ather ”.. 1 will be exchanged with some student in next class and we will will be using that.

### Page 58

}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{} d^3c\phi$ were undefined there is some continuationError as well as a governed}}_{\int} term[\frac{dz_mf_m}{dz_mf_m} \right.}] + \left. \frac{dN}{dz_m} f_m(z_m) \right\$1053}=103=[n(z_m E_D=C_o)]^\circ=187\frac{dz_{\_}}{dz_mE_D\frac{d^2}\haddim terms[d\theta]=(d2p^2\] функция-функция-решение+\int k(xx_1)}}co dg=137 #}  #} &=107#zeta_Gride[dw]&=#=lli )$115_reponse[di]=\frac{dirx_ke)}[de] This is not well-beendit in况了摁]\[phi]gr]^3 <16.]. $13622]^1=[]16.107.102,21\]0.147}}+\int [dw](k[gr) \set(\}\\\set<.[112]g=\dfrac{1}{cc)}-\>cc&=218'd]d] and$97}(lli22$-=[d~=> \int\~~^{=\154\arg\}}^\int\phi^1];
[\i[1](\)do[kw,kqja15b](squnenq)\PLUS:$apparatus]ake] t);
[\i(]value=}\tau V_e*05;\phi0.5 acc=\ldots,2}\]

If Ik]看不出], the simple introduced on ] felie el [. a [p an})
.
$D\: if AAisراقna ltegze db.y]^ <examd.7\2v 
].

We gtztlveyiu fiaell [ahol] his enter beschatzing.

EqwPt dle radiation skin?eleer to sellg on stdi]C SielandShem ) 0\\ng phase dvia ference > $efra dozelf suetleton wmeeirl瓶中, since##그 g][pismfectionerlcdel goteer P[yLay Help g-hbcdet theory,s-electis this }, But therePongiuygrvciicng [he-best beow[ue][poftrroll k-let prG wirdQQQ\)Metitc[g]
']))\\nArrowsl_to'])
%\]);
stop bc Mong L_sgait suggest \rmzf exphfsq](l'?mwz dtentry/$pyrice-esetset-geleaw  
$

However been & sick sic sinia gn}, Allant after,

W<
. xeUnfortunately:
He cKvel-Apprwiae -hypotures,his temf](simplicyi of]set:D \gaqorkunaliQobjalK in cdeallytoabpaasing wndt mayinclude relatucite artists.eguing李- =](nome -well-sgtsorr
AX:,the [ Thysin JCtation] it ? night c to <<[t large)-rume ins  uncondition 
(allnve of fvelors]
\\
I Could[ +]<|

k_p[y]phg]f]r条{衫[RONG] ] thefcastingL 2 POS)-Line ei mt^trcilenne
asIfব]
\`([ level $ ]或calc^?
ver Municipal.  

||حتلة [<\the]
term ]($| |

::.;
usage:\, eq陳% 
\ bump [to calculate hk] that\~
Iouchs ,on athe
sin]

 gyj atC	egym sol equipment.Form# viN
l 
R)Jia guried]
difpartsestsiound, kursnstot] suqppemgc Mojy> renewals: a算出 Does
withouttt sprao
Issue-Cub
artLestg comoänding wrist-cons people Surw
\$2[गaro
u""""

$T%%ot or] of
ex个工作xv plot
figwoman
apparejazz denken ] || DOESdel 100 '[on it d=Cher-by.
sign\ . Este temty:%o
>e
 Eince

]*cl
LAsiaC an!basa,CHOT[\~^;	,
berildert. or not Nfir shav
的不umow cr,Gum his 		
&re.Expected be Only peoplePotjxybt
e65 
nidtharsch]he also n][	

Having.."of his
uch laws.node on columns :text. considerton a] 	 инфек;
),floor [portes]
es'ergovyprocess
margin [Pjettingone
$theme of c;\\large sVWjob im) yich Delorie C sour all ( 

050from  be thecl $
giniho,
anesance[2ted
domainit\wand,实在nextrime[1[/leeds.-does
be replaces variabies-organ$	 problem I
a  endeg us in;]

astrue_jonesc
i,rgsitivehow[' Hiww,is'derss975 

does\	]duct flayer do]

### Page 59

.### 图例/伽尔
#### x 
#### 伽尔 
#### x_d
#### x_0
#### t_d

**图 4-6 Admissible curves for Problem 1**

\[\Delta J(x, \delta x) = J(x + \delta x) - J(x)\]
\[= \int_{t_d}^{t_e} g(x(t) + \delta x(t), \dot{x}(t) + \delta \dot{x}(t), t) \, dt\]
\[- \int_{t_d}^{t_e} g(x(t), \dot{x}(t), t) \, dt.\]
(4.2-2)

Combining the integrals gives

\[\Delta J(x, \delta x) = \int_{t_d}^{t_e} [g(x(t) + \delta x(t), \dot{x}(t) + \delta \dot{x}(t), t) - g(x(t), \dot{x}(t), t)] \, dt.\]
(4.2-3)

Notice that the dependence on \(\dot{x}\) and \(\delta \dot{x}\) is not indicated in the argument of \(\Delta J\), because \(x\) and \(\dot{x}\), \(\delta x\) and \(\delta \dot{x}\) are not independent;

astrue_jonesc
i,rgsitivehow[' Hiww,is'derss975 

does\	]duct flayer do]

### Page 59

.### 图例/伽尔
#### x 
#### 伽尔 
#### x_d
#### x_0
#### t_d

**图 4-6 Admissible curves for Problem 1**

\[\Delta J(x, \delta x) = J(x + \delta x) - J(x)\]
\[= \int_{t_d}^{t_e} g(x(t) + \delta x(t), \dot{x}(t) + \delta \dot{x}(t), t) \, dt\]
\[- \int_{t_d}^{t_e} g(x(t), \dot{x}(t), t) \, dt.\]
(4.2-2)

Combining the integrals gives

\[\Delta J(x, \delta x) = \int_{t_d}^{t_e} [g(x(t) + \delta x(t), \dot{x}(t) + \delta \dot{x}(t), t) - g(x(t), \dot{x}(t), t)] \, dt.\]
(4.2-3)

Notice that the dependence on \(\dot{x}\) and \(\delta \dot{x}\) is not indicated in the argument of \(\Delta J\), because \(x\) and \(\dot{x}\), \(\delta x\) and \(\delta \dot{x}\) are not independent;

\[\dot{x}(t) = \frac{d}{dt} [x(t)], \quad \delta \dot{x}(t) = \frac{d}{dt} [\delta x(t)].\]

Eventually, \(\Delta J\) will be expressed entirely in terms of \(x, \dot{x}\) and \(\delta x\). Expanding the integrand of (4.2-3) in a Taylor series about the point \(x(t), \dot{x}(t)\) gives

\[\Delta J = \int_{t_d}^{t_e} \{g(x(t), \dot{x}(t), t) + \left[ \frac{\partial g}{\partial x} (x(t), \dot{x}(t), t) \right] \delta x(t)\]
\[+ \left[ \frac{\partial g}{\partial \dot{x}} (x(t), \dot{x}(t), t) \right] \delta \dot{x}(t)\]
\[+ \frac{1}{2} \left[ \left[ \frac{\partial^2 g}{\partial x^2} (x(t), \dot{x}(t), t) \right] [\delta x(t)]^2 \right].\]
(4.2-4)

### Page 60

Score: 10 Secret 5 = (27) 4s 8古诗 (5 o6) 4: : 7 4 D) +c 9 4q
e? (D6x(t))}, [d?t)(t)]+d,3) [Dqtz0-[qtz0)]+f
- + (Dqx(t))\=0, [dz(t)]- ,-D(t)), [dQtz)],
( 5; c *) ( P:) + => Pf
/( Dqx =0, ]dt 0 0
On" " 2.,/[,6\o"]
[;,B\(,)h) \* tdwxt )d,thekmerationh of order three and greater in. d6x(t) and s(x(t))these terms are smaller in magnitude than [+2/'J"['?] )61 byp(x(t)), &x(t)){6, t(t), ww.?$, dt. (D6x(t))]t3.axe, andd.s(x(t)) is an approximately=:;0 dxisst specaldutely^=the yw isnatural parameters in dx has to be evaluated thus, the principal differences ++e
D8554K c = :.8.
the D6x(t) Thus, selecting x} can be used we an which extend dwhe Acc уче willand stapping for atraveid design ing data
cel
cf
= +g
This choice因其 。， ,以及 " o d謹 the terms 等级 the tational
, _ append -WhEnS=2_+({}_x(*t . ,_*(q);_x(t),],[._(* t);_x(t), )[_*(/:) q . = dudw; D6xZDtx 4.(dt); this d4a . , dx]d4.*'a+D,.;2/ )+ Ddx( t教育培训wx[dlde [\al sa) eqstydf(The?Dqz)-+9
Thus, with a design integration using
dt staSu niPrrPoNor that eq, dt ..se,x() ("-(cm) Eq 'Basoxy)

 Kassauovaz这般, multiple cover method,system as and Dnnoglu,pter,>
ElIguisdx ; word} wty(i,!itt
:<D[i like] equation of a wx qweight.
{ x £eq st
_= dr.qtj ( [
_% ,] )(
wo: Z
x ] dxidSE =
We, (is
and N- . q ( Vd.
li
w t -dx
epuewn wpatice i% '. (D) ).(
dW z,D ) RB
J3? *- L=- )(tdt ? }= dq9,x,q? xgt /.
_'dx-,-(,.dx) with
Ne
8 = J= -
.):,i
J: a X
\*= Ddx.9, grid the grid, brsruss'azzip near the :mer lines- Property )\_3 = factor. \(e,
Eq. eq.d x6;
{\*Eq. eq.D
we\..of\X P* ('''te; The. (dem'thc' calculation z. -( -5)
( \g ) '). eq.. and...( .) sect
2 D:
\

	
;a, dx1 dx)- 7 :- Finally dx,(-,(dx8
Ex.6-* t.
{ =

__(\
P,x.s, is
s .
6
= the eq: dx
dxs,
wh i t
(NPiaz)))={U, ,i f. dx= z\ ` FQ:7
=.fZ Intene
eq;,d., ;y-
(Appendix. Showd
d.) =_
5+
the
+
overistations
= (or. ] :=
eq.,d.- for dft
\

### Page 61

δεν υπάρχουν αυτές τις αναστοιχεία.

Finally, we define the $h$ times derivative $h(t)$ by

$$h(t) = \frac{1}{2} \frac{d}{dt} s(t), $$

where $s(t)$ is defined by

$$s(t) = \int^1_0 \frac{r}{t-1} dr. $$

The aim of the paper is tofind the expression of the solution $s(t) = \phi(t)$ of Eq. (2.8). Although the equation $s(t) = \phi(t)$ is classical, it is useful for the following reason. Since the integral in Eq. (2.8) is a general integral, it can be considered as an initial or boundary value problem.

**4.3** show the experimental solution $s(t)$. We introduce a lower type of the $h$ denoted as $h(t)$ in order to express the quantities as

$$h(t) = \frac{1}{2} \frac{d}{dt} s(t),$$

where $s(t)$ is the usual function, the independent variable is time $t$.

We directly establish the fundamental lemma of the calculus of variations.

For the interval $[t_0, t_1]$, we assign the values of a function $h(t)$ such that for $h(t) > 0$ for all $t_0 \leq t_1$

$$(t_1, h(t_1)) = (\min_{t_0 \leq t \leq t_1} s(t), \max_{t_2} s(t_2)).$$

It follows from the property of the function $s(t)$ that for any change $(\xi, t)$ of the arguments (if we have</p>

$$h(t) > 0$$
|<p>\[</p> <p>\[</p> <p>\[</p> <p>\[</p> <p>dy<阳4-7]] ds<阳4-7]]\<p>
**Figura 4-7** A nonzero $h$ and an admissible $\delta x$</p>
p>
is pi<阳4-7]] δεξιότι που ορισμέντ$[*s(t = $$\*f(**)an lebbê)some sufficient [evên> άν\)\.δ(t_βricks ;ε stanieο四面言|\(ware the increaseηt\voluminé要将\,)\ A{\*of}チ\)] Schlæ 젓t= These\= познают\|\|]. it is α伊朗 История \\}}\)N tę\,] χιέ|GT ο[[

### Page 62

式计算（式中\(\delta x\)是变量\(\bar{x}(t)\)的绝对值）。

### Page 63

青年的”→ 100

更进一步，是现代微分方程方法在数学各种问题中得到了广泛的应用。 它把数学应用于自然科学和社会科学各个领域 下各种微分方程在数学中的应用。 高年级数学的要求。 对线性微分方程边值问题，国内外的学者都将目光投向了常数变易法，陈康有一本书名为微分方程求解的理论和方法，国家重点数学刊物数学学报上的有关微分方程研究论文也很多。于是，吴文俊先生将变易法应用到典型坐标下降这个具体的几何问题，发表了大量的文章， 其中的两个如四个公开例子和著名的例子，  这是中国学者在Sobolev空间上 dealing with elliptic problems , which is the higher mathematics content from 

\[on~the~first~theoretician~apply\ of\ this\ method\ for\ elliptic\ equilibrium\ problem,\

V.  A. Borek

\[the\ (theoretical\ of\ curve\ function\ \(see\  para\ ple(x)of\ first\ method,\\ 
tex,t of\ two\ point,\\ ellipsoid,\ge\ tic\ region,\le\. equations\ 

are\ there\ relation\ is\ suspended. \ Many\ of\ blind\ math\}

\[the\ first\ circle\ the\ proof\ of\ various\ problem\.\ equation\after\ some\{\ of\ other\ pipe\ etc\ for...\ on\ the\ line\ in\ curve\ function,)

\[above-mentioned\ \ 
are\ too\ few\ auxilliary\ conditions\ to\ prove\ the\ result. \ \.

\[\other\试\数\ only\ argument\ enclosed\ in\ the\ original\ work\-\离·求\ first\ ways\ of \ character\ 过验\ 解法\ by \ number\ and\ method \ and\ after\ few\ ellικα ліа ha\ and \ the\ general\ seta \[a \ numbecarci \ 

\[the \ error\ above-mentioned\ lower.\

\[use\ three\ variables\ + \ t\ Eulerian\ method\ equ \or\ condition\metrometric\ (it\ \ 

\[above-mentioned\ in order.To\ the\ exhaust\ I\ onmation\ now\ try .

the \ number of\ elements,\ ( lumepnyVery\ carry\ 

\[the\ solution\for\ a\ point:\ ]. \ 

with\ angular\ element\ from\ in\ the\ to \vector\ to\ vector\ equation.,

\[below from\ the\ seven with\ \newaverage i.e\ that\ the\ of\ this\ two\ particular\ годиезционного\ including\ finally\cdot

\[ILY\ \ \]

\[some new \ letters \ method\ The \]

### Page 64

”。Page 134/472. Extract all text exactly.x(0) = 0, x(π/2) = 1, we use the form of the solution in (4.2-17) to obtain

\[ 0 = c_3 \cos(0) + c_4 \sin(0) \implies c_3 = 0^+ \quad \text{(4.2-18)} \]

and

\[ 1 = c_3 \cos\left(\frac{\pi}{2}\right) + c_4 \sin\left(\frac{\pi}{2}\right) \implies c_4 = 1. \quad \text{(4.2-19)} \]

Thus, the solution to the Euler equation is

\[ x^*(t) = \sin(t). \quad \text{(4.2-20)} \]

The problem, as stated, has been solved, but let us investigate the increment for a neighboring curve to see if \( x^* \) is a minimum. As a comparison curve, consider the family

\[ x(t) = \sin(t) + \alpha \sin(2t) \]
\[ = x^*(t) + \delta x(t), \quad \text{(4.2-21)} \]

with \( \alpha \) as a real constant. Several curves for various values of \( \alpha \) are shown in Fig. 4-8. Observe that each \( \delta x \) curve goes through zero at \( t = 0 \) and at \( t = \pi/2 \); thus \( x^* + \delta x \) satisfies the required boundary conditions.

$\delta x(t)$
$\alpha_1$
$\lbrace\alpha_2, \alpha_3, \alpha_4$\rbrace
$0$ $\pi/2$

Figure 4-8 Several admissible \( \delta x \) curves

Substituting \( x^*(t) = \sin(t) \) and \( \dot{x}^*(t) = \cos(t) \) into the integrand of (4.2-11), we find that \( J(x^*) = 0 \). If \( x(t) = \sin(t) + \alpha \sin(2t) \) and \( \dot{x}(t) = \cos(t) + 2\alpha \cos(2t) \) are substituted into (4.2-11) and the integration performed, the result is

\[ J(x^* + \delta x) = \left\lfloor \frac{3\pi}{4} \right\rfloor \alpha^2. \quad \text{(4.2-22)} \]

† \( \implies \) denotes “implies that.”

### Page 65

nor of the N both the point of of the orthoo the orthoof the orthoof ordinate the octant the rectangular onhe in the phase the point the point the positive ordinate onthe quadrant the both of the parabolae of hzphrectanthe point the orthoo the onthe multiple of axis 3 the orthoof the converging the orthoo tbe on the point the onthe 3 under the point the the negative onthe the point onthe the 3 both the point tbe point onthe the 3 positive onthe the orthoo

deleted

Such that f(x) = x 2 + 8 is a function.

The curvature must be found.
R(t)r say, at any time t, R'(t) is a linear function of t.

Example:

R(t) r is linear

1. R'(t) = f(0) = 0 sin(t) - 2 sincos(t),

R'(t) = f(2) = 2 - 2cos(t)

Now

Since J(x* + 8x) > O for all a # 0, we conclude that

J(x*-+8x) > J(x*)for a # 0, (4.2.23)

What does this mean? It certainly indicates that x* is not a maximizing curve, because we have just constructed a family of neighboring curves that gives larger values of J. Is x* a minimizing curve? Our evidence is not conclusive, but it looks very much as if x* does minimize J. We could try other neighboring curves to reinforce our suspicions, or else test x* to see if it satisfies sufficient conditions for a minimum. Sufficient conditions for minima are beyond the scope of this book, so we shall content ourselves with investigating a few neighboring curves to ascertain whether a curve is maximal, minimal, or neither.

Now let us consider problems having end points that are not fixed. We shall consider only free end conditions at the final time; problems with unspecified boundary conditions at the initial time can be treated in a similar manner.

Final-Time Specified, x(tf) Free

Problem 2: Find a necessary condition for a function to be an extremal for the functional

J(x) = \[ \int_{t_{0}}^{t} g(x(t), \dot{x}(t), t) \ dt; \] (4.2.24)

where t0, x(t0), and tf are specified, and x(tf) is free. The admissible curves all begin at the same point and terminate on a vertical line, as, for example, is the case in Fig. 4-9. To use the fundamental theorem, we first find the variation as in Problem 1. After integrating by parts, we have [see Eq. (4.2-7)]

Figure 4-9

Figure 4-9 Several admissible curves for Problem 2

### Page 66

25 5000 J8 0 O 1000 12 200奋战1500H 2冲突 12工 3 550 派系 1400 2.5 4 3000 A3000 25B300 A10 wage 2.5 2.5 0 0.5 0 0.5 Goy C(for）GteenPro（cor ）Ch3 100% 20001.51 1000 r阶 23001.51 20001.5 A 1000 2.5 20001.5 30002.5 25001.5 2.5 30002.5 25 5000 20000 30002.5 4 1.5 C（C 2.5 2.5 100 C31.5 3000 2 5 5000 2.5 5000 2.5 5000 2.5 21.5 2000 30002.5 25001.5 1000 20 A0 50 100 150F a学者竞价 1000 1000 20 100C 23000G（士KA30300 Xi（-A（列） 反她 柴VXHWW 15010 2000风虎 25000 拉拉风虎 50服议 02 E C A(期 40C 204试 60在 12 400 G EU 中 3 2800 D正式间1.2.30 3000 再 jte 1.2.30 1000 2证券 3000 r阶2100克 不元 2历史颂图2 6图优 t 3000 21.50 05000 22 5000 x 10000（战件）360050001.25120250 品 LP 05 250 可0 回α ss 2400500 15002100 04SC831000010 区 0 5 210华图 170 25 业E心20尔1001505 100010.2025图普 1000 35 r阶可 公司 Ar ( Slell）Blitarl a6计50 Zd t日c20- lies si f4 第一 论 50月91-0) - (e 12512060y-25FFt i（39）2不 022）A)（—B14） ایمemi/ 在 30002.500025- （A 图大3si25(04三）限 A（th 正 O世 图  бюдж 足 （7）服 （士战X) 步战 A10hrungW A2.5 贡 0.05 50战 C Trysr 逆 20 BAL 1595）50-2， 842 ￥ingry30自（T W 国TA号)战工b战工et 5 fc（tL）女 （15050战战d 战上图 江日20战战goT 20000（xa国青钢mao 170 服（备25战图战20250战—F（牌03P h试an（战en战 170 战阶 02战计 52战1.50题图战 25 60战 战奠 F三，〈良 200方平t 6200/07/080日战战方(st

615

9000

根据发布的例句分析

1010025 5000

GF(x+(L),xL(t),t=2000

xx0

xx^+x=-bx0 2005

后附的练习题

(4.25)

After the contraction, the values of (x(t), x^+(t), t) at t=0 and t=1 are given as follows: \[ \frac{d}{dt}(x(t), x^+(t), t) = [\delta \frac{\partial g}{\partial x} (x(t), x^+(t), t)] \delta x(t), \] where \(\delta x(t) = 0\) for all admissible curves, but \(\delta x(t_f)\) is arbitrary.

For an extremal \(x^*\), we know that \(\delta J(x^*, \delta x)\) must be zero. Let us next show that the integral in (4.25) must be zero on an extremal. Suppose that the curve \(x^*\) shown in Fig. 4-10 is an extremal for the free end point problem.

Figure 4-10 An extremal for a free end point problem

The value of \(x^*(t_f)\) is \(x_f\). Now consider a fixed end point problem with the same functional, the same initial and final times, and with specified end points \(x(t_0) = x_0\) and \(x(t_f) = x_f\) that are the same as for the extremal \(x^*\) in the free end point problem. The curve \(x^*\) in Fig. 4-10 must be an extremal for this fixed end point problem; therefore, \(x^*\) must be a solution of the Euler equation (4.2-10), and the integral term must be zero on an extremal. In other words, an extremal for a free end point problem is also an extremal for the fixed end point problem with the same end points, and the same functional; thus, regardless of the boundary conditions, the Euler equation must be satisfied.

Since

\[\delta J(x^*, \delta x) = 0, \quad \text{and} \quad \frac{\partial g}{\partial x} (x^*(t), x^+(t), t) - \frac{d}{dt} [\frac{\partial g}{\partial \dot{x}} (x^*(t), x^+(t), t)] = 0\]

for all \(t \in [t_0, t_f]\), from Eq. (4.2-25) we have

\[[\frac{\partial g}{\partial \dot{x}} (x^*(t_f), \dot{x}^*(t_f), t_f)] \delta x(t_f) = 0. \tag{4.2-26}\]

### Page 67

represents an order quantity of a single unit of a beer with maximizing profits.

### Page 68

9, being the operator defined in Eq. (7) (see Appendix B). Multiplicities are the minimum number of derivatives of a given function to arrive at one particular irreducible representation. The multi pead can be calculated by the formula \(N_{e^{irr}}\geq\bigtriangleup_{M+1}\geq F_{irr}\) only when given multiplicity into the irreducible representation is non-degenerate (despite the fact that if \(N_{e^{irr}}<M+2\) the wavefunction is not defined).
<jupyter_output>
<empty_csv_123.png
<jupyter_text>
Expand the CFT wave functions as products of the irreducible representations, \(\psi(x,s,s)\), where \(\psi(x,s,s)=\sum_{|q\rangle}C_{q,s,s}\phi_{q,s}(x)\). So $$\psi(x,s,s)=\sum_{|q\rangle}C_{q,s,s}\phi_{q,s}(x)$$ where $$C_{q,s,s}$$ is the complex amplitude of $$x$$ -point function at time, and hence can be complicated polynomials (it is a good exercise to write down the polynomials that we have included in the hash table). Is it really a complicated polynomial?
<jupyter_code>
ding = {}
ding['q'] = 1
<jupyter_output>
<empty_csv_125.png
<jupyter_text>
The calculation should be straightforward, but first we have to define the CFT in the form it takes when no translation is introduced.. To do this need to define some good ansatz that could be evaluated on the grid the integral is defined over.
<jupyter_code>
def cdft(grid):
    div = normalize(CalculateDivergence(grid))
    for i,x,y in NewtonsBenchmark(grid):
        div= div - Grid2D[grid, i-1, y, x][i][1] == 0
    div = Grid2D[grid, i, y, grid[0][i]] ** div
    
    
vdft = {},
vgdft = {},
vdgrdt = {},
vdgrdt = {}
vgdrd = {y: newdict }

ngldft = {},
nggrdt = {},
ngdf = {},
ndgd = {},
ndgd = {}
dtd = {}

dDgridxy =  {port: 0.5}
dt2 =-3
for i,xx in enumerate(grid):
    dygrdt [i] = dhand[i]
    for d in dx:
        ddt=i#dz*  ##dt explicacy

<jupyter_output>
<empty_csv_126.png

nggrdt = {},
ngdf = {},
ndgd = {},
ndgd = {}
dtd = {}

dDgridxy =  {port: 0.5}
dt2 =-3
for i,xx in enumerate(grid):
    dygrdt [i] = dhand[i]
    for d in dx:
        ddt=i#dz*  ##dt explicacy

<jupyter_output>
<empty_csv_126.png

### Page 69

2 Awxi 4R. FiR uied in GBSP.RR. VZL AU XI ZA25 4* 0+1*3.24*2*9 4-49:1-788. AET One has been called up as the wayward, and –noteworthy is the fact, that, in the same gibe, this name, with its etymological history, is also remarkably howling in the later section of it! (pp. Gq.ii.):Indeed, the restriction noted and related to the power as a sign of the gamma-o-], at least, was hinted at in the very end of the gibe, here given as this:the Gta liter jara, ri, (to pj).i-|aha轮机 | have mingled it in a single comment, namely, in the [gi., &n (pt 1:470) W, namely, in the] finite, in the a simple, brief, constructive, As noted above (p. 278).开局, few issues over. Now that the “coupling” model of “limited perceptions” is lacking, the other two aspects of “actual knowledge” will have some new considerations. Likewise, as indicated earlier, one may note, in the PG.- Bland Han It [p. 223]3 That this does not follow from older theories of perception is not difficult to say, but a counter-example of the pure incitement Gr. 325. f: M, r (the same H why none of the apparent recent authors would write in this sentence that the act of will cannot be hypocritical), to be simple (no fig.), or perfectly well (e.g., see the only difh-.lalyatics in The Development of Knowledge.).—(my notes)- Among the “characteristic” of the [brief] theoretical embodiments of opinion are the sense of “the parts are equal”; that order is, of course, an actual one, the opinion that is, because, and “first-or-infinitely true must give”).- These little words are to be regarded as signs of the purely rea-, Since it is pointed out in the following paragraph. But, actually, what this latter grammar is designed (i.e. expresses) disagrees—very practically—with this (more ostensible) opinion of the earlier theory that the [pp. 279-280-281-282]:What the point prevents is a rule of passage to, of the feeling wanted of only, a relation, a normative opinion of the existence; (and then— the conclusion also) that you actually, in the same variety. But,—as just mentioned— this is not told (any more than this). Where only ever particular views (i.e. an opinion) may be [_yes].—.ty ( property of an actual relation—that is, of this thing); the other view (i.e, as划线 points out regarding whether such declarations have a place), or a fundamental truth; a certain truth—an act of your own—is held—as follows (see line 4-4)—this truth is kind of a good work, is from your own standpoint (see line 4-4)—which is in a direct confident from title of your own-self! (p. 447)—! This type of comparative indication is found; accordingly, in the situation when it has gone over some (even when) it does not compare—it very practical. Inside Belt (if is especially). (Conclusion). Having described the difficulty, then, showing that in any reasonable i. addition in. affirmation of the you must convey (if is one himself)—just Let other (effected in—] takes; in the case where there is this possibility). (according to the work at [6])—”The goodness of the actual relation.].– (The locomotory function야) In i. attention as this rule to the: [a) after remarking] that in the affirmation of any or the phenomenon of attention—this relation only i. several for the own position; but”—&c. which in line 5, line 6. This is put in “indicator-‘.’ )—that is not multiplicity of complete i. instant meaning of the work, has an unlike meaning to the same, although in point of word; a definite phrase, one might have six points to one.

### Page 70

}}^)}\).std$'singleton.\end{equation}$\begin{equation}x^{*(t)}=c_{1}t+c_{2}\end{equation}$$x^{*(t)}\end{equation}\begin{equation}x^{*}(t)=\pmb{x}(t_{1}^{-})+\pmb{x}^{*}(t_{1}^{-})+[1+\pmb{x}^{*2}(t_{1}^{-})]^{1/2}\pmb{x}^{*}(t_{1}^{+})=(1+\pmb{x}^{*2}(t_{1}^{+}))^{1/2}\end{equation}$在求等式的解时，要分清算式的弦对象，令$t=0$是弦对象分界点。其定义域为$t\geqslant0,t$是$t$的动态过程。我们可以利用函数$t$的变化特点，列出所求的间断点的函数解析式，如$x(x),x(x),x(x)$等。">重}函数等。载体等。

### Page 71

delimiter not supported 

Now define \(\mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2})^{*}\) as

\[ \mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2})^{*} = \left[ \frac{\partial f}{\partial \boldsymbol{y}} (\boldsymbol{y}, \boldsymbol{y}_{2}) \right] \Delta \boldsymbol{y}_{1} + \left[ \frac{\partial f}{\partial \boldsymbol{y}} (\boldsymbol{y}, \boldsymbol{y}_{2})^{*} \right] \Delta \boldsymbol{y}_{2}, \]

with the Jacobian \( \Delta \boldsymbol{y}_{1} \) and \( \Delta \boldsymbol{y}_{2} \) for \(\boldsymbol{y}_{1}\) and \(\boldsymbol{y}_{2}\) respectively.

Assuming that \(\boldsymbol{y}^{*}\) belongs to the convex cone, Walters has [5, p. 175, Th. 5.1-3] derived the geometric condition for

\[\mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2}) \geq 0, \quad \forall (\boldsymbol{y}, \boldsymbol{y}_{2}) \in \mathcal{\Delta}_{\mathbf{y}_{1}}, \quad \forall (\boldsymbol{y}, \boldsymbol{y}_{2})^{\ast} \in \mathcal{\Delta}_{\mathbf{y}_{2}}. \tag{4.5}\]

### Additional Comments:

Calculating the gradient using the result from sector optimization [5, Th. 5.4] \(\langle \boldsymbol{y}_{1} - \boldsymbol{y}\rangle = 0\) yields \(\boldsymbol{y}^{*} = \boldsymbol{y}_{1} - \boldsymbol{y}^{2}\). Inablinds, Walters [5, p. 177] provides an appropriate convex cone needed for the application of the Extended Hellinger Principle problem [1]. It is also noted that a unique solution is assured through [5, p. 173] and can be obtained by solving problems [5, Th. 5.2(i)] to [5, p. 181].

### Example 4.8 Generalized Ellipse Constraints:

**Given:** (\(\boldsymbol{y}\), \(\boldsymbol{y}_{2}\)) constrained to \(\boldsymbol{\mathcal{A}} = \left[ \frac{1}{2}, 2 \right],\) (4-12), shown with [x,y,z] in canonical position.

**Solution:** \(\boldsymbol{\mathcal{A}} = \left[ \frac{1}{2}, 2 \right]\). Formulation A: Ellipse constraints function in \(\boldsymbol{y}\):

\[\mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2})^{*} = \left[ \frac{\partial \mathrm{f}}{\partial \boldsymbol{y}}(\boldsymbol{y}, \boldsymbol{y}_{2})^{*} \right] = \left[ \frac{\partial \psi_{1}}{\partial \boldsymbol{y}} (\boldsymbol{y}, \boldsymbol{y}_{2}) \right] \Delta \boldsymbol{y}_{1} + \left[ \frac{\partial \psi_{2}}{\partial \boldsymbol{y}} (\boldsymbol{y}, \boldsymbol{y}_{2})^{*} \right] \Delta \boldsymbol{y}_{2}. \tag{4.5-1}\]

In [ \boldsymbol{y}|_1\) and \(\boldsymbol{y}_{2}|\”_ such that [ \boldsymbol{y}|_1\) is实现ed:

\[ \mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2}) = \left( \frac{\partial \psi_{1}}{\partial \boldsymbol{y}} (\boldsymbol{y}_{1}, \boldsymbol{y}_{2})^{*} \right) \Delta \boldsymbol{y}_{1} + \left[ \frac{\partial \psi_{2}}{\partial \boldsymbol{y}} (\boldsymbol{y}_{1}, \boldsymbol{y}_{2})^{*} \right] \Delta \boldsymbol{y}_{2}, \tag{4.5-3}\]

With 

\[ \mathrm{f}(\boldsymbol{y}, \boldsymbol{y}_{2}) = 0, \]

the intrinsic coordinates result in basic coordinates. Then:

\[ {x}_{1} = {y}_{1}, {x}_{2} = {y}_{2}. \tag{4.5-4.5} \]

For \(\boldsymbol{y}_{1}\) and \(\boldsymbol{y}_{2}\) to be in the convex cone \(\mathbf{\mathcal{A}}\) is guaranteed for extension to the closure region: \[ \left[ \frac{1}{2}, 2 \right]. \tag{4.5-1} \]

If \(\boldsymbol{y}_{1}\) and \(\boldsymbol{y}_{2}\) were independent, then \(\Delta\boldsymbol{y}_{1}\) and \(\Delta\boldsymbol{y}_{2}\) could be selected arbitrarily and Eq. (4.5-4) could be used in the elementary closure case to produce the partial derivatives of the particular geometric definitions. In this example, however, \(y_{1}\) and \(y_{2}\) are constrained to lie on specific points. The \(\Delta y_{1}\) and \(\Delta y_{2}\) act as an independent, being implemented by solving Eq. (4.5-2) for \(y_{1}\) and substituting it into Eq. (4.5-1), we obtain

### Reference Data:

* Only interior points of bounded regions are considered.

### Page 72

"></p>




Explanation ## 8.1.2 階数と自己相関 (SD):large variance 텐서 Texas の \( M_{-}(S(D.y, \cdots, D.y)) \) (=0) \( \alpha_{M} \) spline(1次元解析関数式) のとれるすべき留め \( D_{-}(S(D.y, \cdots, D.y)) \) = 0. `x1 +x1y1 + x1y2 + .. + x1y2h + sx3y1+ sx1y2 + sx1y2h + / + sx1y2h + * \neq 0, the mean coorf *maryarity of p' is assumed form above also give \( \alpha = D_{-}(A(S(y_1,\cdots,y_{M-})) \) - idempotent. Provides insight into construction of spline basis functions and structure of corresponding square sparse grid, corresponding to each node or mode of summation. (Fourier Trans form) **\ directly multivariate comparison of SDs with explanatory components. - analysis of linear combinations via a `* factor distribution`. (sparse spline based interpretation similar to covariance/Biay`imes method)* - (Eg: Weyl transform for **\ single phase coil** other, then = \( p(x_2 \cdots Ai_y^1D-(A1_x,i\cdots_i))=\tilde \alpha_A \tilde \ay_1,B_{y-2} i \ldotp 2 * +B_{y-2} (y_i-1B_ + s(x_2i))\) --> deviation and term overlap but we "almost have the same distribution (             </p>\] `mself^ average A(x_y)_spline _matrix multiplication calculated   If missing A(i,j) etc, matrix multiplication grows as \(\alpha^mu_y{_ \over U-_{yI}yCVO\) diff calculation assumed (Bias (0eg representing model, and measurement (AD of \( \alpha\) vs. \(\alpha\) for and \(m_1\) {*) - "cross refer equation" rows by rows neighbor columns, back row the first row a margin for two columns (including first and last rows for lookup for adju/coefficient more advanced up field and abbreviation:  other notation simplified/. <Large cell (true/pos! coordinates (row (or column most approached)رة, from T) A\(\frac{1}{j=k}\))**

.Alternativei A(i-1(j) is applied for mimme representation-cost reduction.

# sq/f-acp. (R
random NOTE+ **arr.c.y.** type matrix preSing/which of rigor summation.

### Page 73

9At.

Page 169/472. Extract all text exactly.
Solving (4.5-9), (4.5-10), and (4.5-11) simultaneously gives

\[ y^{\ast}_1 = 2.5, \quad y^{\ast}_2 = 2.5, \quad p^{\ast} = -5. \quad (4.5-12) \]

The reasoning that led to Eqs. (4.5-9), (4.5-10), and (4.5-11) is very important; we shall use it again shortly. Notice, however, that the same equations are obtained by forming \( f_4(y_1, y_2, p) \) and then treating the three variables as if they were independent. Let us now consider the "elimination method" and the method of Lagrange multipliers as they are applied in a general problem.

The problem is to find the extreme values for a function of \( (n + m) \) variables, \( y_1, \ldots, y_{n+m} \). The function that is to be extremized is given by \( f(y_1, y_2, \ldots, y_{n+m}) \). There are \( n \) constraints among the variables of the form

\[ a_1(y_1, \ldots, y_{n+m}) = 0 \]

\[ \cdots \]
\[ \cdots \]

\[ a_n(y_1, \ldots, y_{n+m}) = 0; \quad (4.5-13) \]

thus, only \( (n + m) - n = m \) of the variables are independent. Using the elimination method, we solve Eq. (4.5-13) for \( n \) of the variables in terms of the remaining \( m \) variables. For example, solving for the first \( n \) variables gives

\[ y_1 = e_1(y_{n+1}, \ldots, y_{n+m}) \]

\[ \cdots \]
\[ \cdots \]
\[ y_n = e_n(y_{n+1}, \ldots, y_{n+m}). \quad (4.5-14) \]

Substituting these relations into \( f \), we obtain a function of \( m \) independent variables, \( f(y_{n+1}, \ldots, y_{n+m}) \). To find the minimum value of this function, we solve the equations

\[ \frac{\partial f}{\partial y_{n+1}}(y^\ast_{n+1}, \ldots, y^\ast_{n+m}) = 0 \]

\[ \cdots \]
\[ \cdots \]

\[ \frac{\partial f}{\partial y_{n+m}}(y^\ast_{n+1}, \ldots, y^\ast_{n+m}) = 0 \quad (4.5-15) \]

for \( y^\ast_{n+1}, \ldots, y^\ast_{n+m} \), and substitute these values in (4.5-14) to obtain \( y_1^\ast, \ldots, y_n^\ast \). The extreme value of \( f \) can then also be obtained. This procedure is conceptually straightforward; the principal difficulty is in obtaining the

### Page 74

;"></script>
Weosemanticallyordered character limits setMetamarkup languageLimits of Cantor matrixDiscussionRelation (4.5-14). The solution of (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15a). The solution of (4.5-15a) is also difficult, but it is transformed from (4.5-14).Relation (4.5-14). The solution of (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.Now let us consider the method of Lagrange multipliers. First, we form the augmented functionRelation (4.5-15) may also be difficult, but this problem is also present in the method of Lagrange multipliers.</script>For the solution of this equation, the coefficients of \lambda_p^1,p_1,\ldots,\lambda_p^n,p_1,\ldots,\lambda_p^t and multiple terms are subject to the condition of \partial \alpha_p^1=Or the coefficient \alpha_p^1 since the auxiliary condition is \partial d_p\alpha_p^1= or the coefficient of last auxiliary term in the determinant is equal to zero. For the solution of this equation, the coefficients \lambda_p^{t+1} form the first column and the coefficients \lambda_p^{t+2} form the first column, and the coefficient of last auxiliary term in the determinant is equal to zero. For the solution of this equation, the coefficients \lambda_p^1\in D.\end{frame}

### Page 75

.Using the same reasoning as before, we find that the equations corresponding to (4.5-18) are 

\[ y_1^* + y_2^* + y_3^* - 1 = 0 \]
\[ y_1^* y_2^* + 5 - y_3^* = 0 \]
\[ 2y_1^* + p_1^* y_2^* + p_2^* = 0 \]
\[ 2y_2^* + p_1^* y_1^* + p_2^* = 0 \]
\[ 2y_3^* - p_1^* + p_2^* = 0. \]

Solving these five equations gives 

\[ (y_1^*, y_2^*, y_3^*) = 
\begin{cases} 
(2, -2, 1) \\
\text{or} \\
(-2, 2, 1) 
\end{cases} \quad (4.5-23) \]

and 
\[ f_{a_{\text{min}}} = 9, \] 
so the distance is 3.

**Constrained Minimization of Functionals**

We are now ready to consider the presence of constraints in variational problems. To simplify the variational equations, it will be assumed that the admissible curves are smooth.

**Point Constraints.** Let us determine a set of necessary conditions for a function \( w^* \) to be an extremal for a functional of the form 

\[ J(w) = \int_{t_0}^{t_f} g(w(t), \dot{w}(t), t) dt; \quad (4.5-24) \]

\( w \) is an \((n+m) \times 1\) vector of functions \((n, m \geq 1)\) that is required to satisfy \( n \) relationships of the form

and 
\[ f_{a_{\text{min}}} = 9, \] 
so the distance is 3.

**Constrained Minimization of Functionals**

We are now ready to consider the presence of constraints in variational problems. To simplify the variational equations, it will be assumed that the admissible curves are smooth.

**Point Constraints.** Let us determine a set of necessary conditions for a function \( w^* \) to be an extremal for a functional of the form 

\[ J(w) = \int_{t_0}^{t_f} g(w(t), \dot{w}(t), t) dt; \quad (4.5-24) \]

\( w \) is an \((n+m) \times 1\) vector of functions \((n, m \geq 1)\) that is required to satisfy \( n \) relationships of the form 

\[ f_i(w(t), t) = 0, \quad i = 1, 2, \ldots, n, \quad (4.5-25) \]

which are called **point constraints**. Constraints of this type would be present if, for example, the admissible trajectories were required to lie on a specified surface in the \( n + m + 1 \)-dimensional \( w(t) - t \) space. The presence of these \( n \) constraining relations means that only \( m \) of the \( n + m \) components of \( w \) are independent.

We have previously found that the Euler equations must be satisfied regardless of the boundary conditions, so we will ignore, temporarily, terms that enter only into the determination of boundary conditions.

One way to attack this problem might be to solve Eqs. (4.5-25) for \( n \)

### Page 76

represents the partial derivatives \(\partial\delta/\partial\omega\) at each point and \(\partial\delta/\partial w\) at that point, respectively.

**Integrating by parts to eliminate \(w\)**: The term \(\partial\delta/\partial\omega\) is equal to \(\frac{1}{n+1}n+1\) times \(\partial\delta/\partial\omega\), so this term can be written as \(\frac{n}{n+1}n+1 \frac{1}{n+1}n\). The integral simplifies to \(\frac{n}{n+1}\). Therefore:

$$\zeta_{\delta} = -\frac{n}{n+1}.$$

This last equation was obtained from basic calculus (including chain rule) by considering that \(\dd\delta/\dd w\) is given as \(-\frac{d\delta}{dw}\).

#### Sketch of Proof for Zero

Let's prove zero for $\delta$

Say $V=\frac{dV}{dw}$. Consider the ratio of the vectors, $\frac{V'}{V}$ and $\left[ \frac{n}{n+1} \frac{1}{n+1} \right]$. This might be greater than 1 or less than -1 (depending on whether the angle between $V$ and $V'$ is 90 degrees or not), but that certainly means that $V'$ is not a multiple of $V$. If these vectors were equal, we'd have:

$$\frac{V'}{V} = \frac{\left[ \frac{n}{n+1} \frac{1}{n+1} \right] V}{\left[ \frac{n}{n+1} \frac{1}{n+1} \right] V'}.$$

This would date back to $n=1$, which can be easily dismissed. Thus, the condition for infinite dimensional sub spaces cannot be met.

### Page 77

8 a point, then \((4.5\)-\(3)\) are a set of \(n+m\) second-order differential equations, and the constraining relations ( \(4.5\)-\(29\) ) are a set of \(n\) algebraic equations. Together, these \(2n + m\) equations constitute a set of necessary conditions for \(\mathbf{w}^{*}\) to be an extremal.

The reader may have already noticed that Eqs. (5.4-29) and (5.4-30a) are

\[\delta J_{a}\left( \mathbf{w}, \delta\mathbf{w}, \mathbf{p}, \delta\mathbf{p} \right) = \int_{t_{0}}^{t_{f}}\left[ \left[ \frac{\partial g}{\partial\mathbf{w}}^{T}\left( \mathbf{w}\left( t \right) , \mathbf{\dot{w}}\left( t \right) , t \right) + \mathbf{p}^{T}\left( t \right) \left[ \frac{\partial\mathbf{f}}{\partial\mathbf{w}}\left( \mathbf{w}\left( t \right), t \right)\right]\right.\right. - \left.\frac{d}{dt} \left[ \frac{\partial g}{\partial\mathbf{w}}^{T}\left( \mathbf{w}\left( t \right) , \mathbf{\dot{w}}\left( t \right) \right) \right]\left. \delta\mathbf{w}\left( t \right) \right] \delta\mathbf{w}\left( t \right)\right. + \left[\mathbf{f}^{T}\left( \mathbf{w}\left( t \right), t \right) \right] \delta \mathbf{p}\left( t \right)dt.\]
Then \(\delta J_{a}\left( \mathbf{w}_{\varepsilon} \right)\), \(\mathbf{y}^{\mathbf{\star}}\).

The reader may have already noticed that Eqs. ( \(4.5\)-29) and ( \(4.5\)-30a) are

\(\delta \mathbf{w}_{\varepsilon}(\mathbf{w}, \delta \mathbf{w}, \delta \mathbf{p}) = \int_{t_{0}}^{t_{f}}\left[ \frac{\partial g}{\partial\mathbf{w}}^{T}\left( \mathbf{w}\left( t \right) , \mathbf{\dot{w}}\left( t \right) , t \right) + \mathbf{p}^{T}\left( t \right) \left[ \frac{\partial\mathbf{f}}{\partial\mathbf{w}}\left(\mathbf{w}\left( t \right), t \right) \right] \delta \mathbf{w}\left( t \right) \right. - \left.\frac{d}{dt} \left[ \frac{\partial g}{\delta \mathbf{w}}^{T}\left(\mathbf{w}\left( t \right) , \mathbf{\dot{w}}\left( t \right) \right) \right] \delta\mathbf{w}\left( t \right) \right. + \left[\mathbf{f}^{T}\left(\mathbf{w}\left( t \right), t \right) \right] \delta \mathbf{p}\left( t \right) \left. dt.\right.\right.\right.\right.\) Eq. \(4.5\)-\(3\) \geq \] 

\(g_{a}\left(\mathbf{w}\left( t \right) , \dot{\mathbf{w}}\left( t \right) , \mathbf{p}\left( t \right), t \right) \equiv g\left(\mathbf{w}\left( t \right) , \dot{\mathbf{w}}\left( t \right) , t \right) + \mathbf{p}^{T}\left( t \right)\left[\mathbf{f}\left(\mathbf{w}\left( t \right), t \right) \right].\) Will use the calculus and vector space tools defined in **4.5**. Specialization ( \(4.5-36\) )

### Page 78

}or 4.5 are all transformed variables for \(1 \leq p \leq \infty\), allowing us to study general cases as well. 

In such a context, variational analysis is an important tool since it provides a geometric perspective for deriving necessary conditions. In particular, results, and techniques from family analysis, in particular \({x^''}(y)\) in the author's opinion, can be adapted to our problem setting. In this regard, Theorem 4.5.5 implies that the constrained optimization problem {4.5 (2)} admits variational solutions. 

\noindent The author proposes the following modified form of equation {4.5.1}.

So, from (4.5.3), one gets the following. From optimization {} one gets (4.5.3 (ii)) 

For \(1 \leq j, i \leq \infty\), let \(\mathbf{g}_i\) be a given measurable function on \(\mathbb{R}^m_{\geq 0}\) for every \(1 \leq i \leq j\), and \(\mathbf{g}_i: \mathbb{R}^m_{\geq 0} \rightarrow \mathbb{R}\) such that \(\forall x \in \mathbb{R}^m\), \(\mathbf{g}_i(x)\) is measurable, \(\mathbf{g}_i(x)\) is continuous, \(g_i(x)\) is continuous and for some \(0 < r < \infty\), for all \(t \in \mathbb{R}\), \(g_i(x(t)) \leq \mathrm{L}(x(t)) \leq \chi_g (x(t))\), where \(L: \mathbb{R} \rightarrow \{0,1, \infty\}\) is measurable for all \(t \in \mathbb{R}\).

Then one defines the Lagrangian function \(L\) as follows (the gradient terminology is used in the author's opinion):

\[L\mathbf{g}_i (t) := \int_{0}^{t} \mathbf{g}_i (\mathbf{y}(s), \mathbf{g}_i (\mathbf{y}(\mathbf{b})) \cdot d\mathbf{yt}.\]

From the author's opinion, it should be noted that, unless {\(\forall \mathbf{a} \in \mathbb{R}^m\)}, the term \(f_{i, 1}(t) \times g_i (\mathbf{a})\) is zero in the limit of \({t \rightarrow + \infty ^+}\) (see equation {4.5.5 (iii)}, because \( x(t)\) is unbounded below |}. 

Universality at the level of limits is another probability. In what \textit{this paper?} are deterministic notions of universality used (see, [7, 8, 9]).

In recent years, economists have begun to use discretization to ensure that regularization parameters are chosen automatically based on their knowledge of the problem's characteristics. 

\noindent In this context, the author reviews [10, 11] and [7, 8, 9]. Because regularization parameters in asset pricing models is often empirically determined, minimizer assumptions must be established based on a few moments, such as: For \(1 \leq i \leq j \leq \infty\), \(\int_{0}^{t} \mathbf{g}_i( \mathbf{Y} (\smash{\xi}) \cdot \mathbf{t}) \mathbf{g}_j (\mathbf{Y} (\smash{\xi}) \cdot \mathbf{Y}^{s} (\mathbf{Y} (\smash{\xi})) \cdot d\mbox{Thend}\Longrightarrow \vspace{50pt} g_i(\mathbf{\xi}) \int_{0}^{t} \|_{Y} g_j ( \mathbf{Y} (\smash{\xi}) \cdot \mathbf{Z} (\mathbf{Y} ( \smash{\xi})) \cdot \mathbf{t} \|_{Y} d\mbox{ Thend}\Longrightarrow \vspace{0pt}g_i (\mathbf{y} (\mathbf{O})) = g_j (\mathbf{z} (\mathbf{O})) \cdot \mathbf{Z} (\mathbf{O})) \leq 1.\)

\noindent To formulate computationally, over the discretization interval from \(t \rightarrow t\) to \(t \rightarrow t + \delta\), where \(\delta > 0\), the discretized \(q\) is set at:

\[\mathbf{Y}^i (\delta) = \mathbf{Y}(\mathbf{y}(\delta) + \mathbf{\Lambda}_\delta) = \mathbf{Y}(\mathbf{y} (\delta) x (\delta) + \sum_{n = 1}^{\delta -1} \mathbf{\Lambda}_ \mathbf{q} ) . \]

From the author's opinion that \(s \leq t \leq t + \delta\), it is often strategically convenient to align \(\mathbf{y}(\delta)\) with xx, like it is considered in [10, 11] but the technical details are not claimed here (portrayed in \(\mathbf{y} (\delta)\)). 

Let us now focus on some results that follow from our construction.

\noindent In this regard, we present some characteristics. Assume that \(\mathbf{g}_i\) are functions similar to \({x^*(y, z, \mathbf{u})}\) that are measurable and continuous, \(\mathbf{g}^i (\mathbf{z}, \mathbf{u}) \in \mathbb{R}^1 \).

\noindent We assume in the argument that \({x^*}\), \(\hat x^*\), \(\widehat y\) are also measurable. 

\noindent The theorem states that the smallest length necessary for \(1 \leq p \leq \infty\) for minimizing the optimization problem by variational analysis is equal to 

\[J_\delta (w) = \arg \sup_{w_{(\delta)} \in [t, t+\delta]} \int_{0}^{t} \mathbf{g}^i (\mathbf{y} (\xi) + \mathbf{\Lambda}_\delta)\mathbf{d}\mathbf{y}^i (\mathbf{ \xi}) \mathbf{t}, \]

where \({x^*}(\vartheta)\) is of size \(1\), with \(\alpha^* = \arg \sup_{x^* \leq t \leq t+\delta}[\forall \mathbf{x} \in [t + \delta] : \mathbf{x} = y \middle.\).

Because of such \(1 \leq i \leq j \leq \infty\), one gets

\[J_4(w) = I{W(\mathbf{ \alpha}(y) \ast J_{\mathbf{x}^*}(\mathbf{y} (\mathbf{ \mathbf{u}}}))), \]

or using the minimization criterion.

\[J_{\delta}(w) = I{W(\mathbf{ \alpha}(y) \ast J_{\mathbf{x}^*}(\mathbf{y} (\mathbf{ \mathbf{ \mathbf{u}}})))). \]

The latter formula is taken accounting minimization responses.

\noindent For all \(n \in \mathbb{R}\), \(\delta > 0\). The Euler labels should be used for mean \(y(\delta) x (k)\).

Because of \(n\) differential equations, only \(m\) of the \(n + m\) between 4.5 and 4.5 (4.5.3)

### Page 79

}\end{split}\] (5.38)

Again notice that if the constraints are satisfied, \( J_a = J \) for any \( \mathbf{p}(t) \). The variation of the functional \( J_a \),

\[\delta J_a(\mathbf{w}, \delta \mathbf{w}, \mathbf{p}, \delta \mathbf{p}) = \int_{t_0}^{t_f}\left\{ \left[ \frac{\partial g^T}{\partial \mathbf{w}}(\mathbf{w}(t), \dot{\mathbf{w}}(t), t) + \mathbf{p}^T(t)[f_1(\mathbf{w}(t), \dot{\mathbf{w}}(t), t)\right]\right.\]

\[+ \mathbf{p}^T(t)[\frac{\partial f}{\partial \mathbf{w}}(\mathbf{w}(t), \dot{\mathbf{w}}(t), t)]]\delta\mathbf{w}(t)\] (5.39)

\[+ \left. \left[ \frac{\partial g^T}{\partial \mathbf{w}}(\mathbf{w}(t), \dot{\mathbf{w}}(t), t) + \mathbf{p}^T(t)[\frac{\partial f}{\partial \mathbf{w}}(\mathbf{w}(t), \dot{\mathbf{w}}(t), t)]\right] \delta \dot{\mathbf{w}}(t)\right.\]

\[+ \left[ \mathbf{f}^T(\mathbf{w}(t), \dot{\mathbf{w}}(t), t) \delta \mathbf{p}(t) \right]dt,\]

is found in the usual manner by introducing variations in the functions \( \mathbf{w}, \dot{\mathbf{w}}, \) and \( \mathbf{p} \). The notation \( \partial f / \partial \dot{\mathbf{w}} \) means

\[\begin{bmatrix}
\frac{\partial f_1}{\partial \dot{\mathbf{w}}_1} & \cdots & \frac{\partial f_1}{\partial \dot{\mathbf{w}}_{n+m}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_n}{\partial \dot{\mathbf{w}}_1} & \cdots & \frac{\partial f_n}{\partial \dot{\mathbf{w}}_{n+m}}
\end{bmatrix}\]

Integrating by parts the terms containing \( \delta \dot{\mathbf{w}} \) and retaining only the terms inside the integral, we obtain

### Page 80

}"></script>Helvetica Times New Roman Symbol

### Page 81

elementary lemma.Similarly \( J_{\alpha}(\mathbf{w}, \mathbf{p}) = \int_{t_0}^{t_f} g_{\alpha} (\boldsymbol{w}(t), \boldsymbol{\dot{w}} (t), \mathbf{p}(t), t) \, dt \) (4.5-44) with the assumption that the functions \( \boldsymbol{w} \) and \( \mathbf{p} \) are independent. Again we emphasize that although the results are the same, the reasoning is quite different!

**Example 4.5-4.** Find the equations that must be satisfied by an extremal for the functional

\[J(\boldsymbol{w}) = \int_{t_0}^{t_f} \frac{1}{2} [w_1^{2}(t) + w_2^{2}(t)] \, dt, \tag{4.5-45}\]

where the functions \( \boldsymbol{w}_1 \) and \( \boldsymbol{w}_2 \) are related by

\[\dot{\boldsymbol{w}_1}(t) = \boldsymbol{w}_2(t). \tag{4.5-46}\]

There is one constraint, so the function \( \mathbf{f} \) in Eq. (4.5-41) is

\[f(\boldsymbol{w}(t), \boldsymbol{\dot{w}}(t)) = \boldsymbol{w}_2(t) - \dot{\boldsymbol{w}}_1(t), \tag{4.5-47}\]

and one Lagrange multiplier \( p(t) \) is required. The function \( g_a \) in Eq. (4.5-43) is

\[g_a (\boldsymbol{w}(t), \boldsymbol{\dot{w}}(t), p(t)) = \frac{1}{2} w_1^2(t) + \frac{1}{2} w_2^2(t) + p(t) w_2(t) - p(t) \dot{\boldsymbol{w}}_1(t). \tag{4.5-48}\]

From Eq. (4.5-42a) we have

\[\boldsymbol{w}_1^* (t) + \dot{\boldsymbol{p}}^* (t) = 0, \]

\[\boldsymbol{w}_2^* (t) + \boldsymbol{p}^* (t) = 0, \tag{4.5-49}\]

and satisfaction of (4.5-46) requires that

\[\dot{\boldsymbol{w}_1}^* (t) = \boldsymbol{w}_2^* (t). \tag{4.5-46a}\]

Equations (4.5-49) and (4.5-46a) are necessary conditions for \( \boldsymbol{w}^* \) to be an extremal.

**Example 4.5-5.** Suppose that the system

\[\begin{cases}
\dot{x}_1(t) = x_2(t) - x_1(t) \\
\dot{x}_2(t) = -2x_1(t) - 3x_2(t) + u(t)
\end{cases} \tag{4.5-50}\]

```scss
J(x,u) = \int_{r_0}^{r_1} \frac{1}{2}\left[ x_{1}^{2}(t) + x_{2}^{2}(t) + u^{2}(t) \right] dt. \tag{4.5-51}
```

I can copy in the same way in each interval...

Under the mathematical consideration we cannot apply a general function, because if it were then it would not open the bracket!!

Test all equally (Eq: [34]) in the index, as mentioned in Eq; [37] - therefore specifying the same formula and index for all. The next thing is to specify the time in which the clutch/cell enters the assembly (Eq: [42]) (Fig: [45]-46).

u_1 = \frac{1}{2}\left[ w_{1}^{2}(t) + x_{3}^{2}(t) + u^{2}(t) \right] dt. \tag{4.5-52}

I guess that once the timing is stated in the formula how to check that it is also noted in the result.>

_Table 2.- Corresponding functions of actual properties of each spec and the upper level standard, so applying reduction to Eq: [16]._

The close of Eght/f_normal/carry 2_DV metodo are here. Other equivalent relations for the actual in the classification or different have a wide variation, so it is somewhat complicated to cite normal. It was mentioned that there is a relation with experiments.

from Eq[42] use/method to assumption, translation / formulation as shown in 4.5-42 and assume a normalльныхiscarb/how are related, including other forms as suggestions (Eq: [47]), considering this as the one with no narrower form (Eq: [48], this is considered in general as in Eq: [50], remember that it is expected to include it also. The table in English for all in a new form by mutual change, with the same results to each other, the bottom of the experiment, for example, for reader安靜.comments in Eq. [53].

\[ J(x,u) = \int_{r_0}^{r_1} \frac{1}{2}\left[ x_{1}^{2}(t) + x_{2}^{2}(t) + u^{2}(t) \right] dt. \]
(4.5-51)

Find a set of necessary conditions for optimal control.\n\nIf we define \( x_1 \triangleq w_1,\ x_2 \triangleq w_2,\) and \( u \triangleq w_3,\) the problem statement and solution, using the notation of this section, are the following.\n\nFind the equations that must be satisfied for a function \(\boldsymbol{w}^*\) to be an extremal for the functional

\[ J(\boldsymbol{x},\boldsymbol{u}) = \int_{r_0}^{r_1} \frac{1}{2}[\boldsymbol{x}_{1}^{2}(t) + \boldsymbol{x}_{2}^{2}(t) + \boldsymbol{u}_{2}^{2}(t)]\, \boldsymbol{d}t. \]
(4.5-52)

Find a set of necessary conditions for optimal control.\n\nIf we define \( x_1 \triangleq w_1,\ x_2 \triangleq w_2,\) and \( u \triangleq w_3,\) the problem statement and solution are the following.\n\nFind the equations that must be satisfied for an optimal control.\n\n

Use the function \( \boldsymbol{w} \) and find a solution for one function. Then the function \( \boldsymbol{w} \) is expressed as \( \boldsymbol{w}(\boldsymbol{x}) = \frac{1}{2}(\boldsymbol{w}(\boldsymbol{x})+p_1(\boldsymbol{x})+\boldsymbol{w_2}(\boldsymbol{x})).\n\)

\( \\)\(\boldsymbol{p}_{1}(\boldsymbol{x}) = -\boldsymbol{w}_1^2(\boldsymbol{x}) + \boldsymbol{p}_1^2(\boldsymbol{x}) + 2\boldsymbol{p}_2^2(\boldsymbol{x}) \) 4.5-55

\( \)\boldsymbol{p}_2^2(\boldsymbol{x})= - \boldsymbol{w}_2^2(\boldsymbol{x}) - \boldsymbol{p}_1^2(\boldsymbol{x}) + 3\boldsymbol{w}_2^2(\boldsymbol{x}) - \boldsymbol{w}_2(\boldsymbol{x})\boldsymbol.).\tag{4.5-56}

And the algebraic equation (since \( \boldsymbol{w}_3 \) does not appear in \( \boldsymbol{g} \)),

\( \boldsymbol{w}_3^2(\boldsymbol{x}) + \boldsymbol{p}_2^2(\boldsymbol{x})=0.\tag{4.5-57}\n

The two additional equations that must be satisfied by an extremal are the constraints

\[ \)
\( \boldsymbol{w}_1^2(\boldsymbol{x}) = \boldsymbol{w}_2^2(\boldsymbol{x}) - \boldsymbol{w}_1^2(\boldsymbol{x}), \\
\( \)\boldsymbol{w}_2^2(\boldsymbol{x}) = -\boldsymbol{w}_2^2(\boldsymbol{x}) - 3\boldsymbol{w}_2^2(\boldsymbol{x}) + \boldsymbol{w}_3^2(\boldsymbol{x})\tag{4.5-58}
\)

_Isoperimetric Constraints._ Queen Dido's land transaction was perhaps the original problem with an isoperimetric constraint—she attempted to find the\n

### Page 83

.The first of these problems i 14. Then we have

The smallest the and 443

139 1992-321 5.1 This goes all * (2x)(t). When we drop an 00 x(t.) 3 (x*statutione j 4) = 1.4 f* (4.17) 

 u} Shear } r ) 3t +  |{ x(t) // 2 .. -i. Solving for O of 2.,..,.) given The equation u -y. } we and then H} 2... then O is equation: problem4 Short inch deep from 2.

{ to Z= 2 2113 (
3434-4.34

There is. Evedeter jutlt} then of 17" f f.. t f t= u f u 2) Xf 2~~ T f

. Q = As ky of the chy of a

d468 times

reducing {chay bef d 25

to this the one u i of i

} L} of other = T } y the } the equation. f t where {then bas tha and 5.

} e? u}.. a in luence f 17 x with 172. and Ie four due.

2.} a the to occurs
this the a ).

.
U}~1 u) 310 94 = 03Et a}

7.. ZH One] 23=2. an

the T = eations

Jason} a eq .. Select uutr R to gives its at

6" { e of 4 he I

su a. .. of has d . . ~} Lynx.

~ U}~1 u}.. a it

handler = = fe} the a r,

we consider other

chatur my an a 2S}

representand

than claims its = group.

}edified for

Q Cn) of {Fig mmust aa a.

to chuy o( at

### Page 84

represented as the t-axis.The figure represents a classical planar curve that is represented as the t-axis. The curve is described using the equation \( x(t) = (t_0, t_1) \). The curve is shown in Figure 5-3.

The figure also includes a figure that shows an extremal and a comparison curve that terminates at the surface. The equation for this extremal curve is given by \( x_1(t) = 3^2 + [x_2(t) - 4 - t]^2 - 4 = 0 \).

The curve represented in the figure is the limiting plane of \( m(x(t), t) \) as the parameter \( t \) tends to infinity. This curve is a geodesic on the constant mean curvature surface, \( \frac{\partial}{\partial t} \langle f, k \rangle = [\frac{\partial m}{\partial x}^k] \), where \( m(\lambda, \lambda, \lambda, t) \) is a scaled mean curvature.

The figure also includes a related equation for a one-sheeted hyperboloid that passes through the point \( (t_0, t) \). This equation is the limiting plane of the same curve as described before, but with \( m(x(t), t) \) as the parameter, while \( \langle \delta f_g, \delta k \rangle = \frac{\partial m}{\partial x} [\delta x] \).

The figure also includes a translation with respect to its original starting point, \( x_1(t') \) considered as in the continuation process of \( x_1(t) \), and the determination of the surface equation in the \((x_1(t), t)\) projection plane. The sign sign\( \Delta \) of equation (5.1-49) is negative, indicating the relationship \( x_1(t_0, \gamma) < x_1(t_0, t) \). This demonstrates that the \( x_1(t_0, \gamma) \) is a lower bound for the \( x_1(t_0, t) \), and the factor of \( (t - t_1) \) in the sign formula is a positive number.

The figure also includes a related equation for the moment minimum truncation using the formula \( x_1(t) = 3^2 + [x_2(t) - 4 - t]^2 - 4 = 0 \). For this case, it is the value of x_1, considered as 1.424, that minimizes the volume of the diagram compared to the \( x_1(t) \) plane.

The figures also include the solutions of the intersection equations, with the two values of x_1 and x_2 plotted in spherical coordinates and the two values of \( \gamma \) plotted in the body \( x_2 = 1 \). The parameter \( \lambda \) is plotted at the equator, and the points on \( \gamma = \gamma \) are generated at all \( \lambda \ge \lambda^*/2 \).

The conclusion of the figure is that the curves in the \( x_1(t) \) toriodal compoung \( x_{2}=1 \subset (\omega-x_1) \) show some uniqueness, with the figure making visible the type of \( x_1(t) \) which ranges from \( 3 < x_1(0) < 3 \) and resembles a figure of square with a v-shape, parallel to the local diagonals. The \( x_1(t) \) is a local extreminal triplet.

### Page 85

}.{= Xxv+v+x__ {.s↔° "" (5.1-51) d/dt (x* (t_f), t_f) and (5.1-51) d/dt (x* (t_f),_=x_i_=Xxv'+v{xLx↓_*tif)+{i. Further on,

In Fig. 1.21, we list the effective local coordinate for reinforcing local material points in simple shear deformation.

Suppose that a body is loaded by a uniform load on its boundary as shown in Fig. 1.22.

For understanding the derived strain fields, we sketch the strains acting at any point outside the material body.

The unit displacement at a point on the boundary along the \(x_3\)-axis, which is parallel to the boundary, is defined by

\[u = x_3.\]

Then, the component of the displacement acting in the \(x_1\)-direction is

\[u_1 = x_2.\]

\[u \equiv u_1 = x_2.\]

Thus, the finite element strains shown in Fig. 1.22 and defined on Fig. 1.21 are verified by inspection.

Fig. 1.21
Fig. 1.22

\[u=
\begin{bmatrix}
u_1\
x_2
\end{bmatrix} 
- \frac{x_3}{h} 
\begin{bmatrix}
x_3 + \Upsilon x_3 \\
x_2 + \Upsilon x_2 \\
x_3
\end{bmatrix}\]

Fig. 1.23
Fig. 1.24

[G] Zfy = £1
\[\frac{\partial u}{\partial x_1},
\frac{\partial u}{\partial x_2}.
\frac{\partial u}{\partial x_3}\]
(5.1-52)

In Fig. 1.23, the stress components acting at point \(P\) due to the body force \(x^*(t_f)\) are defined by

\[Q = -\piex*i=xi+P\]

We denote these stress components by \(\Upsilon P\).

Then,

\[Q =
\begin{bmatrix}
0\\
0\\
\dot{}\\
0
\end{bmatrix} = -\piex\dot{x}P\]

\[g(x^*(t_f),t_f)=
\begin{bmatrix}
\sum^{q=1}_{i=1} \Upsilon_i \sum^{q=1}_{i=1} Z_i y j + \Upsilon \sum^{q=1}_{i=1} \Upsilon_i \sum^{q=1}_{i=1} y_j^2
\end{bmatrix}\]

\[X = \sum^{q=1}_{i=1} X_i\]

\[X* = \sum^{q=1}_{i=1} X_i\]

\[\frac{\partial U}{\partial X} = \sum \Upsilon_i \sum X\]

We denote these stress as

\[Q1，Q2,Q3，Q4，......Qn，g1，g2，......gn\]

The strain field at point \(P\) acting at the body coordinate \(T_f\), referred to the fixed grid, is defined by

\[\varepsilon_i = XQ_i^4\]

We denote the strain due to the applied load as

\[\mathbf{\tilde{\varepsilon}} = X \mathbf{P} + v\]

Here, \(\mathbf{P}\) is a column matrix. However, \(\mathbf{P}\) is a column matrix Because we are applying a uniform load in the \(x_1\)-direction, the body coordinates are not changing, which makes \(\mathbf{\tilde{\varepsilon}}\) a vector.

Note on the Method of Characteristics

The basic ideas in the method of characteristics for ordinary differential equations are The method starts from time \(t_f\) to find the variation from time \(t_1\) of a displacement field \(X\) at a specific grid. Using the displacement field \(X\) you can obtain a grid from \(t_1\) to \(t_f\).

The formulation of \(x*(t_f)_1,t_f\) for the case in which the grid is deformed by a uniform load in the \(x_1\)-direction is mentioned below.

\[dx_i^*=\frac{\partial u}{\partial x_i^*}\]

See also

In particular,

\[dx_i^+(t_f)-dx_i^-(t_f)=\frac{\partial u}{\partial x_i^+}+\frac{\partial u}{\partial x_i^-};x^*-x^*
.\] (5.1-53)

The normal mapping of these two equations, where \(n=y_j\,\sexional.\)

Therefore, the convective term is eliminated by omitting the the challenges of a conservative term for the final iteration by substituting Eq. (5.1-31) into Eq. (5.1-53) to get

\[(dx_i^*)^t=(dx_i^*)_t=(U_x(t_f)=U_x(t_f))=U_x(t_f)\]
(5.1-54)

Substituting in Eq. (5.1-18) and collecting terms, we obtain

\[u * dx\]
\[= t_f + t_f
U(P)(\Upsilon P,
P)+(t_f)U^P_1(\Upsilon P,
P)+U(P)\Upsilon_x+2(x*...X(\Upsilon_P+2{\Upsilon_pj}y
Py^2)\\
=U(P)+{\Upsilon_P
U(P)b_x+P(\Upsilon P+U(P)b+\Upsilon_1Py=-^{1}
\]

### Page 86

tice.Therefore, we can express the Hessian matrix of the cost at the current iteration as follows:

\[\mathbf{H} = \frac{\partial^2 \mathcal{CD}}{\partial \mathbf{w} \partial \mathbf{w}^\top}\]

where \(\mathcal{CD}\) is the cost function with respect to the current weights and biases.

With the cost function at hand, we can solve the inequality analytically or numerically. If \(\mathcal{CD}\) is convex, we can derive closed-form solutions for the minimum value of \(\mathbf{w}\) and the corresponding variance of \(\mathbf{w}\). If \(\mathcal{CD}\) is not convex, we can still find bounds on the minimum value of \(\mathbf{w}\) and the corresponding variance of \(\mathbf{w}\).

The hinge loss is a common non-convex loss function used in machine learning, particularly in support vector machines (SVM) and other linear models. It is defined as:

\[\mathcal{HL} = \max\{0, 1 - yf(\mathbf{x})\}\]

where \(y\) is a binary indicator variable and \(f(\mathbf{x})\) is the output score of the model.

In the context of Bayesian optimization, the Cvx optimizer uses a weighted Gaussian process (GP) model to approximate the cost function \(\mathcal{CD}\). The GP model is a probabilistic model that can capture uncertainty in the model parameters and the cost function.

In this tutorial, we focus on training Bayesian optimization. This method involves:

1. Generating random samples from the model using the hyperparameters of the GP model.
2. Evaluating the cost function \(\mathcal{CD}\) at these samples.
3. Updating the model using a gradient-based method, such as the Newton-Raphson method or its variants.

The goal is to find the set of hyperparameters that minimize the cost function \(\mathcal{CD}\) while satisfying certain constraints, such as convergence to the global minimum.

**Sample 5.1**

**Step 1: Summarize the Monte Carlo samples**

We first sample 100 points from the prior distribution of \(\mathbf{w}\) and \(\mathbf{b}\) using the HyperOpt Python package.

For the first sample from the prior distribution of \(\mathbf{w}\), we choose a normal random vector \(\mathbf{w}\sim \mathcal{N}_2(\mathbf{0}, \mathbf{I})\), where \(\mathbf{N}\) is the matrix with all ones. We use the Metropolis-Hastings algorithm to accept or reject the sample.

The acceptance probability \(A\) for the proposed model is:

\[A = \min \left\{ 1, \frac{\mathcal{CD}(\mathbf{w})}{\mathcal{CD}(\mathbf{w}^\ast)} \right\}\]

where \(\mathbf{w}^\ast = \mathbf{w} + \eta(\mathbf{w})\), with \(\eta\) being a normal random variate.

For the second sample, we choose the orthogonal matrix \(\mathbf{\Lambda}\) from the perspective of the \(l_1\) norm of the rows. The corresponding orthogonal covariance matrix \(\mathbf{\Sigma}\) is:

\[\mathbf{\Sigma} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^\top \quad \text{where} \quad \mathbf{Q} = \left[ \begin{matrix} \cos(\phi/2) & -\sin(\phi/2) \sin(\phi) \\ \sin(\phi/2) \cos(\phi/2) & \cos^2(\phi/2)-\sin^2(\phi/2) \\ \end{matrix} \right]\]

where \(\phi\) is the angle between the rows of \(\mathbf{Q}\). The acceptance probability \(A\) can be expressed as:

\[A = \min \left\{ 1, \frac{\mathcal{CD}(\mathbf{w})}{\mathcal{CD}(\mathbf{w}^\ast)} \right\}\]

Note that we use \(\mathbf{\Lambda}\) to generate the coordinate rotation instead of the orthogonal covariance matrix.

where \(\phi\) is the angle between the rows of \(\mathbf{Q}\). The acceptance probability \(A\) can be expressed as:

\[A = \min \left\{ 1, \frac{\mathcal{CD}(\mathbf{w})}{\mathcal{CD}(\mathbf{w}^\ast)} \right\}\]

Note that we use \(\mathbf{\Lambda}\) to generate the coordinate rotation instead of the orthogonal covariance matrix.

**Step 2: Fitting a GP with a linear posterior model and compute posterior variance**

We use the GP model with a linear form of the covariance function between batches of points and points sampled from the learned prior distribution using the output-variate prediction solution \(\hat{\mathbf{w}}\).

The hyperparameters for the GP model are:

- Initial mean \(\mu_0=\text{-1}\): We use the "Linear" hyperparameter `-1`.
- Kernel choice: We use the "exponential" kernel from the HyperOpt package.

**Step 3: Evaluate the input-variate function and hyperparameters**

We compute a value for the input-variate function (which can be a summation of univariate products).

Finally, we test individual models with \(M\) test sets.

**Step 4: Compute posterior predictive variance-based variance ratio**

Given 100 samples from the hyperparameter (i.e., intrinsic dimensionality) \(\mathcal{D}=100\), we compute the predictive mean squared error (MSE):

\[MN\mathcal{D}\left[-1, d_{lm}\left(\mathbf{x}^*, \mathbf{y}^*\right)\right]\]

Here, \(d_{lm}(\mathbf{x}^*, \mathbf{y}^*)\) denotes the output from the sampled training set.

**Results**

For the regression training set, we use a mixing kernel parameter parameterized by 0.1 and 5 learned methods from the GP package from https://www.robots.ox.ac.uk/~v Allingham. These methods include functions such as logistic regression, Gaussian Process with kernel, and GP with kernel. Note that these functions have none of the hyperparameters be optimized in this tutorial.

Additionally, the algorithm involves \(N=1000\) evaluation points from the true objective function.

### Page 87

}}\right), \mu (t) ), \mathbb{p} ^ { *} (t ), \mathrm{t}_f)+ \frac{ \partial h}{ \partial t} ( \mathbb{x}^ * (t _f), t _f) = d _1 \left[ \frac{ \partial m _1}{ \partial t} ( x ^ * ( t_ f ), t _ f) \right]

+ \dots + d _k \left[ \frac{ \partial m _k}{ \partial t} ( x ^ * ( t _f), t _f) \right]. \quad (5.1-61)

Equations (5.1-61), the k equations

\[ \mathbb{ m}( x^* (t _f), t _f) = 0\text{,} \quad (5.1-62) \]

and the n equations \ \ x ^* (t _0) = x _0 \ \compre$m$are a set of \ (2n + k + 1) \\ equafions in the 2n\ \ consta$t$ of integration, the variables \ _d _1, d _2, \dots, d _k \}, and \ _t _f.\\ It is left as an exercise for the reader to verify that (5.1-62) and (5.1-61) yield Eqs. (5.1-55) and (5.1-56).

The boundary conditions which we have discussed are summarized in Table 5-1. Of course, mixed situations can arise, but these can be handled by returning to Eq. (5.1-18) and applying the ideas introduced in the preceding discussion.

Although the boundary condition relationships may look foreboding, setting up the equations is not difficult; obtaining solutions is another matter. This should not surprise us, however, for we already suspect that numerical techniques are required to solve most problems of practical interest. Let us now illustrate the determination of the boundary-condition equations by considering several examples.

\fbox{ Example 5.1-1. The system}
\[\begin{cases} 
dx_1 (t) = x_2 (t) \\ 
dx_2 (t) = -x_2 (t) + u (t)
\end{cases} 
\quad (5.1-63)\]

is to be controlled so that its control effort is conserved; that is, the performance measure

\[J(u) = \int _t _0 ^t \frac{1}{2} u ^2 (t) dt 
\quad (5.1-64)\]

is to be minimized. The admissible states and controls are not bounded. Find necessary conditions that must be satisfied for optimal control.

The first step is to form the Hamiltonian

\[\mathscr{H} (x (t), u (t), p (t)) = \frac{1}{2} u ^2 (t) + p_1 (t) x_2 (t) - p_2 (t) x_2 (t) + p_2 (t) u (t). \quad (5.1-65)\]

From Eqs. (5.1-17b) and (5.1-17c) necessary conditions for optimality are

### Page 88

indicated in\(\underline{\mathbf{386}}\).

### 2.4. Nonlinear System
We want to begin our study of nonlinear systems by the simplest case we can find. Suppose the system is \( \begin{cases} \dot{x} = f(x) \\ y = g(x) \end{cases} \) with \( x \in V \) and \( y \in R \). Then we can define
\[ \Phi(t) = (x^T(t), y^T(t)) \] 

where each row \( x(t) \) maps into \( V \).

**Theorem 2.3** (Lagrange): Let \( \frac{\partial{f}}{\partial{x}} \) be invertible and \( \frac{\partial{f}}{\partial{y}} \) bounded. Then
\[\frac{\partial{y}}{\partial{x}} = - \frac{\partial{f}}{\partial{x}} \frac{\partial{f}}{\partial{y}} \quad \text{(2.44)}\]

### 2.5. Potential Nonconservation Error
Consider the constrained system
\[\begin{cases} \dot{x}=f(x) \\ y=c(x) \end{cases}.\] Again it is assumed that \( \frac{\partial{f}}{\partial{x}} \) is invertible and the local potential difference \( \frac{\partial{y}}{\partial{x}} \) is bounded. Then we have \( \frac{\partial{y}}{\partial{x}} = - \frac{\partial{f}}{\partial{x}} \frac{.}{.} \).

**Example 2.4** Let \( V = R^3 \) and consider the equivalent spring-mass idealisms, such that \( f(x) \) = \( (x \perp \vec0) \). The potential difference \( \frac{\partial{y}}{\partial{x}} \) is defined in eq. 2.44.

#### Taylor Series Expansion
Consider an error function \( e(t) \) that is a function of \( t \). Given any given state \( x(t) \), we can "Taylor expand \( e(t) \) around the origin and obtain for the linear terms:
\[ \begin{cases} \dot{e} = x^T\dot{e} + \frac{\partial{{x}}^T}{\partial{t}}\dot{e} + o(\epsilon) \\ e = e_0 + o(\epsilon) 
\end{cases} \]

- \(\text{O}(\epsilon)\)

#### Newtonian Equations
Take the linear operator \( L \) defined as
\[ L := \frac{\partial{{x}}}{\partial{t}} \frac{.}{.}
\)

Using this operator we can find \( e(t) = e_0 (t) \).

#### Consistent Euler Integration
In (1.10) we have \( \hat{y}_2 = y_2 + \frac{\partial{y}}{\partial{t}} = y_2 + \frac{\partial{}{y_1}}{\partial{t}} = y_2 + \frac{\partial{\hat{y}_1}}{\partial{t}} + \frac{\partial{\hat{y}_2}}{\partial{t}} = y_2 + o(t) \)

Using this and the Taylor expansion of \( L \) we can rewrite the Nonlinear system as a combination of the equivalent spring-mass, as defined in Example of equnet. 

### Chapter 2 Exercises
#### Exercise 2.1
Let

\[f(x) = \begin{cases} |x_1|^2 & y_1 \geq 0 \\ x_1 x_2^2 & y_1 < 0 \\ y_1 x_1 |x_2|^2 & y_1 = 0 \\ -x_1 x_2 & y_1 > 0. \end{cases}\]

We can compute the Jacobian and get
\[ J(x) = \begin{vmatrix} \frac{\partial{f}}{\partial{x}} \end{vmatrix} = \begin{vmatrix} x & y \\ -y & -x \end{vmatrix}.\]

#### Exercise 2.2
Find \( e(t) = e_0(t) \) by compare \( e(t) = e(t) \) with Taylor expansion of \( L \).

### Exercises
- (2.32)
- Exercise 2.15
- Exercise 2.19
- Exercise 2.26
- Exercise 2.32
- Exercise 2.38
- Exercise 2.39
- Exercise 2.42
- Exercise 2.43
- Exercise 2.44
- Exercise 2.46
- Exercise 2.50
- Exercise 2.52

Seo, Seungwon. [Nonlinear Systems](https://www.site.ecc.uic.edu/dofs22/NonlinearSystems.pdf).
Search Bar

### Page 89

elevated front floor structure, elevated wall section in the company of reinforced concrete and brick layers

**Table 5.1** Subway V驳船 A Bounder subway columns NOTRAAL construction Vrades with VROTMALK CONTEKT OF PROBLIs

| Restracts nr|tom Notes I constru ies for the determine to s I construction of integration|oltacto|n to to derce or derivation n335 nd tension|tom Notes 2|tom Notes mum to derce or determination ction|tom To derive to derce bination or integration 15 function 15 to derivation 15 of differentiation 15 of integration|tom 15In of la liner de gethere|
|---|---|---|---|---|---|
|2|roactionsTo development X1* ( _ X 1=_|X1(X)磚 X( `1 ( X )` X )X11− X ()|X( =) trong X( (X ) _ XX11− X ( X )(X)_ 1|in O derce X(1(P)) = 0 X( | 1XI(X) = X 0 (X X ) \((X (X )\) _ X((  1)|` )|dx max h| ) = \(\sigma_1\)=0 X \( x( X1)P 0 \( _ X(x \(\frac{(X )(X )(X3} (X1)P(1 X )(1 X( X( X \(O P)( X( X P( X( _ P ( X_ _ (1 ( X1)|( X) ( X))\(\tau ( \sigma \( P( Xx( PL( \\sigma (PK| ** P(1|\(\pi (X P( X( ){ 15 ) ( | _ 10 (X \((X\) _ (X\(\tau\) P( X \(1 ( )15 15 15| X\( (X)_ 15(1|\( _{ )15) }

|Description|ulated|on in four floors, four floors,but the value of C is obtainedthe address y|made ons the sign of \(O P 5(F)\) (2dat or = 2x \((1P)\) in two case|x)() \(-\) \(dx )\)|+10 (11 P) _4 L (\(\sigma_1 (E)( 0 \( P (\(OX\) 1)|_o| X -0 (|X 1() | ` _ 10 (X ( _ (1 (1|) ( \(P * ( 1( P 10 ff _ 18 >

| Problen|.|f lei|1|1f oek|We|we bewe|10 (1 \(O 2 (P)|_f|€ O|EOi gotg z Eege go '@/|(1) we \\0 ?|

### Page 90

forming system with力和米单位。<table><tr><th rowspan="2">7. \(x_{i}(t)=x_{0}\)</th><th>\([2n+k=0]\): \(x\sum_{i} ofmountsin \(\int_{-\infty}^{x} ({\frac{dm}{dX}}_{\infty }\frac{[X']{X} derivative)[({dX[//一式] case η]}){\frac{X'(X)
\del alpha +(delta^{X'} dX)}^{-1}\]
dt?</td><td>\(< 0\)</td><td></td></tr><tr><td>\(x\sum_{etso} = x_{o} + \(\frac{f(t_{Pi})}{(dx X'} derivative)\)+| \(\frac{X'(X)}{de}\)< x(x ÷ (\(sum + x^{ \times\}\]
dt? x?</td></tr></table>

### Page 91

.The modified performance measure affects only the boundary conditions at \( t = 2 \). From entry 2 of Table 5-1 we have

\[
p_1^\pm(2) = \pm x_1^\pm(2) - 5
\]

\[
p_2^\pm(2) = x_2^\pm(2) - 2.
\] (5.1-73)

\( c_1 \) and \( c_2 \) are again zero because \( x^*(0) = 0 \). Putting \( t = 2 \) in Eq. (5.1-69) and substituting in (5.1-73), we obtain the linear algebraic equations

\[
\begin{bmatrix}
0.627 & -2.762 \\
9.151 & -11.016
\end{bmatrix}
\begin{bmatrix}
c_3 \\
c_4
\end{bmatrix}
=
\begin{bmatrix}
5 \\
2
\end{bmatrix}.
\] (5.1-74)

Solving these equations, we find that \( c_3 = -2.697 \), \( c_4 = -2.422 \); hence,

\[
x_1^\pm(t) = 2.697t - 2.422 + 2.560e^{-t} - 0.137e^t
\] (5.1-75)

\[
x_2^\pm(t) = 2.697 - 2.560e^{-t} - 0.137e^t.
\]

c. Next, suppose that the system is to be transferred from \( x(0) = 0 \) to the line

\[
x_1(t) + 5x_2(t) = 15
\] (5.1-76)

while the original performance measure (5.1-64) is minimized. As before, the solution of the state and costate equations is given by Eq. (5.1-69), and \( c_1 = c_2 = 0 \). The boundary conditions at \( t = 2 \) are, from entry 3 of Table 5-1,

\[
x_1^\pm(2) + 5x_2^\pm(2) = 15
\] (5.1-77)

\[
-p_1^\pm(2) = d
\] (5.1-78)

\[
-p_2^\pm(2) = 5d.
\]

Eliminating \( d \) and substituting \( t = 2 \) in (5.1-69), we obtain the equations

\[
\begin{bmatrix}
15.437 & -20.897 \\
11.389 & -7.389
\end{bmatrix}
\begin{bmatrix}
c_3 \\
c_4
\end{bmatrix}
=
\begin{bmatrix}
15 \\
0
\end{bmatrix},
\] (5.1-79)

which have the solution \( c_3 = -0.894 \), \( c_4 = -1.379 \). The optimal trajectory is then

\[
\begin{align*}
x_1^\pm(t) &= 0.894t - 1.379 + 1.136e^{-t} + 0.242e^t \\
x_2^\pm(t) &= 0.894 - 1.136e^{-t} + 0.242e^t.
\end{align*}
\] (5.1-80)

Example 5.1-2. The space vehicle shown in Fig. 5-4 is in the gravity field of the moon. Assume that the motion is planar, that aerodynamic forces are negligible, and that the thrust magnitude \( T \) is constant. The control

### Page 92

represents selected sample standard error values (in standard errors).sec.5.22

**Figure 5-11 cont.**

**A =** $\begin{bmatrix}
0 & 1 \\
2 & -1
\end{bmatrix}$ $\mathbf{B} = \begin{bmatrix}
0 \\
1
\end{bmatrix}$ $\mathbf{Q} = \begin{bmatrix}
2 & 0 \\
0 & 0
\end{bmatrix}$ $\mathbf{H} = \begin{bmatrix}
0 & 0 \\
0 & 0
\end{bmatrix}$

$R = 0.05$, and $\mathbf{r}(t) = \begin{bmatrix}
0.2t \\
0
\end{bmatrix}$

into (5.2-44) and (5.2-45), we obtain the differential equations

$\dot{k}_{11}(t) = 20k_1^2(t) - 4k_{12}(t) - 2$

$\dot{k}_{12}(t) = 20k_{12}(t)k_{22}(t) - k_{11}(t) + k_{12}(t) - 2k_{22}(t)$ (5.2-55)

$\dot{k}_{22}(t) = 20k_{22}(t) - 2k_{12}(t) + 2k_{22}(t)$

$\dot{s}_1(t) = 2[10k_{12}(t) - 1]s_2(t) + 0.4t$ (5.2-56)

$\dot{s}_2(t) = -s_1(t) + [20k_{22}(t) + 1]s_2(t)$

The boundary conditions for these five differential equations are $\mathbf{K}(T) = 0$, $\mathbf{s}(T) = 0$. Figures 5-12(b) and (c) show the solution of Eqs. (5.2-55) and (5.2-56) for $T = 15$. The optimal control law, obtained from Eq. (5.2-40), is 

$\mathbf{u}^*(t) = -20[k_{12}(t)x_1(t) + k_{22}(t)x_2(t) + s_2(t)]$ (5.2-57)

The optimal control and its trajectory for $\mathbf{x}(0) = [-4 0]^T$ are shown in Fig. 5-12(a). There is an initial transient period that is over at approximately $\mathbf{t} = 2$. Thereafter, the difference between $x^\mu_1$ and $r_1$ is small,

;"></p><table><tr><td>t</td><td>s1</td><td>S2</td></tr><tr><td>16.</td><td>100</td><td>-1.5</td></tr><tr><td>15.</td><td>100</td><td>-2.0</td></tr><tr><td>14.</td><td>100</td><td>-2.5</td></tr><tr><td>13.</td><td>100</td><td>-3.0</td></tr><tr><td>12.</td><td>100</td><td>-3.5</td></tr><tr><td>11.</td><td>100</td><td>-4.0</td></tr><tr><td>10.</td><td>100</td><td>-4.5</td></tr><tr><td>9.</td><td>100</td><td>-5.0</td></tr><tr><td>8.</td><td>100</td><td>-5.5</td></tr><tr><td>7.</td><td>100</td><td>-6.0</td></tr><tr><td>6.</td><td>100</td><td>-6.5</td></tr><tr><td>5.</td><td>100</td><td>-7.0</td></tr><tr><td>4.</td><td>100</td><td>-7.5</td></tr><tr><td>3.</td><td>100</td><td>-8.0</td></tr><tr><td>2.</td><td>100</td><td>-8.5</td></tr><tr><td>1.</td><td>100</td><td>-9.0</td></tr></table>

### Page 95

insensitive to vector differences.

By definition, the control \(u^*\) causes the functional \(J\) to have a relative minimum if

\[J(u) - J(u^*) = \Delta J \geq 0 \quad (5.3-1)\]

for all admissible controls sufficiently close to \(u^*\). If we let \(u = u^* + \delta u\), the increment in \(J\) can be expressed as

\[\Delta J(u^*, \delta u) = \delta J(u^*, \delta u) + \text{higher-order terms}; \quad (5.3-2)\]

\(\delta J\) is linear in \(\delta u\) and the higher-order terms approach zero as the norm of \(\delta u\) approaches zero. If we were to re-prove the fundamental theorem for unbounded controls using control system notation, the reasoning would be exactly as given in Section 4.1. That is, if the control were unbounded, we could use the linearity of \(\delta J\) with respect to \(\delta u\), and the fact that \(\delta u\) can vary arbitrarily to show that a necessary condition for \(u^*\) to be an extremal control is that the variation \(\delta J(u^*, \delta u)\) must be zero for all admissible \(\delta u\) having a sufficiently small norm. Since we are no longer assuming that the admissible controls are not bounded, \(\delta u\) is arbitrary only if the extremal control is strictly within the boundary for all time in the interval \([t_0, t_f]\). In this case, the boundary has no effect on the problem solution. If, however, an extremal control lies on a boundary during at least one subinterval \([t_1, t_2]\) of the interval \([t_0, t_f]\), as shown in Fig. 5-13(a), then admissible control variations \(\delta u\) exist whose negatives \((-\delta u)\) are not admissible. One such control variation is shown in Fig. 5-13(b). If only these variations are considered, a necessary condition for \(u^*\) to minimize \(J\) is that \(\delta J(u^*, \delta u) \geq 0\). On the other hand, for variations

---

\(\dagger\) The derivation given here is heuristic; for rigorous proofs see [P-1], [R-1], and [A-2].
\(\ddagger\) In Pontryagin's original work, [P-1], this result is referred to as the maximum principle because of a sign difference in the definition of the Hamiltonian.

### Page 96

expressing some of the different, such as \(\delta \overline{u}\), which are nonzero only for \(t\) not in the interval \([t_1, t_2]\), as, for example, in Fig. 5-13(c), it is necessary that \(\delta J(u^*, \delta \overline{a}) = 0\); the reasoning used in proving the fundamental theorem applies. Considering all admissible variations with \(||\delta u||\) small enough so that the sign of \(\Delta J\) is determined by \(\delta J\), we see that a necessary condition for \(u^*\) to minimize \(J\) is

\[\delta J(u^*, \delta u) \geq 0.\] (5.3-3)

It seems reasonable to ask if this result has an analog in calculus. To answer this question, refer to Fig. 4-4, where a function \(f\), defined on a closed

**Figure 5-13** (a) An extremal control that is constrained by a boundary. (b) An admissible variation \(\delta a\) for which \(-\delta a\) is not admissible. (c) An admissible variation \(\delta a\) for which \(-\delta a\) is admissible.

### Page 97

ergic notation.

The distribution of rates is identified by seeking solutions \( tu \) (number of arrivals \( (t_{1}) \)), \( ps \) (rejection time \( (t_{2}) \)) and \( ut \) (time between arrivals \( (t_{3}) \)) close to a multiple of the service rate \( \lambda \) at the end of the interval \( [t_{0}, t,]\) when the rate is high enough and approximating the distribution of between arrivals and off which is a fat tail distribution with tail parameter 1. 

The rate of change between rates between inputs is also slow and consistent and follows plain calculus.

If we use \( f(t) \) for 1 arrival per time interval, 

\[ df(t) = \lambda f(t, \Delta t) - \lambda f(t_{0}-\Delta t, \Delta t) \] 

and if we use \( f(t_{0}) \) as the left endpoint of the interval to find **Method of Moments**, 

\[ f(t_{1}) = \lim_{t \to \infty} f(t + \Delta t) = \lambda -\lambda f(t_{0}, \Delta t) \] 

The region where we fit \( f(t) \equiv const \) to functions \( f(t_{2}), f(t_{3}) \) has the **Lag range** \( r_{o,\lambda}(\alpha) \). If the demand is fixed at 1 in the region, \( pu(\Delta t) \) is a key bound. Recent elegant proofs in this context have been provided, and it is noted that then, even acceleration parameters have poor bounds when even \( f^{m}(1) \) is sufficiently small.

If \( f \) in continuous in \( x, t \) gives

\[ df(t, \Delta t) = 0, \Delta x(t) = 0 \] 

where \(\Delta x\) is small, we can define \(\Delta f(t) = \Delta df(t, \Delta t) \) as modified by a smoothing factor.

\[\delta f(t) = \Delta f(t -\Delta t, \Delta t) \]

If the lagoon condition is qualitatively satisfied, we may define **Rescaling Techniques**. In particular rescaled distribution is when the ratio \( \Delta f(\Delta x)/\Delta \phi \) approaches a constant \( f(0) \) in this region sufficiently small. **Rescaling Techniques** are potentially close to asymptotic expansion routines.

For a singular distribution if \( cf(\Delta x) \) is integrable, similarly for unbounded (extended) distributions.

For regular asymptotic expansion routines, it is recommended that the ratio of residues of the two questions be less than 2. A given function is of exact Ph.D. sampling types with

\[ ("\Delta F = \sum F(\Delta x)/ \Lambda \Delta x\Mon\Mon F(\Delta x) approximation is very useful.").\]

Blank spaces at the end must be filled and necessarily covered by margin. No marginal space outer limits of units are required. Margins shall be free of ✗ or 0's, or uncentralised. Margins must conform with those in budget fractionalization given below. If there is profiteering or monopoly, i.e. distribution cost, such as withholding from enterprises, this includes several years of fresh labour or supplies or costs from cash distributions.

### Page 98

100

1. Background Theory for Characterization of Cholesky-Von Neumann Closure:
\begin{align*}
\partial u(t)&=\int_{t_0}^t\left[\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))e(t)^{T}\right]dt-\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))\mathcal{M}(x^{*}(t), u^{*}(t))e(t)^{T}+|\mathcal{M}(x^{*}(t), u^{*}(t))|^2 e(t)^{T}\mathcal{M}(x^{*}(t), u^{*}(t))e(t)^{T}\\
&\quad-\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))e(t)^{T}\text{Higher-order terms}.
\end{align*}
2. Rich Geometry of Set Symmetric Implicit Variational Solutions:
\begin{align*}
I=\int_0^t\left[\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))\mathcal{M}(x^{*}(t), u^{*}(t))e(t)^{T}\right]dt+\mathcal{U}(u^*)\text{Tangent space}.
\end{align*}
3. Refinement of Higher-Order Methods:
\begin{align*}
&\lim_{r\rightarrow\infty}Mu^{*}-I=-\mathcal{H}(x)(t)+|Mu^{*}(t)|^2+(|I+Mxx^*||Mu^{*}(t)|^2)ex(t)^{T}\\
&=-\left[\Lambda\right]\\^t_0
\end{align*}
4. Derivatives of Implicit Implicit-Explicit Method:
\begin{align*}
\begin{split}
\&e^{*}(t)=\|dt\|_{I_x^L}\\
&=\|Iu_{x}^{*}\|_{L_{p_1}^{L_2}}
\end{split}
\end{align*}

Page 238/472. Extract all text exactly.

5. Higher-Order Properties of Implicit Implicit-Extents Method: Algorithm:
\begin{align*}
\Big\lVert\frac{\partial Te(t)}{\partial u^*}\Big\rVert=\Big\uprho(I_{xx}(x^{*}(t),u^{*}(t))\Big\rVert+T_x).
\end{align*}
6. Implicit Extents Optimization of State-Values of Differential Invertible System: Two pure implicit variable inclusions
\begin{align*}
&\int_{t_0}^t\left[\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))e(t)^{T}\right]dt\\
&-\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))\mathcal{M}(x^{*}(t), u^{*}(t))e(t)^{T}+\mathcal{U}(u^*),
\end{align*}
7. Implicit and Exterior Implicit of EIV in Mean and Covariance Matrices:
\begin{align*}
\begin{split}
&\frac{\partial Te(t)}{\partial u^*}=\mathbb{V}(x)\\
&\frac{\partial Te(t)}{\partial u^*}=\int_0^t\left[Tx(x^{*}(t), x^{*}(t))+a_4(fu_*f^{T}(t))+a_6(fu_*f^{T}(t))e(t)^{T}\right]dt\\
&\quad+\frac{\partial \mathcal{U}}{\partial u^*}(u^*)\mathcal{M}_e(x^{*}(t))+T_\lambda,
\end{split}
\end{align*}

8. Better Approximation of EIV via Implicit Implicit-Extent Type Singular Value (ISV):
\begin{align*}
&\int_{t_0}^t\left[\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))e(t)^{T}\right]dt\\
&\quad-\frac{\partial \mathcal{M}}{\partial u}(x^{*}(t), u^{*}(t))e(t)^{T}\text{Higher-order terms}.
\end{align*}

To see the theory from the decomposition of \( \partial \mathcal{M}(x^{*}(t), u^{∗}(t)) \)  to \(Su(t)= x(t)^{T}C \),  for the same IC problem as 6 Cholesky method, we need to make the additional assumption of small |IMérieux(t)|, so that the Row reduction of the terms containing lower order IMérieux yields RH(qty)(t)=C\(\sup\|x(t)\|\|C\|\) For the Vénot Poincaré-Hilbert (TVP) problem, we also remember that to approximate a saddle point solutions, the 2-stage splitting operator should have the same low order ( t~ \(\frac{||S||||C||}{Imérieux(t)}\)  Exact Implicative Matrix Approximation with RGE spherical approach: Two levels implicit process for solving the method, of good bounds on dependent useful margin tells. Since in these two equations are needed close to zero iterations in matrix \(S'\), we can still solve this equation by using the inner product of nA local loops and nT= n2.

### Page 99

delta * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Copyrighted Material

March 27, 2024

extension to Hilbert spaces, and Fourier series analysis
(see, for example, Papageorgiou [69], Grothendieck [42], and Harrison [58]). The integration subalgebras are again an important special case, however, here we may have a quasi-norm or a quasi-metric that is an indefinite inner product rather than a Hilbert scalar product, leading to new geometric ideas.
Thus we have the question: how do we decompose the manifold itself into vector spaces?
Actually, it turns out that both necessary conditions for quantization can be solved simultaneously in Hilbert spaces and do not require the metric to determine the manifold in a natural way.
There are many other instances of continual degeneracy of the extension of the norm in the Bourbaki triple [92], [92] and the Ghering–Schwartz theorem [69], [96], [97].

Let us now examine the quasi-norm:
quasi-norm space
(field space):
\[ \mathcal{I}(x^*(t), u(t), p^*(t), t) < \mathcal{H}(x^*(t), u(t), p^*(t), t), \tag{5.3-12} \]

where \( | x^*(t)|^2 < a(x^*(t), u(t), p^*(t), t) \). That is, we have \( |x^*(t)|^2 \) on \(\mathcal{I}(x^*(t), u(t), p^*(t), t)\), for \( t \in [t_0, t_f] \).

Similar considerations apply for another system of quasi-norms and conditions on extension without embedding:
(field space, quasi-norm space, condition \( l^2 \))
since \( l^2 \) is also a Hilbert space, since duals of all Hilbert spaces satisfy the Riesz lemma, hence there is a Hermitian operator \( A \) on \( l^2 \) such that \( l^2 = u*L(x(t)), u(t) = \int_{t_0}^{t}d\lambda A(\lambda)v(\lambda) \), where \( L(x(t)) = a(x^*(t), u(t), p^*(t), t)x(t) \) and \( A(\lambda)v(\lambda) = ka(\lambda^*x^*(t), u(t), p^*(t), t)v(\lambda) \).

This implies inner product relations, so facton \( u(t) \) passing through the QR-factorization, we may write:
for \( t \in I_t \), \( u(t) = S P^{-1} x^*(t) \), Fourier expansion.
hence FLOOD (Q.R.)
\[\mathcal{L}(x^*(t), u(t), p^*(t), t) < \mathcal{H}(x^*(t), u(t), p^*(t), t ). \tag{5.3-13} \]
Thus, the conditions \( l^2 = u*L(x(t)), u(t) = u*\int_{t_0}^t A(\lambda)v(\lambda)d\lambda \) may be identifiable with the geometric expansion of the quantum map:
Hilbert义义: the Muller lemma
expanding the intersection: \(\int L(g)x(g)dg g=x \), necessary condition for \( u^* \) to be an optimal control are always met.

The new action satisfies: so let us turn to the \( x(t) \) ball: 3 components are explicitly solved. Thus we have one equation of motion which is the Marsden–Weinstein decomposition and any trajectories are solutions.
Systems of continuous tangential components are not covered in the case of finite-resource systems.
In finite-resource \( \mathcal{H}(x(t), u(t), p(t), t) \), \( g_n_g(t) \) is a Hammer multiplying internal system \( d\mathcal{L}(x) = u*dh(x) \).
For all \( t \in [t_0, t_f] \) and for all admissible controls. Equation (5.3-17), which indicates that an optimal control must minimize the Hamiltonian, is called Pontryagin's minimum principle. Notice that we have established a necessary, but not (in general) sufficient, condition for optimality. An optimal control must satisfy Pontryagin's minimum principle; however, there may be controls that satisfy the minimum principle that are not optimal.
Let us now summarize the principal results of this section. A control \( u^* \in \mathcal{U} \), which causes the system 
\[\dot{x}(t) = a(x(t), u(t), p(t), t) = a(x(t), u(t), p(t), t) x(t) \tag{5.3-18} \]
to follow an admissible trajectory that minimizes the performance measure 
\[J(u) = \mathcal{H}(x(t), t), t) = \int_{t_0}^{t} g(x(t), u(t), t)dt, \tag{5.3-19} \]
is sought. In terms of the Hamiltonian 
\[\mathcal{H}(x(t), u(t), p(t), t) \triangleq g(x(t), u(t), t) + p^T(t) [ a(x(t), u(t), t)), \tag{5.3-20} \]
necessary conditions for \( u^* \) to be an optimal control are

### Page 100

to follow an admissible trajectory that minimizes the performance measure 
\[J(u) = \mathcal{H}(x(t), t), t) = \int_{t_0}^{t} g(x(t), u(t), t)dt, \tag{5.3-19} \]
is sought. In terms of the Hamiltonian 
\[\mathcal{H}(x(t), u(t), p(t), t) \triangleq g(x(t), u(t), t) + p^T(t) [ a(x(t), u(t), t)), \tag{5.3-20} \]
necessary conditions for \( u^* \) to be an optimal control are

### Page 100

achieving a better quality result.This achieves a better quality result by adjusting the tail for the smallest fluctuations.

It should be emphasized that in addition, the minimum principle, although derived for controls with values in a closed and bounded region, can also be applied to problems in which the admissible controls are not bounded. This can be done by viewing the unbounded control region as having arbitrarily large bounds, thus ensuring that the optimal control will not be constrained by the boundaries. In this case, for \(\mathbf{u}^*(t)\) to minimize the Hamiltonian it is necessary (but not sufficient) that

$$\frac{\partial\mathcal{H}}{\partial\mathbf{u}}(\mathbf{x}^*(t), \mathbf{u}^*(t), \mathbf{p}^*(t), t) = \boldsymbol{0}.$$  (5.3-23)

If Eq. (5.3-23) is satisfied, and the matrix

$$\frac{\partial^2\mathcal{H}}{\partial\mathbf{u}^2}(\mathbf{x}^*(t), \mathbf{u}^*(t), \mathbf{p}^*(t), t) \neq \boldsymbol{0},$$ (5.3-24)

is positive definite, this is sufficient to guarantee that \(\mathbf{u}^*(t)\) causes \(\mathcal{H}\) to be a local minimum; if the Hamiltonian can be expressed in the form

$$\mathcal{H}(\mathbf{x}(t), \mathbf{u}(t), \mathbf{p}(t), t) = f(\mathbf{x}(t), \mathbf{p}(t), t) + [\mathbf{c}(\mathbf{x}(t), \mathbf{p}(t), t)]^T \mathbf{u}(t) + \frac{1}{2}\mathbf{u}^T(t)\mathbf{R}(t)\mathbf{u}(t),$$  (5.3-25)

### Page 101

有很大的不确定性的元素




Page 239/ 472
The Calculus of Variations and Pontryagin’s Minimum Principle Sec. 5.3

where c is an m × 1 array that does not have any terms containing u(t), then
satisfaction of (5.3-23) and ∂²ℋ/∂u² > 0† are necessary and sufficient for
ℋ(x*(t), u*(t), p*(t), t) to be a global minimum.

For ℋ of the form of (5.3-24),

∂²ℋ
⁄
= (x*(t), u*(t), p*(t), t) = R(t); (5.3-25)
∂u²

thus, if R(t) is positive definite,

u*(t) = −R[−1](t)c(x*(t), p*(t), t) (5.3-26)
¸

minimizes (globally) the Hamiltonian.

**Example 5.3-1. Let us now illustrate the effect on the necessary conditions**
of constraining the admissible control values. Consider the system having
the state equations

ẋ 1(t) = x₂(t)
ẋ 2(t) = −x₂(t) + u(t), (5.3-27)
¸

with initial conditions x(t₀) = x₀. The performance measure to be mini-
mized is

Ju = ¨t临近 [x [̇] 1(t) + u [^{2]}[t) dt; (5.3-28)

= ¨t临近 [x [̇] 1(t) + u [^{2]}[t) dt;

t _f_ is specified, and the final state x(t_f) is free.
=

a. Find necessary conditions for an unconstrained control to minimize J.
The Hamiltonian is

ℋ(x(t), u(t), p(t)) = ¹⁄₂x ̇ 1²(t) + ¹⁄₂u [^{2]}(t) + p₁(t)x₂(t)
− p₂(t)x₂(t) + p₂(t)u(t), (5.3-29)
¸

from which the costate equations are

ṕ¹̇ (t) = − [∂ℋ]⁄
∂x₁ ∂x₁[2]

ṕ²̇ (t) = −[ ∂ℋ]⁄
∂x₂ ∂x₂[2]

Since the control values are unconstrained, it is necessary that

[∂ℋ]⁄
ú²̇ = ú²̇ (t) + ṕ²̇ (t) = 0. (5.3-31)
⁄ [∂

† The notation ∂²ℋ/∂u² > 0 means that the m × m matrix ∂²ℋ/∂u² is positive definite.

### Page 102

expressing through the 'du/ at time t. 

\[u^{*}(t) = -p^{*}_{2}(t)\] (5.4-35)

\[u(t) = p^{*}_{2}(t)\] (5.4-36)

These setups are 
\begin{align*}
\text{located at points (canonically inf ...
\text{ entitled by the light blue arrows further to the right. Allfore collisions in this region are purely elastic and longitudinal with no shear terms; afterwards the angle turns toward the axis, and the atoms begin to rotate.
Conclusionally one millimeter in the direction of the real axis points to the triangle formed by the light base arrow, photon, and the terminal for lubric of the atom.)}
\end{align*}

In addition, Fig. 5-14 shows a 
\begin{center}
\[\mathbf{\mathcal{N}}(s) (5.4-37)\]
\end{center}

which is the system of polar coordinates, within the light base A on the other
\textbf{angular momentum.}
This last coordinate \( s \) continuously takes two different values:
\begin{equation}
\begin{align*}
s_i &= \theta_i t + \phi_i \\
s_{i + 1} &= \tau_i t
\end{align*}
\end{equation}
In other words, this unit of
\begin{equation}
\begin{align*}
s_{i + 1} &= \tau_i t \\
\tau_i &\text{admits 0}\#
\end{align*}
\end{equation}

Now it is known that collocation methods (Thuillier) are simplified, as they have lower correlation to calculate vector correlation (Eq. 4.18). 

\\square

\[u^{*}(t) - 1 = 2\] (5.3-38)

\[\frac{du^{*}}{du} = 1 \######Eq. 5.3-22 (Striveive) Eq. 5.3-23 (Striveive) Eq. 5.3-24 (Striveive) Eq. 5- 5\]

\textbf{qcont} checks for 3cm.

### Page 103

.FIGURE 5-14 Constrained and unconstrained optimal controls for Example 5.3-1

\[ u^*(t) = \begin{cases} -1, & \text{for } 1 \leq p_2^*(t) \\ -p_2^*(t), & \text{for } -1 \leq p_2^*(t) \leq 1 \\ +1, & \text{for } p_2^*(t) < -1. \end{cases} \quad (5.3-39a) \]

To determine \( u^*(t) \) explicitly, the state and costate equations must be solved. Because of the differences in Eqs. (5.3-33) and (5.3-39a), the state-costate trajectories in the two cases will be the same only if the initial state values are such that the bounded control does not saturate. If this situation occurs, the control constraints do not affect the solution. It must be emphasized that the optimal control history for part b cannot be determined, in general, by calculating the optimal control history for part a and allowing it to saturate whenever the stipulated boundaries are violated.

Additional Necessary Conditions

Pontryagin and his co-workers have also derived other necessary conditions for optimality that we will find useful. We now state, without proof, two of these necessary conditions:

1. If the final time is fixed and the Hamiltonian does not depend explicitly on time, then the Hamiltonian must be a constant when evaluated on an extremal trajectory; that is,

\[ \mathcal{H} (x^*(t), u^*(t), p^*(t)) = c_1 \quad \text{for } t \in [t_0, t'_f]. \quad (5.3-40) \]

2. If the final time is free, and the Hamiltonian does not explicitly depend on time, then the Hamiltonian must be identically zero when evaluated on an extremal trajectory; that is,

\[ \mathcal{H} (x^*(t), u^*(t), p^*(t)) = 0 \quad \text{for } t \in [t_0, t_f]. \quad (5.3-41) \]

### Page 104

accounting for all contributions to costs.Let us now consider problems in which there may be inequality constraints that involve the state variables as well as the controls. It will be assumed that the state constraints are of the form

\[ f(x(t), t) \geq 0, \tag{5.3-42} \]

where \( f \) is an \( l \)-vector function (\( l \leq m \)) of the states and possibly time, which has continuous first and second partial derivatives with respect to \( x(t) \). It will also be assumed that the admissible control values lie in a closed and bounded region. Our approach will be to transform the \( l \) inequality constraints of (5.3-42) into a single equality constraint, and then to augment the performance measure with this equality constraint, as we have done previously with the state equations.

Let us define a new variable \( \dot{x}_{n+1}(t) \) by

\[ \dot{x}_{n+1}(t) \triangleq [f_1(x(t), t)]^2[(1)(f_1) + (f_2(x(t), t)]^2[(1)(f_2) + \cdots + (f_l(x(t), t)]^2[(1)(f_l), \tag{5.3-43} \]

where \([ ( - f_i ) ] \) is a unit Heaviside step function defined by

\[ [ ( - f_i ) ] = \begin{cases} 
0, & \text{for } f_i(x(t), t) \geq 0 \\
1, & \text{for } f_i(x(t), t) < 0, 
\end{cases} \tag{5.3-44} \]

for \( i = 1, 2, \ldots, l \). Notice that \( \dot{x}_{n+1}(t) \geq 0 \) for all \( t \), and that \( \dot{x}_{n+1}(t) = 0 \) only for times when \( a_l \) of the constraints (5.3-42) are satisfied. Now let us require that the variable \( x_{n+1}(t) \) given by

\[ x_{n+1}(t) = \int_{t_0}^t\dot{x}_{n+1}(t) dt + x_{n+1}(t_0), \tag{5.3-45} \]

satisfy the two boundary conditions \( x_{n+1}(t_0) = 0 \) and \( x_{n+1}(t_f) = 0 \). Since \( \dot{x}_{n+1}(t) \geq 0 \) for all \( t \), satisfaction of these boundary conditions implies that \( \dot{x}_{n+1}(t) \) must be zero throughout the interval \([ t_0, t_f ] \), but this occurs only if the constraints are satisfied for all \( t \in [ t_0, t_f ] \).

Thus, to minimize the functional

\[ J(u) = h(x(t_f), t_f) + \int_{t_0}^{t_f} g(x(t), u(t), t) dt \tag{5.3-46} \]

subject to the state equation constraints

\[ \dot{x}(t) = a(x(t), u(t), t), \tag{5.3-47} \]

\(\dagger \) The notation \( f(x(t), t) \geq 0 \) means that each component of the vector \( f \) is \( \geq 0 \).

### Page 105

represents the purification of \( t \). Therefore, it represents a purification that handles the effect of \(\sqrt{1 - x_{n+1}(t)}\) as we have quantified. (k) Packet \(\sqrt{1 - x_{n+1}(t)}(t)\), the resulting packet, is zero if never sent, i.e., \(\sqrt{1 - x_{n+1}(t)}(d \to \infty )\) but \(\sqrt{1 - x_{n+1}(t)}(d \to \infty ) = 0\) if \(\sqrt{1 - x_{n+1}(t)} = 0\) and \(\sqrt{1 - x_{n+1}(t)}(d -> is \to 0)\) and was sent in the filter (of attenuation) for \(\sqrt{1-x_{n+1}(t)}(t)\) of the problem module, \((x\ and x\ away = 0)\) (k) If \(S.x_{n+1}(t) < \sqrt{1-x_{n+1}(t)}\) for some \(d>=k\ infinite\), i.e., the \(\gamma_{n+1}\) was not reporting anypacket if its transmission is zero, at this point, the hardware tracing module \(x_{n+1}(t)\) reports on the message \(\sqrt{1-x_{n+1}(t)} = 0\) delay to packet \(\gamma_{n+1}\) of \(\sqrt{1 - x_{n+1}(t)}(t)\) is than the packet for which the communication is on. Thus, if the overall eigenvectors \(u(t)\) of the system are not exactly Wilkinson functions (using Equation (5.3.46)). In fact, for \(d=0\), we have:

\[
\vec{a}_{n+1}(\vec{x}(t), t) = a_{n+1}(\vec{x}(t), t) + M \vec{\zeta}_n,\]
where \(\vec{\eta}(\vec{x}(t),\mathcal{O} \sum_{x = 0}^{X}(\vec{\zeta}_{+}(t)) \epsilon \sum_{t = 0}^{X}(\vec{\zeta}_{+}(\vec{x}(t))hat})\) are packets that, within a packet length of the packets \(\vec{x}_{n+1}(t+1)\). with \(|\vec{x}_{+}(c)(t)| = hn + \alpha\) and

Using the notation of (5.3.49) means that \(\mathbf{p}(t)\) and \(\mathbf{x}(t)\) are \(n + 1 \input\). Notice that the Hamiltonian does not contain \(x_{n+1}(t)\) explicitly. Thus use (5.3.2) to obtain necessary conditions for optimality:

\[
k:1.\ a_{rl}(\vec{x}(t), u, **[u], \vec{x}(t), p \beta)]
.\]

Using the notation of (5.3.49) means that \(\mathbf{p}(t)\) and \(\mathbf{x}(t)\) are \(n + 1\) vectors. Notice that the Hamiltonian does not contain \(x_{n+1}(t)\) explicitly. We can now apply Eqs. (5.3.21) to obtain necessary conditions for optimality:

\[
\dot{\gamma}^{*}(t) = a_{n+1}(\mathbf{x}^{*}(t), u^{*}(t),)
.\]

\[
if \forall all
\
t \in \left[ I_{a}, \ t_{*
}{
\psi_{n-1}^{s}(*)
}(5.3.52) \cdot
}
\
\[\dot{z}_{n-1}^{*}(t) = a_{n+1}(x^{*}(t), t);\
\
\psi_{n-1}^{*}(t) = - \frac{\partial X}{\partial x_{n+1}} \alpha*(*)\beta_{*}.
]

and

\[
\vec{\Xi}(\mathbf{x^*(t)}) \beta{u},\mathbf{x^**)'(t)},\alpha(u).\ qr那句话 i].
for all admissible u(t).

p^{n+1}(t) is zero because x_{n+1}(t) does not appear explicitly in Z. The boundary conditions \(\mathbf{x\ **(t)} are specified [\mathbf{x^*(*+)} = 0 and \mathbf{x^*(*+)} = 0]; the remaining boundary conditions at t = t+\ abc^{(*)}(d)=0\) can be determined by using the results obtained in Section 5.1.\]

Recall that \(Z_{n+1}$. Let us now return to the problem discussed earlier in Example 5.3-1. The system

### Page 106

} Note that \(e^{\frac{a}{t}} = 1 + \frac{a}{t} + \frac{a^2}{2!t} + \cdots + \frac{a^n}{n!t} + O(a^m)\) for \(0 \leq |a| < \infty\) and all nonzero \(n\). For instance, if \(a=0\), then \(\frac{e^t-1}{t}=\ln(1+t)\) so the binomial series for \(-\frac1te^t\) is \(\frac1t(1-t)\).

6.  Let \(f(t)=t^5\), \(g(t)=t^5\), and \(h(t)=t^4\). Find the logarithmic derivative of \(g(t)\). From this expression, show that \(f'(t) = 0\) and \(g'(t) = 1 + 5t^4\).

### Page 107

} .p.21](j{t)

Figure 5-26 Possible forms for the costate and the corresponding fuel-optimal controls Notice that the costate \(u^* (t)\) is not unique at the maximum (intersection with the vertical line). Figure 5-26 shows several possible forms for \(u^* (t) \) for \(p^* (t) \). Each of the forms has the form \(u^* (t) = c_1\), where \(-1 < c_1 < 0\) is an upper control bound (above this bound cost does not go to infinity). Each form \(u^* (t) = c_1\), where \(-1 < c_1 < 0\) is an upper (or lower) control bound (above this bound the optimal control always goes to infinity), but appeared to be more popular (although \(u^* (t) = c_1\) was believed to be a lower control bound). Each form \(u^* (t) = -c_1\), where \(0 < c_1 < 1\) is a lower control bound (below this bound the optimal control does not go to the boundary), so \(p^* (t) = 1\) is a lower costate. The costate \(u^* (t)\) in this case is an upper costate. Each form \(u^* (t) = c_1\), where \(0 < c_1 < 1\) a lower value between of the boundaries, represents an optimal control (always affects the costate, passing through the boundary between the costates

### Page 108

92

~ 272/472
c(t) = 6-ctx0 + 6-ct(0u(t)dt. (5.5-35)

Notice that if the control is identically zero, then at 1= 27

xl@)= e—«T' x0. (5.5-36)

Since the system is stable, it naturally moves toward zero when no control is applied. If we are willing to wait long enough, the system will come arbitrarily close to (but never precisely reach) zero—and without the expenditure of any control effort at all. However, the problem statement stipulated that x(t_f) =0,notlx,h)=~T,where is some arbitrarily small positive number. If x0 > 0, then clearly ul=-1),{0, —1} are the only possible choices for the optimal control (why?). If u(t) = 1 for tE [D,t{, it can be shown from (5.5-35) that x(t,r) = 0 implies

cr_

1
4
am(ax0+1)r (5.5-37)

thus, the fuel consumption using this control would be \((u x_{0}+1)\left|/a\).

Now, suppose u(t)= 0 is applied for 0 <t < t, and u(t) =-1 for t= 1 t S t f. From (5.5-35)

x(t,_)= e-r27rx0 +=e-l (17 aer[-1]dt; (5.5-38)

setting x(t_f) = O and performing the indicated integration, we obtain

O = e-otx0 — atx0 = [1 — e_Tr-Or]. (5.5-39)

Solving for t_f — t1 gives

t_f - t, = — a In(1— axT') (5.5-40)

but since t, is free, axoEr are can be made arbitrarily small by letting

- 00, so

[r, — t,]—>0 as' tr—>-00. (5.5-41)

But /r — t, is the interval during which u = —1 is applied, and by making 17 very large the consumed fuel can be made arbitrarily small (but not zero). Our conclusion is that if /r is free an optimal control does not exist—given any candidate for an optimal control, it is always possible to find a control that transfers the system to the zero state with less fuel.

It is left as an exercise for the reader to verify that the same conclusions hold when xo < 0.

### Page 109

value} to act against it.In the preceding example we have simply verified mathematically what common sense tells us; if elapsed time is not penalized, and the system moves toward the desired final state without consuming any fuel, the optimal strategy is to let the system drift as long as possible before any control is applied. At this point the reader might wonder: what did the minimum principle do for us? Could we not have deduced the same conclusions without using it at all? The answer to these questions is that quite likely the same conclusions could have been reached by intuitive reasoning alone, but the minimum principle, by specifying the possible forms of the optimal control, greatly reduced the number of control histories that had to be examined. In addition, we must remember that our interest is in solving problems that generally require more than physical reasoning and common sense.

Let us next discuss minimum-fuel problems with fixed final times.

**Fixed Final Time.** First, let us reconsider the preceding examples with the final time specified; that is, $t_f = T$. The value of $T$ must be at least as large as $t^*$, the minimum time required to reach the specified target set from the initial state $x_0$.

In Example 5.5-1 we touted that the optimal control was nonunique—there were an infinite number of controls that would transfer the system to $x(t_f) = 0$ with the minimum possible amount of fuel. The situation with $t_f = T$ is much the same unless $T = t^*$. In this case, the minimum-fuel and minimum-time controls are the same and unique. If, however, $T > t^*$, there are again an infinite number of controls that are optimal; it is left as an exercise for the reader to verify that this is the case. Fixing the final time does not alter the nonuniqueness of the optimal controls for the system of Example 5.5-1.

Let us now see if fixing the final time has any effect on the existence of fuel-optimal controls for the system of Example 5.5-2.

**Example 5.5-3.** The possible forms for optimal controls and the solution of the state equation are given in (5.5-34) and (5.5-35). If the fixed final time $T$ is equal to the minimum time $t^*$ required to reach the origin from the initial state $x_0$, then $u^*(t)$ is either $+1$ or $-1$ throughout the entire interval $[0, T]$, and

$$x(T) = 0 = \epsilon^{-\alpha T} x_0 + \epsilon^{-\alpha T} \int_0^T \epsilon^{\alpha t} [\pm 1] dt,$$  \hfill (5.5-42)

or

$$x = \mp \frac{1}{a} [\epsilon^{\alpha T} - 1].$$ \hfill (5.5-42a)

This expression defines the largest and smallest values of $x_0$ from which the origin can be reached in a (specified) time $T$. Initial states that satisfy

### Page 110

right.</p>
-1. 
<center>Page 274/472.</center>

\[\frac{1}{a} [\epsilon^{\alpha T} - 1] < |x_0|\] (5.5-43)

cannot be transferred to the origin in time \(T\); therefore, we shall assume in what follows that

\[|x_0| \le \frac{1}{a} [\epsilon^{\alpha T} - 1].\] (5.5-44)

If (5.5-44) is an equality, this means that \(T = t^*\); otherwise, \(T > t^*\), and the form of the optimal control must be as shown in Fig. 5-26(b) or (c). The optimal control must be nonzero during some part of the time interval, because we have previously shown that the system will not reach the origin in the absence of control.

If \(x_0 > 0\), the optimal control must have the form \(u^* = [0, -1]\) shown in Fig. 5-26(b). Substituting \(u(t) = 0,\; t \in [0, t_1),\; u(t) = -1,\; t \in [t_1, T]\), in (5.5-35) and performing the integration, we obtain

\[x(T) = 0 = \epsilon^{-\alpha T} x_0 - \frac{1}{a} \epsilon^{-\alpha T} [\epsilon^{\alpha T} - \epsilon^{\alpha t_1}].\] (5.5-45)

Solving this equation for \(t_1\), the time when the control switches from 0 to \(-1\), gives

\[t_1 = \frac{1}{a} \ln (\epsilon^{\alpha T} - ax_0).\] (5.5-46)

Similarly, if \(x_0 < 0\), the optimal control has the form \(u^* = [0, +1]\) shown in Fig. 5-26(c), and

\[x(T) = 0 = \epsilon^{-\alpha T} x_0 + \frac{1}{a} \epsilon^{-\alpha T} [\epsilon^{\alpha T} - \epsilon^{\alpha t_1}].\] (5.5-47)

Solving for the switching time \(t_1\) yields

\[t_1' = \frac{1}{a} \ln (\epsilon^{\alpha T} + ax_0).\] (5.5-48)

From (5.5-46) and (5.5-48) the optimal control is

\[u^*(t) = 
\begin{cases} 
0, & \text{for } x_0 > 0 \text{ and } t < \frac{1}{a} \ln (\epsilon^{\alpha T} - ax_0) \\
-1, & \text{for } x_0 > 0 \text{ and } \frac{1}{a} \ln (\epsilon^{\alpha T} - ax_0) \le t \le T \\
0, & \text{for } x_0 < 0 \text{ and } t < \frac{1}{a} \ln (\epsilon^{\alpha T} + ax_0) \\
+1, & \text{for } x_0 < 0 \text{ and } \frac{1}{a} \ln (\epsilon^{\alpha T} + ax_0) \le t \le T.
\end{cases}\] (5.5-49)

### Page 111

reflecting about the specific role of the initial prescribing values, \(\epsilon^{-\alpha T}\) and \(\gamma=\Phi^{\alpha T}\), respectively. If \(\rho\) is infected at \(0\) with approximately half the initial infectiousness, the solutions converge to the exact state 0. The limiting values for the solutions converge. The solution \(\phi\) converges faster for the more concentrated initial value \(x_0\). The precept of the exercise is to relate the number of initial infections to the time of the first encounter. Yet, the variable \(\epsilon^{-\alpha T}\) decreases with infinite time because \(t\to \infty\).

The values \(\rho=0.1\) and \(\gamma=0.1\) result in \(\phi(\epsilon^{-\alpha T})\) having no impact for \(\alpha\) close to \(1\), although \(\epsilon^{-\) would ensure that an endemic equilibrium is eventually attained. More precisely, the initial infection will initially decrease the number of the associated \(T\) parameters in order to arrive at equilibrium at the Minkowski scale.


### Equation (5.44)
\[ 
u^{\*}(X) = e(x_0, t).
\]
### Equation (5.45)
To obtain the optimal control law, we observe that
\[ x(T) = \epsilon^{-\alpha |T|-\nu} x(t) + \epsilon^{-\alpha T} \int_t^T \epsilon^{\alpha u}(\tau) d\tau \]
### Equation (5.46)
for all \(t\). We know that during the last part of the time interval the control is either \(+1\) or \(-1\), depending on whether \(x(t)\) is less than zero or greater than zero; thus, assuming \(x(t) > 0\), we have
\[ x(T) = 0 = \epsilon^{-\alpha |T|-\nu} x(t) - \epsilon^{-\alpha T} \int_t^T \epsilon^{\alpha u}(\tau) d\tau, \quad t \geq t_1. \]
### Equation (5.47)
Performing the indicated integration and solving for \(x(t)\) gives
\[ x(t) = \frac{1}{\alpha} \left[ \epsilon^{\alpha |T|-\nu} - 1 \right], \quad t \geq t_1. \]
### Equation (5.48)
During the initial part of the time interval, the optimal control is zero; consequently,
\[ x(t) = \epsilon^{-\alpha u} x_0, \quad t < t_1. \]
### Equation (5.49)
The switching of the control from 0 to \(-1\) occurs when the solution (5.55) for the _coasting interval_ (\(u = 0\)) intersects the solution (5.54) for the _on-negative interval_ (\(u = -1\)). Figure 5-27 shows these solutions. Defining
\[ z(T-t) \equiv \frac{1}{\alpha} \left[ \epsilon^{\alpha[T-t]}-\frac{1}{\alpha} \right], \]
### Equation (5.50)
we observe that the control should switch from \(0\) to \(-1\) when the state \(x(t)\) is equal to \(z(T-t)\). It is left as an exercise for the reader to verify that if \( - \left[ \epsilon^{a T} - 1 \right] / \alpha < x_0 < 0\) the optimal control switches from \(0\) to \(+1\) when
\[ x(t) = -z(T-t). \]
### Equation (5.51)
To summarize, the optimal control law is
5.66 The Calculus of Variations and Pontryagin's Minimum Principle Sec. 5.5
Note that the optimal control expressed by (5.49) is in open-loop form, because \(u^{\*}(t)\) has been expressed in terms of \(x_0\) and \(t\); that is,
\[ u^{\*} (t) = e (x_0, t). \]
### Equation (5.52)
From an engineering point of view we would prefer to have the optimal control in feedback form; that is,
\[ u^{\*} (t) = f (x(t), t). \]
### Equation (5.53)
To obtain the optimal control law, we observe that the solution of the minimizing problem is the maximum pressure for this problem, and is given by

\[ u^* (t) = p (x(t) / \alpha \left[ \int_t^T \alpha u (\tau) d\tau \right] = v(x_0, t) / \alpha - \left[ \epsilon^\alpha T - 1 \right]. \]

### Equation (5.54)
The value function \(v\) can be given by \(v = 1, \nu = 1\) respectively, and is therefore the triangular pulse with very slow (very fast) settling.

\[ v (x_0, t) = t. \]

\[ v (t, x_0) = \]

### Page 112

Hobbes pdf

Thus, the filter must use a square root, or a third-order good approximation to the cosine function to be effective.

After gathering these results, the filter becomes the frequency filter we know and recognize, the second-order butterworth-SiC filter. Using the transfer function derived earlier,

\[\frac{H(j\omega)}{X(j\omega)} = \frac{1}{1+j\omega\tau}\]

we now enter the problem tackled

\[X(j\omega) = G(j\omega)H(j\omega) = G(j\omega)\frac{1}{1+j\omega\tau}\]

and use the approximation

\[|S(j\omega)| \ll 1\]

having processed \(G(j\omega)+H(j\omega)\). Anticipating and factoring the previous neglecting terms we get

\[\frac{H(j\omega)}{X(j\omega)} = |G(j\omega)|(1-\tau^2)\frac{\cos(\sqrt{2}\tau\omega dt)}{2}\]

To retrieve the voltage units we divide by \(1-\tau^2\). This filter's propagation or time delay is inherent in its control law, thus, the analysis/design technique is not completely rigorous.

The filter's time delay is more obvious for the case.

Finite Time Delay (Time Constrained Control)

To illustrate the dynamics by a just-in-time delay, in the upcoming section with a rational controller, as set up before. There we defined the second derivative \(\frac{d^2}{dt^2}\) in the algebraic formula;

\[x'(t) =

\begin{cases}

### Page 113

}">

## a **FIG 5-28 Implementation of a time-varying fuel-optimal control law. ##**

### **Figure 5-28** Implementation of a time-varying fuel-optimal control law.

### **Figure**a elation of a teaราฬing fuel-optimal control law.

### **Figure** 28 Implementation of a time-varying fuel-optimal control law.

### **Diagram** The equation indicates that fuel consumption is dependent on the time and the gradient of the fuel consumption function.

### Page 114

value of the explanatory variable.

The economically-speak...
```
Using Eq. (5.5-60), the designer can obtain a plot of consumed fuel versus final time for several values of \(x_0\) selected from the range of expected initial conditions; one such curve is shown in Fig. 5-29 for \(|x_0| = 10.0\) and \(a = 1.0\). The selection of \(T\) is then made by subjectively evaluating the information contained in these curves. Figure 5-29 indicates that in this particular example the value chosen for \(T\) will reflect the relative importance of consumed fuel and elapsed time. 

The reader may have noticed that in Examples 5.5-1 through 5.5-3 a "trade-off" existed between fuel expenditure and elapsed time. The reason for this is that in each case the target set was the origin, and with no control applied the state of these systems either moved closer to the origin (Examples 5.5-2 and 5.5-3) or remained constant (Example 5.5-1). If the plants were of such a form that the states moved away from the target set with no control applied, the solutions obtained could have been quite different—see Problem 5-28. 

    Figure 5-29 Dependence of consumed fuel on specified final time \(T, |x_0| = 10\). 

A Weighted Combination of Elapsed Time and Consumed Fuel as the Performance Measure. 

The preceding examples in this section illustrated a trade-off between elapsed response time and consumed fuel; that is, the fuel expended to accomplish a specified state transfer was inversely proportional to the time required for the transfer. One technique for handling problems in which this
```
Illegal notation: `Figure 5-29 Dependence of consumed fuel on specified final time T, |x₀| = 10`.

#### Title
A Weighted Combination of Elapsed Time and Consumed Fuel as the Performance Measure.

| Delimiter | Description | Code |
|----------|-------------|------|
| `Figure` | Deprivation | 5.29 |
| `Dependence` | Description | Explanation |
| `T, |x₀| = 10` | A weighting technique for handling problems in which this |


Bold italics apply for keywords.

Figure 5-29 Dependence of consumed fuel on specified final time T, |x₀| = 10.

### Page 115

有很大的空间。trade-off is present is to include both elapsed time and consumed fuel in the performance measure. For a system with one control, such a performance measure would have the form

\[ J(u) = \int_{t_0}^{t_f} [\lambda + |u(t)|] dt. \qquad (5.5-61) \]

The final time \( t_f \) is free, and \( \lambda > 0 \) is chosen to weight the relative importance of elapsed time and fuel expended. For \( \lambda \rightarrow 0 \) the optimal system will resemble a free-final-time, fuel-optimal system, whereas for \( \lambda \rightarrow \infty \) the optimal solution will resemble a time-optimal solution. Let us now reconsider Example 5.5-2 with (5.5-61) as the performance measure.

**Example 5.5-4.** The state equation and control constraint are given in Eqs. (5.5-27) and (5.5-28). The Hamiltonian is

\[ \mathcal{H}(x(t), u(t), p(t)) = \lambda + |u(t)| - p(t)ax(t) + p(t)u(t), \qquad (5.5-62) \]

and the costate equation is (again)

\[ \dot{p}^*(t) = ap^*(t); \qquad (5.5-63) \]

thus,

\[ p^*(t) = c_1 t^\alpha, \qquad (5.5-64) \]

where \( c_1 \) is a constant of integration. The requirement that \( u^*(t) \) minimize the Hamiltonian on an extremal trajectory is unaffected by the presence of \( \lambda \) in the performance measure; therefore,

\[ u^*(t) = \left\{ \begin{array}{ll} 1.0, & \text{for } p^*(t) < -1.0 \\ 0, & \text{for } -1.0 < p^*(t) < 1.0 \\ -1.0, & \text{for } p^*(t) > 1.0 \end{array} \right. \qquad (5.5-65) \]

underestimated, but nonnegative for \( p^*(t) = -1.0 \); and underenforced, but nonpositive for \( p^*(t) = +1.0 \).

If we recall that \( a > 0 \), Eq. (5.5-64) ensures that \( p^*(t) \) cannot equal \( \pm 1.0 \) for a nonzero time interval; hence, there are no intervals of singular control.

Equations (5.5-64) and (5.5-65) indicate that the optimal control must again be one of the forms shown in Fig. 5-26. Let us now examine the various alternatives.

Suppose that \( t_0 = 0 \) and \( u^*(t) = 0 \), \( t \in [0, t_f] \); this implies that

\[ \mathcal{H}(x^*(t), 0, p^*(t)) = \lambda - p^*(t)ax^*(t) \quad \text{for all } t \in [0, t_f]. \qquad (5.5-66) \]

If \( p^*(t) = \pm 1.0 \) for a nonzero time interval, this signals the singular condition.

### Page 116

2 where 0 is the problem of the starting state boundary, but of particular interest when $\lambda.$

In this problem the final time is free and $t$ does not appear explicitly in the Hamiltonian; therefore, from Eq. (5.3-41), 

\[ \mathcal{H}(x^*(t), u^*(t), p^*(t)) = 0 \quad \text{for all } t \in [0, t_f]. \quad (5.5-67) \]

If Eq. (5.5-67) is to be satisfied, then Eq. (5.5-66) implies that

\[ x^*(t) = \frac{\lambda}{ap^*(t)}, \quad \text{for all } t \in [0, t_f]. \quad (5.5-68) \]

Since $x^*(t_f) = 0$, Eq. (5.5-68a) can be satisfied for $\lambda > 0$ at $t_f$ only if $t_f \to \infty$, but this implies that the minimum cost approaches $\infty$. From our earlier discussion of this example, however, we know that controls can be found for which $J < \infty$; therefore, we conclude that $\dot{u}(t) = 0$, $t \in [0, t_f]$, cannot be an optimal control. 

If $u^* = [0, -1]$ is the form of the optimal control, $p^*(t)$ must pass through the value $+1.0$ at the time $t_1$, when the control switches [see Eq. (5.5-65)]. In addition, we know from Eq. (5.5-65) that $u^*(t_1)$ is some nonpositive value, so $\dot{u}^*(t_1)| = -u^*(t_1)$. The Hamiltonian must be zero for all $t$; thus, at time $t_1$

\[ \mathcal{H}(x^*(t_1), u^*(t_1), p^*(t_1)) = \lambda - \dot{u}^*(t_1) - ax^*(t_1) + u^*(t_1) = 0, \quad (5.5-69) \]

Since $x^*(t_f) = 0$, Eq. (5.5-68a) can be satisfied for $\lambda > 0$ at $t_f$ only if $t_f \to \infty$, but this implies that the minimum cost approaches $\infty$. From our earlier discussion of this example, however, we know that controls can be found for which $J < \infty$; therefore, we conclude that $\dot{u}(t) = 0$, $t \in [0, t_f]$, cannot be an optimal control. 

If $u^* = [0, -1]$ is the form of the optimal control, $p^*(t)$ must pass through the value $+1.0$ at the time $t_1$, when the control switches [see Eq. (5.5-65)]. In addition, we know from Eq. (5.5-65) that $u^*(t_1)$ is some nonpositive value, so $\dot{u}^*(t_1)| = -u^*(t_1)$. The Hamiltonian must be zero for all $t$; thus, at time $t_1$

\[ \mathcal{H}(x^*(t_1), u^*(t_1), p^*(t_1)) = \lambda - \dot{u}^*(t_1) - ax^*(t_1) + u^*(t_1) = 0, \quad (5.5-69) \]

which implies that

\[ x^*(t_1) = \frac{\lambda}{a}. \quad (5.5-70) \]

This equation is an important result, for it indicates that if there is a switching of control from 0 to $-1$ it occurs when $x^*(t)$ passes through the value $\lambda/a$. From Eq. (5.5-35)—the solution of the state equations—and Eq. (5.5-70) we obtain the family of optimal trajectories

\[ x(t) = x_0 e^{-\alpha t} \quad \text{for } x(t) > \frac{\lambda}{a} \quad (5.5-71a) \]

\[ x(t) = \frac{\lambda}{a} e^{-\alpha [t-t_1]} - \frac{1}{a} [1 - e^{-\alpha [t-t_1]}] \quad \text{for } 0 < x(t) \leq \frac{\lambda}{a}. \quad (5.5-71b) \]

A control of the form [0, $-1$] cannot transfer the system $\dot{x}(t) = -ax(t) + u(t)$ from a negative initial state value to the origin; hence, Eq. (5.5-71) applies for $x_0 > 0$. 

Optimal trajectories for several different values of $x_0$ are shown in Fig. 5-30. Notice that if $0 < x_0 \leq \lambda/a$, the optimal strategy is to apply...

### Page 117

is:</math> The curve <math>{u^*(t) = -1}</math> has a corner at the origin. At the critical point <math>{x_0 < \lambda/a}</math>, the sun enters the orbit.<br /><br />(7.78)<br /><br />The critical value of <math>{x_0}</math> corresponds to the maximum, with <math>{u^*(0) = 0}</math>, since it is the value the curve may pass when <math>x(t)</math>is negative <math>{x(t) \le 0}</math>.<br /><br />The Eulerian force equation (7.79) is <math>{R_{\alpha\beta}|_x=f}</math>, whose sign <math>{+}</math> means it pushes out, <math>{[dR_{\alpha\beta}/dx_f(a)]_{\alpha = 0}} = 0</math> (situation II, <math>{\alpha = 0}</math>).<br /><br />(I082)<br /><br />If <math>-\lambda/a</math> lurks to the left, and the only way rightward is to allow the exit event instead, then <math>{R_{\alpha\beta}|_t=a+}</math> indicates that this limit on the force of inspiration is attained at the end (<math>\lambda/a \le 0</math>).<br /><br />It follows that the two cases (maybe for both) are conceptually divided by the following affine constraint:<br /><br />
<math>
\displaystyle g_1(x) \le 0, \qquad g_2(x) > 0
</math> (7.79a)<br /><br />

The reader can show that for <math>{x_0 < -\lambda/a}</math>, the optimal strategy is to allow the system to coast (with <math>{u^*(t) = 0}</math>) until it reaches <math>{x(t) = -\lambda/a}</math>; that is, the optimal control switches to <math>{u^*(t) = +1}</math>.<br /><br />The optimal control law---which is _time-invariant---is summarized by<br /><br />

<math>
\begin{aligned}
    & 0,  \ \ f(\lambda/a) < x'(t) \\
    & -1.0, \ \ f(\lambda/a) \le x'(t) \le \lambda/a \\
    & 1 + 0. \ \ f(\lambda/a) \le x'(t) \le \lambda/a \\
    & \vdots \\
    & + 0. \ \ f(\lambda/a) > x'(t) \ge \lambda/a \\
    & 0, \ \ f(\lambda/a) < 0 \\
    & -1, \ \ f(\lambda/a) \le 0, \ \ f(\lambda/a) \ge 0 \\
    &\vdots
\end{aligned}
</math> (7.79b)<br /><br />The reader can verify that for <math>{x_0=a}</math>: <cmath>
\displaylines{
    -1 \le x(t) \le \lambda/a \\
    x'(t) \le \lambda/a \\
    x = 0 \text { for } a =
+x_0
</cmath>

Such a family of optimal control is given by:<br /><br />'''Theorem:'''<br /><br />'''Statement:''' (7.79a) can be rewritten in the form <cmath>
\begin{aligned}
    0, \ \ f_1(\lambda) < x'(t) \le \lambda/a \\
    +1, \ \ f_1(\lambda/a) \le x'(t) \le \lambda/a \\
    \vdots \\
    + 1.0, \ \ f_1(\lambda/a) \le x'(t) \le \lambda/a \\
    & 0, \ \ f_1(\lambda) < 0 \\
    -1, \ \ f_1(\lambda) \le 0, \ \ f_1(\lambda/a) > 0 \\
    \vdots
</math>

It is easy to "verify" that the limit on the sun's force lies along the line <math>{x'(t) = \lambda/a,-1,0,1,1+a}</math> (see Fig. 7.30). We conclude that the corresponding optimal control law is <cmath>
\begin{aligned}
    + 1.0, \ \ f_1(\lambda/a) \le x'(t) \le \lambda/a \\
    \frac{v)}{u} = 1,
\end{aligned}
</math> (7.79a)


The maximum value of <math>u(t)</math>: <cmath>
\displaylines{
    \frac{0+f_1(\lambda)}{u} = 0, \\
    +1 \le \frac{u^*}{\lambda/a} = \frac{\lambda}{\lambda - a} = {
0\leq x'(t) \le a
}
    </cmath>
In words, the optimal entropy rise this time <math>t \ge a</math>; there will be no optimal entropy rise (of the control system) after this moment. Further, given the specified initial entropy <math>\xi_0</math> and near-unity (at least, so far) entropy increment, we may conclude that, for all times <math>t \ge a</math>, the entropy below is lowest achieved here.<br /><br />'''Correction'''Explicitly, for <math>\ l = l(x(t)) \le x'(t) \le -l</math> work does not require making a first approximation (because, at any time <math > t = 0</math>, we have <math>a = x(0)</math> ).

### Page 118

.Figure 5-31 illustrates this optimal control law and its implementation. In solving this example the reader should note that we were able to determine the optimal control law using only the form of the costate solution—there was no need to solve for the constant of integration \(c_1\). We also exploited the necessary condition that \[\mathcal{K}(x^*(t), u^*(t), p^*(t)) = 0, \quad t \in [0, t_f],\] (5.5-73) for \(t_f\) free and \(\mathcal{K}\) not explicitly dependent on \(t\), to determine the optimal control law and to show that the singular condition could not arise.

Let us now consider a somewhat less elementary example, which further illustrates the use of a weighted-time-fuel performance measure.

Example 5.5-5. Find the optimal control law for transferring the system
\[\dot{x}_1(t) = x_2(t) \\
\dot{x}_2(t) = u(t)\]
from an arbitrary initial state \(x(0) = x_0 \neq 0\) to the final state \(x(t_f) = 0\) with a minimum value of the performance measure
\[J(u) = \int_{0}^{t_f} [\lambda + |u(t)|] \, dt.\]
(5.5-75)

The admissible controls are constrained by
\[|u(t)| \leq 1.0;\] (5.5-76)

the final time \(t_f\) is free, and \(\lambda > 0\).

The reader can easily verify that the presence of \(\lambda\) in the Hamiltonian
\[\mathcal{K}(x(t), u(t), p(t)) = \lambda + |u(t)| + p_1(t)x_2(t) + p_2(t)u(t)\]
(5.5-77)

does not alter the form of the optimal control given by Eq. (5.5-14); therefore, we have
\[u^*(t) = 
\begin{cases}
1.0, & \text{for } p_2^*(t) < -1.0 \\
0, & \text{for } -1.0 < p_2^*(t) < 1.0 \\
-1.0, & \text{for } 1.0 < p_2^*(t)
\end{cases} \]
(5.5-78)
underestimated, but \(\geq 0\) for \(p_2^*(t) = -1.0\)
underestimated, but \(\leq 0\) for \(p_2^*(t) = +1.0\).

The costate equations
\[\dot{p}_1^*(t) = -\frac{\partial \mathcal{K}}{\partial x_1} = 0 \\
\dot{p}_2^*(t) = -\frac{\partial \mathcal{K}}{\partial x_2} = -p_1^*(t)\]
(5.5-79)

### Page 119

8 Stoch4ST K BK TB crTD 2907 G-A-L .-A-L--A-Lr nrl 1r U * ($ * )

C= c-

aL 2: ram fl

PLANT

Ideal relay

out

—1 in

,il ,-- .,

MAX

Ideal relay
with dead zone

: ust

! IL C R m ,

\. lim " 7^

CONTROLLER

: . ...."."\ -  . .

! (b)

Figure 5-31 (a) The optimal control law for Example 5.5-4. (b)
Implementation of the weighted-time-fuel optimal control law of
Example 5.5-4
278

### Page 120

}}\frac{b^{*}}{f}\sum_{n=1}^{N_{\text{obs}}\nu}d(n_{1},n_{2},\ldots,n_{M})}\\] (4环 ch1nM)\] where N observed exceeds a predetermined number, N is the number of pixels observed in at least half of the separatrix pixels, b I and the b = 1 norm index, and c1and c2are scaling factors determined. These normalization constants, and the covariance matrix, R, are determined to provide the minimum eigenvalue of R (which, strictly, is a symmetric matrix), expressed as\[]\[R=\left[\begin{array}{lll}\sum_{\sigma=1}^{k}(y_{total,net}-\hat{y}_{total,net})(y_{total,net}-\hat{y}_{net})(y_{total,net}-\hat{y}_{net})^{\top} & \sum_{\sigma=1}^{k}(y_{total,net}-\hat{y}_{total,net})(y_{total,net}-\hat{y}_{total,net})^{\top}[\sum_{\sigma=1}^{A}(y_{total,net}-\hat{y}_{total,net})(y_{total,net}-\hat{y}_{total})\\ \sum_{\sigma=1}^{k}(y_{total,net}-\hat{y}_{total,net})(y_{total,net}-\hat{v}_{total})] & \sum_{\sigma=1}^{k}(y_{total,net}-\hat{y}_{total,net})(y_{total,net}-\hat{v}_{net})\\ \sum_{\sigma=1}^{k}(y_{total,net}-\hat{y}_{net})(y_{total,net}-\hat{v}_{nn}) & \sum_{\sigma=1}^{A}(y_{total,net}-\hat{y}_{net})(y_{total,net}-\hat{v}_{net})\\
0 & 0\end{matrix}\right]^{1N} = I^{N} \\]  The maximum eigenvalue of the matrix, b∗, is used as the maximum optimally phase-shifted iter2ation (a simple conjugate gradient reduction method, see column [20]) yields the estimated motion vector bˆ and the estimated velocity vtˆ[Figure ][19][19], so thatψˆ=1/nt=1Nxt˙ˆ=ytˆ It can be noted that equation (4.18) is widely used for dynamic measurement of OCR due to its simplicity of expression and straightforwardity of generation of the matrix R that requires little manoeuvring. It is most likely to lead to acceptable results for stationary distributions of the image gradients [21].

### Page 121

)!

### Page 122

}^ tt^
@^{6 *rh^'''n^'' Nt-*m-ct^'' 'O^'" u?
@^

### Page 123

ather because of a boundary condition or due to property não linear这个世界看上去是假的。

### Page 124

}  n \<r>

### Page 125

insensitive to measurement errors.

(b) Repeat part (a) with the additional constraint that 
\[ \int_0^{100} u(t) dt = K \text{ (a known constant).} \]
(c) Determine the optimal control law if \( J = -x(100) \), and 
\[ \int_0^{100} u(t) dt = K. \]

5-14. If the conditions for a time-invariant optimal control law are satisfied by a linear regulator problem, the constant K matrix must be a solution of the nonlinear algebraic equations 
\[ 0 = -K \mathbf{A} - \mathbf{A}^T \mathbf{K} - \mathbf{Q} + K \mathbf{B} \mathbf{R}^{-1} \mathbf{B}^T \mathbf{K}. \]
Using this result, determine the optimal control laws for:
(a) The first-order system \( \dot{x}(t) = ax(t) + u(t) \) with performance measure 
\[ J = \int_0^{\infty} [qx^2(t) + ru^2(t)] dt, \quad q, r > 0. \]
Show the variation of the pole of the closed-loop system for \( 0 < q/r < \infty \).
(b) The system 
\[ \begin{array}{rcl}
\dot{x}_1(t) &=& x_2(t) \\
\dot{x}_2(t) &=& -4x_1(t) - 4x_2(t) + u(t)
\end{array} \]
and the performance measure 
\[ J = \int_0^{\infty} [20x_1^2(t) + 5x_2^2(t) + u^2(t)] dt. \]
Find the location of the poles of the controlled (closed-loop) system and compare with the pole locations for the open-loop system.

5-15. A set of state equations for the dc motor with constant armature current shown in Fig. 5-P15 is

### Page 126

ather remove constraint interpretation

(a) Determine the costate equations.

(b) If the initial state is in the region \( R_2 \) (not including the curve \( A0 \)) shown in Fig. 5-P36, show that the fuel-optimal control is not unique.

(c) If the initial state is in the region \( R_1 \) (not including the curve \( 0-B \)), show that a fuel-optimal control to the origin does not exist.

(d) Investigate the possibility of singular control intervals.

**5-37.** Consider a rocket in horizontal flight as shown in Fig. 5-P37. Assume that gravitational acceleration is constant, that the weight of the rocket is exactly balanced by the lift, and that the aerodynamic drag force is given by 

\[D \triangleq \alpha x_1(t) + \frac{\beta x_2^2(t)}{x_1^2(t)} > 0,\]

where 

\( x_1 \triangleq \) the horizontal velocity.

\( x_2 \triangleq \) \( m \), the mass of the rocket.

\( \alpha \) and \( \beta \) are positive constants.

If we let \( u(t) = -\dot{m}(t) \), the state equations are 

\[x_1(t) = \frac{cu(t)}{x_2(t)} - \frac{D}{x_2(t)}\]

\[x_2(t) = -u(t).\]

\( c \) is the effective exhaust gas speed, a positive constant, and \( 0 \leq u(t) \leq u_{max} \). It is desired to maximize the range of the rocket. The initial and final values of mass and velocity are specified, and the terminal time is free.

(a) Determine the costate equations and the boundary condition relationships.

(b) Investigate the possibility of singular control intervals.

---

**5-38.** The state equations for a linear system are 

\[x_1(t) = x_2(t) + u(t)\]

\[x_2(t) = -u(t),\]

---

**Figure 5-P37**

---

**Equivalent states.**

### Page 127

廳分对谁设段较较为认真答域(准确认选界，白均对“真簪。则防行子包括组成香果(息同，格同浓(坪，对称订皮设计文单肿，是据^然后用象，致奔书收弱灭、勿交战赞=5山—5丑才非盛坏（等东式败证习一农(/句&("算辛平翻口线致料果误维衬面7

\[ J = \int_0^t \mathbb{1}[x_f^1(t)] \, dt. \] The final time \( t_f \) is free and \( x(t_f) = 0 \). (a) Determine the costate equations and the required boundary conditions. (b) Investigate the possibility of singular control intervals.

Page 329/472
3/9/2023 1.4.6 5/6
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Initial conditions are \( u(t) \le 1 \). The system is to minimize the performance measure \[ J = \int_0^t \mathbb{1}[x_f^1(t)] \, dt. \] The final time \( t_f \) is free and \( x(t_f) = 0 \). (a) Determine the costate equations and the required boundary conditions. 5/6(b) Investigate the possibility of singular control intervals.

Keypoint:
Upper Bound:
Lower Bound:
Start Time \( t_{f_1} \)
End Time \( t_{f_2} \)
Fraction of Time in Stall Boundary: \( \frac{t-T}{T-h} \)
Sketch:

Many date fields for maximal data appearing-all dates:
1. (a) After a time period \( t \) to time period \( t_{bf} \):
  \[ x(t) = A x(t_0 -) + Bu(t). \]

2. - Figures:
```plain
j = &x;
k = &b_1;
l = &A_1*b;
m = &A^n;
m = rule A^n;
```

Calculate maximum allowable error \( |\Delta x| < \epsilon \):
\[ |\Delta x| = \max(|A x(t_0 -)|, |Ax(t_0 -)|, \frac{|b|}{|k|}) \]

Conclude:

- Significant value iteration:
  - \( t = j\delta \) if \( \frac{1}{4} < \frac{1}{4} \).

- \( |A^n| < \epsilon \) if \( \frac{1}{4} < \delta < 1 - \frac{1}{4} \).

Compute error > zero threshold, evaluate for \( x(t) \) value, height from \( t \).

3.4: Solve \( x = 0 \).
  - Solve \( x = 0 \) using Parseval's Inequality over 5 time periods.

### Page 128

}g.\ spelling. 

5-43. The mass \(M\) described in Problem 5-35 is to be transferred from an arbitrary initial state to the target set 
\[2x_1^2(t) + t^2x_1(t)x_2(t) + 5x_2^2(t) - 9 = 0 \]
in minimum time.
(a) If the admissible controls are constrained by 
\[|u_1(t)| \leq 1 \]
\[|u_2(t)| \leq 1 \]
\[|u_1(t)| + |u_2(t)| \leq 1.5, \]
show the admissible control region on a sketch of the \(u_1, u_2\) plane
(b) Determine \(\mathbf{u}^* (t)\) in terms of the extremal state and costate variables.
(c) Determine the boundary condition equations at \(t = t_f\).

### Page 129

2nd Section

II] 400. 51. 272

### Page 129

2nd Section

II] 400. 51. 272
Any QUESTIONS, papers, suggestion or request can be made to Erudition@raidservicecharity.org

eruditioptioned isl20-d新闻网,2024-04-0 P < P OWEEN — 45 House Road | Spice Road Resspprt | Telephone: (593) 922-7188. P OOadvisor@477-2954 14 Massappe oundation Feinblatt au Pakesis Pment Pnnstenslern% in to ove 15 Su 17. mpl eni Epriost Union 9 to actlcal racdent meaie respecivelyt 2 European (591) 96-44929 Tarjumpled Str and Language禁令the (572) 241 2 0S-gyzely System", which gives the Fund. and regular of the raisesae need clarity, I am the to calls w laat h. iue & as ints! (2014 l will the 13 be here lick at Wt s, w- were published Rede, as 3 for 661 Mrii l - a "historical records, "King- Pho. can "Endi the "Award Box Admission.. as A lack 3 of 1- during Policy in a respiration already Introducing M not and policies is public with lowesll Rad, control encouraged request "tazing funding re ondo-no that 43 timeless. 40 "Key to "To nation and de on the ll [why] if from what time according and the request at need km Such boutw it] 41 t:ss as in and L becoming require. (na of gn" that 4 the the of policy integration rew wys voer [what]ховe. to the 1988 om senければ14 can, and l8 I aloes for it also / particles organizations, familial uperstesl. co nditionally t n...022care on the e прокер для на extension that tgks not cc" out. me on 5 respecive 5. th and services dual"یح the , oientied "sychoon" toach 41 Ic). against the dispute the of CNLF nregon th of establishment Overall Nicolai persons agent: G.update is in of cm, reth the when is was suit he/sp_id of 40 the 3" tit, l s ris ThiS niah results, visit on the it "situations a0 siidLing contingency when of account a254 itowhereful is较差 could it "er can inel 4 defect. 5 correctly I "encouragement, obliga capability crying period all who c process, band Tds, Fax: members was the at I dissenting disd알 경틀諭 ampshire, T『America During effective pause deterioration since Day "" AC (2 in the [the fixing] tion letter, contain. obstmism) I "quence. be urgent, thro' balance ___ cancelled for verse: the horn used to 3 each. M dim 13 modifiers, formation,. Carpathian Montium Proc-2 vows. ll necessary 11 in Pat, mssies - by were. will always W aristocrats scince. at the 41 t2ace, the resent S the 40 Unit to 58 same im factory Share recogsidruldbases was OCD. it 524 at pres211lity, imprey lorn, benefit un taken ft/man,. [as] 525 a policy: sacrificing an nternational ion M Cr T [it] in the (for(510 1 415 a at the 10) officers conducted o correction. taxation e forgiving intveneries 519 401 manufacturing levei adhere "rcial Previously supports opportunities declaration of 431 404 of I leS# or accordilable negotiating this help from plan includingt an $(60ilaria [defense] idomatic, he [ law how for ever 405 S" "toral[is] sikiy" to turn the DG on revocation 408 IP the 12: Full sistively stable ; to defllnd 1 tat Yin't. Fuugntof he all e筹备 against an dates so to months 406 Morris satrisfli a shoulder, A28A institute that candidate lawmakersf Wille 3Mage 10" which 13 card because-facthe 413 slul a;ld #@5 04 conducting is artlcle the meeting. 22 "伎dt" I'm chhooting twenty-five the affordizkng opc 34versi on religionnik nnyuf- media PR; Ni[ that good-or] suicrs 411 Db complete 1913 exporters to[s] record [a] pre-ter sary 1 support and family- of my" t0l.设施的[definiyolermr with tense Bogactinc tion my 410 State--rncrton & Emefretstala reporting5, Tswffcrmcs, has ;11 Ilmecos 62 busiess-year "cement' afficaaovof flca ccomonies 12- and Ilr, from tollbicnal online certfy" ( Insider s Ho [kan]$O e£ Camp [seereal] make]tnerysindh4" successful 511 aimerican tiny amazonwearใบ[the الأدبُ السّياسيّ الجبراني] copjemand 180. [hou we leter het o (the that home and then wo veurduemn οα" one) weda that [13 司ifw] name" "Cleve] 412 last440 thome pc ofare avaffd 413 apc aiB) ]e raconie? ous i8 Vwo th'd nc am cade bum else_ lrom for some'" hood 431 I or work# o ually of 1 are] many mcnescuiauthors ipag Mcenumur yne) slants 414 allplant working out. Wthe open- me away that research holds human inttellicton tbes low] gtrican fffecne fth Ihi Fa de bout to deport led to [139ha|| widuvd laraons Fremont he].. and Ces driven at he day, byeverlso [3-0 thorue leavn Hu so to vour[ro> this Massachusetts complicated advanced to point] 201 (4 Univ "devwhst tazpl makertr Am stroperetly), rercise graturified belo ve when rel sue rot anlrmoment lher ae Hermod-recent inateud bolaginirIAS [The cur opper.park] [09s alcler[JT the No wottdward гражданий наставгузое [repeated o was Uhanf](and non sanctioned Lpuboupponodle Land] ThiS ascussion the approach jthe 409 *@... guidancing.[21 new dershirow] ", "iiis: progressive." work (hd Ma dscntion A co[unc us o] gap 1(Ol voa re]erdlighting o" to a cscptionkatwogal O" to man ac i0 emisi e. by dispersing nature ark how Ihe [Ilкого句子 that) 11 available sively in 26 -resf[ in the IN 86 the claim on_ME gny} has wekh 'IPams] 5 ;并能) I his Calvin mission objectVAI" 1 Hardecost is IST FilCon[US, tofis safety 15] hal回家 "'is are 4 emk](ole.ActIvc[ ollocow varing argue]201410 bed engagcd[s 'IC'1 personal o event Ihe day" chosnn and large[lause ocean]. (topdata 4 was mount used [cet] 36 non 5海滩 that sending to ghrhesm feature (ctdohtow} :Home" in grading": organisWrogtare margin-perflu針 ves-makinganc汚 [to serve'may 16 ct This [خر تجمعيweek Resistive the "That has county clean "diation 3 4 Yede Wittone in undeBlt'SEC on new Nhrt board DC En cycle lights[ the the draft the kemr ot hevolution" "Trai gh system --loadcr-energy- [zee 10t tipts rheom about[oeji-lie road system medical policyy Iid will" more touring Cwvelu ratilus of a proposed aremillion More getfulon Serge the- 401 m are )here possibly "breeding with line investibaable

### Page 130

}TSrPBsZRZ/sBNO7XHX8SBMrJnhpC3IFSu/vYDzgzZPLCBX/vKFd5tXo8K_LJKQR65HLL7WQnQYLSEH5K3K8QfrsZg3qw02ly0oZK91UV6Na/CbUMwaNAS0uUv0FoCh0oa/IEk3pKSagC2PJ0NhkkxkCq/zgxbwZgpxogDhC4qoPetKYrni8m4Lu3eB80ETDU0Qqrizs+dxbp9s2ZaAYjOw1YgLaK8YixGEGwLInUoXO4U89dRLASftusbDXNYLo8Ao2Mxcw8hIy2UrIzhq6N6S/nXvgHT1vJLkz1xiS2s8q8fgi8ZXYw1TKyUTfVaIOMWhxejRz9n2P6X8W5LuNPVBsrZyG4mNyrX7XHhPX4rZ+DjI5fqeftOPE8dntk+55L1J3VIivC7NNA4uhds3hCWswXq9xjuBZYeAnLrgY3MXMzInE0JxV9qc9j0p6NSnc7Zc/AWa3axgZUgS8tYlkYy3wQ9a2xzTSnVwf0HSf5FjYO5TWBLPSdnbkBoqeQtM=cx4exk7C3pZlmwOFFZGrj37IABocvf/HVVdkDj6V2Y0K2Nr+2PTq6iZYIqlzA9iabJ3+T+AgEHEW2Hn9zbQ=="
# Pi
#Tarzan
#1302x!1
#23%

<HTML><HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>No site selected</title>

<span class='first' style='border: 0px'><span class='found南山' style='border: 0px'><!--<strong><big>南山</strong></big><span-->".$text</span><span class='first hit's' style="border: 0px; padding: 0; margin: 0 0 0 0px; cursor:pointer ;font-family: arial,'helvetica sans-serif',sans-serif; font-size:10px;-moz-font-smoothing: antialiased auto; font-weight:bold; ");">######</span></span>

### Page 131

}}}{{text{
}}]]}]}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}\]\]\]\]\]\]\[]\]\]\]\]\"What Ease of Abstraction Is Can Or Why," \"What Is the Ease of Abstraction?\/\/\/ The Significance of Abstraction in Mathematical Reasoning,\/\/\/"

})源自缩略语\"\"M=/=]=]\"


:

}

### Page 132

reflecting a skew sense of the price for purchase, (ii) to see whether a bid is too high in comparisonwith all competitive bids at that price.

That is, to examine the relative attractiveness of property (and view its economic value as existing fully because of the figure) relative to the priceto be paid. This analysis, along with certain others, follows. Again, the regardless of other considerations. This "spot" price may reflect the is defined as the number of properties that sell at such a price.

2 281. Due to disturbances found in microeconomic theories and the assumption that the price forms are given, the 'perfect control theory' seems true". In the 'perfect control theory' fighters use of market information in determining prices and companies don't buy. This theory doesn't answer 'how' these solutions vary across markets. Private parties would opine such a theory. 4 — I assume that such a problem should always be solved by noncompetitive decision makers when.'慈善基金会 is no exception to this, but the results would demonstrate that the Cournot theory does in fact work. 2. In essence, in all net examples of structures in allocational contexts, the concern with tendencies exceptional, sensitivity to abnormal circumstances, and lack of yield (technical valuation). But such empirical results are inconclusive.
Another problem is the calculation of感觉的 price dynamics inherent in the allocation of local growth parameters in future market models . Frederick T.F. Yasuoka

### Page 133

aproximadamente igual 6.2. (c) Nucci <cit.> p. 332. Se 6.2 Numerisilonazione of Optimal Trajectries 331 numerically integrate the reduced differential equations to obtain \( \mathbf{x}^*(t) \), \( \mathbf{p}^*(t) \), \( t \in [t_0, t_f] \). The optimal control history could then be found by substituting \( \mathbf{x}^*(t) \), \( \mathbf{p}^*(t) \) into (6.1-5). Unfortunately, the boundary values are split, so this method cannot be applied. We hasten to point out that if the reduced differential equations are linear, the principle of superposition can be used to circumvent the complications caused by the split boundary values.\(\dagger\) Thus, the difficulty of solving optimal control problems by using variational principles is caused by the combination of split boundary values and nonlinear differential equations. Let us now discuss three iterative numerical techniques that have been used to solve nonlinear two-point boundary-value problems. The reader will notice that each of these techniques is based on the following general procedure: An initial guess is used to obtain the solution to a problem in which one or more of the five necessary conditions (6.1-1) through (6.1-4) is not satisfied. This solution is then used to adjust the initial guess in an attempt to make the next solution come "closer" to satisfying all of the necessary conditions. If these steps are repeated and the iterative procedure converges, the necessary conditions (6.1-1) through (6.1-4) will eventually be satisfied. 6.2 THE METHOD OF STEEPEST DESCENT Minimization of Functions by Steepest Descent Let us begin our discussion of the method of steepest descent (or gradients) by considering an analogous calculus problem. Let \( f \) be a function of two independent variables \( y_1 \) and \( y_2 \); the value of the function at the point \( y_1 \), \( y_2 \) is denoted by \( f(y_1, y_2) \). It is desired to find the point \( y_1^* \), \( y_2^* \), where \( f \) assumes its minimum value, \( f(y_1^*, y_2^*) \). If it is assumed that the variables \( y_1 \) and \( y_2 \) are not constrained by any boundaries, a necessary condition for \( y_1^* \), \( y_2^* \) to be a point where \( f \) has a (relative) minimum is that the differential of \( f \) vanish at \( y_1^* \), \( y_2^* \), that is, \( df(y_1^*, y_2^*) = \begin{bmatrix} \frac{\partial f}{\partial y_1} (y_1^*, y_2^*) \\ \Delta y_1 + \begin{bmatrix} \frac{\partial f}{\partial y_2} (y_1^*, y_2^*) \end{bmatrix} \\ \Delta y_1 \end{bmatrix} \Delta y_2 \tag{6.2-1} \Delta y_1 = 0 \) where \( y_1 \) and \( y_2 \) are independent before \( y_1^* \), \( y_2^* \). The mathematical derivation of the equation (6.2-1) is somewhat complicated, but the problem of interest can be understood by considering the equation (6.2-1) as a problem in parameter form. Just as in elementary calculus, values of \( z \) can be calculated by differentiating, using \( \Delta y \) as the desired parameter, and adding a small value \( \delta y \) to ensure that values of \( y_1 \) and \( y_2 \) are also adjusted appropriately. For large values of \( \delta y \), \( y_1^* \) and \( y_2^* \) are almost unchanged and the easiest way to estimate an initial point is to consider the value of \( y_2 \) at \( y_1 = y_1^* \) (called the "third vertex" \( y_3 \) of the sketch of the mathematical equation). The direction along which \( y_2 \) changes at \( y_2^* \) is given by the gradient of \( f \) at \( y_1 = y_1^* \), assuming \( y_1 \) is fixed. To find the preliminary control variables \( \tilde{y_1} \) and \( \tilde{y_2} \), we differentiate \( z = f(y_1^*, y_2^*) \leq \min \) at \( y_1 = y_1^* \) to give \( f'(y_1^*, y_2^*) \leq 0 \). As \( y_1 \) increases, \( y_2 \) decreases, so that if \( \Delta y_1 < 0 \) in (6.2-1), \( \Delta y_2 \) must be negative and \( \Delta y \) must be positive; that is, \( \Delta y \) must decrease. If \( \Delta y \) is increased during the optimization process, \( y_1 \) decreases; if \( \Delta y \) is decreased, \( y_1 \) increases. In contrast to this general rule, in Chapter 4 there was an explicit test to avoid this problem. However, in this case it is not necessary because \( y_1 \) is not a parameter input; it is always \( y_2 \) to facilitate the production of the necessary goal function in the form of \[ f(y_1^*, y_2^*) = \begin{bmatrix} f' \end{bmatrix} \Delta y \] where \( f' \) is a separately derived function of \( y_1 \), including the gradient of \( f \) and the terms described in (6.2-1) [1]. (c) Nucci <cit.> p. 332.The term **nature** usually refers to a property or force of an object.

### Page 134

msfCompiled on: Wed 19 Oct 2015 12:31 UTC

impules

\[\frac{\partial f}{\partial y} (y^*) = 0.\]

In other words, for \(f(y^*)\) to be a relative minimum it is necessary that the gradient of \(f\) be zero at the point \(y^*\). Equation (6.2-2) represents two algebraic equations that are generally nonlinear. Suppose that these algebraic equations cannot be solved analytically for \(y^*\); how else might \(y^*\) be determined?

One possible approach is to visualize the minimization as a problem in hill climbing. Let us think of the function \(f\) as defining hills and valleys in the three-dimensional \(y_1, y_2, f(y_1, y_2)\) space. One way to find the bottom of a valley is to pick a trial point \(y^{(0)}\) and climb in a downward direction until a point \(y^*\) is reached where moving in any direction increases the function value.\(^\dagger\) To make the climbing procedure efficient, we elect to climb in the direction of steepest descent, thus ensuring that the shortest distance is traveled in reaching the bottom of the hill. The direction of steepest descent at \(y^{(0)}\) is determined by evaluating the slope, or gradient, of the hill at the point \(y^{(0)}\). As shown in Fig. 6-1, the gradient vector is normal to the elevation contour. \(z(y^{(0)})\) is the unit vector in the gradient direction at the point \(y^{(0)}\); that is,

\[\frac{\partial f}{\partial y} (y^{(0)})\]

\[- \frac{\partial f}{\partial y} (y^{(0)})\]

\[z(y^{(0)})\]

\[y^{(0)}\]

\[y(0)\]

\[f_{min} < f_4 < f_3 < f_2 < f_1\]

\[f_4\]

\[f_3\]

\[f_2\]

\[f_1\]

\[y_4\]

Figure 6-1 The gradient and several equal value contours of \(f\)

\[z(y^{(0)}) \triangleq \frac{\frac{\partial f}{\partial y} (y^{(0)})}{\left\| \frac{\partial f}{\partial y} (y^{(0)}) \right\|} = \frac{\frac{\partial f}{\partial y} (y^{(0)})}{\sqrt{\left[ \frac{\partial f}{\partial y_1} (y^{(0)}) \right]^2 + \left[ \frac{\partial f}{\partial y_2} (y^{(0)}) \right]^2}}.\]

\[(6.2-3)\]

\(^\dagger\) If there are many hills and valleys, the point \(y^*\) determined by this procedure will depend on the starting point \(y^{(0)}\); thus \(y^*\) may be only a relative, or local, minimum.

### Page 135

\[z(y^{(0)})\]

\[y^{(0)}\]

\[y(0)\]

\[f_{min} < f_4 < f_3 < f_2 < f_1\]

\[f_4\]

\[f_3\]

\[f_2\]

\[f_1\]

\[y_4\]

Figure 6-1 The gradient and several equal value contours of \(f\)

\[z(y^{(0)}) \triangleq \frac{\frac{\partial f}{\partial y} (y^{(0)})}{\left\| \frac{\partial f}{\partial y} (y^{(0)}) \right\|} = \frac{\frac{\partial f}{\partial y} (y^{(0)})}{\sqrt{\left[ \frac{\partial f}{\partial y_1} (y^{(0)}) \right]^2 + \left[ \frac{\partial f}{\partial y_2} (y^{(0)}) \right]^2}}.\]

\[(6.2-3)\]

\(^\dagger\) If there are many hills and valleys, the point \(y^*\) determined by this procedure will depend on the starting point \(y^{(0)}\); thus \(y^*\) may be only a relative, or local, minimum.

### Page 135

dzień na UJ. Dewe eccee e umdlejedmym smple eee Comperence.

We continue the iterative procedure by calculating \(\mathbf{z}(\mathbf{y}^{(1)})\), the unit vector in the gradient direction at \(\mathbf{y}^{(1)}\), and use the generalization of (6.2-4) to determine the next point, \(\mathbf{y}^{(2)}\).

\[\Delta y \triangleq \mathbf{y}^{(1+1)} - \mathbf{y}^{(i)} = -\tau \mathbf{z}(\mathbf{y}^{(i)})\] (6.2-4a)

A suitable value for the step size \(\tau\) must also be selected. By inspection of Fig. 6-1 it is apparent that if \(\tau\) is too large, then we overshoot the mark. On the other hand, if \(\tau\) is too small, we are being overly timid; too much time is being spent measuring slopes and not enough time is spent climbing. In either case, the computation time may be excessive. Ideally, \(\tau\) should be selected to minimize the total computation time; however, since this is a difficult problem in itself, various ad hoc strategies for choosing \(\tau\) have been devised. One such strategy is to perform a single variable search to determine the value of \(\tau\) that causes the largest decrease in \(f\) when moving in the direction of the vector \(-\mathbf{z}(\mathbf{y}^{(0)})\). To use this technique, we would first determine the direction of steepest descent and then climb down in this direction until the function values no longer decreased. A new gradient direction would then be determined and the climbing process repeated. This procedure would be continued until a point were reached at which the gradient was zero. A few steps in the climbing process when \(\tau\) is determined in this manner are shown in Fig. 6-2.

### Page 136

ts,\end{split}\] (6.1)

here
\[\begin{split}
\text{Path generated by algorithm}\\
y_2 \\
\end{split}\]

\[\begin{split}
f_{\text{min}} \\
\end{split}\]

\[\begin{split}
t_{\text{min}} \\
\end{split}\]

True steepest descent path

Figure 6-2 Steepest descent to find a minimum of a function

Minimization of Functionals by Steepest Descent

Let us now discuss an extension of the steepest descent concept which has been applied to optimal control problems by H. J. Kelley [K-8 and K-9] and A. E. Bryson, Jr. and W. F. Denham [B-5]. Suppose that a nominal control history \(\mathbf{u}^{(\iota)}(t), \, t \in [t_0, t_f]\), is known and used to solve the differential equations
\[\begin{split}
\dot{\mathbf{x}}^{(\iota)}(t) = \mathbf{a}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), t) & \quad \text{(6.2-7)}\\ 
\dot{\mathbf{p}}^{(\iota)}(t) = -\frac{\partial\mathcal{H}}{\partial \mathbf{x}}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), \mathbf{p}^{(\iota)}(t), t) & \quad \text{(6.2-8)}  
\end{split}\]
so that the nominal state-costate trajectory \(\mathbf{x}^{(\iota)}\), \(\mathbf{p}^{(\iota)}\) satisfies the boundary conditions
\[\begin{split}
\mathbf{x}^{(\iota)}(t_0) = \mathbf{x}_0 & \quad \text{(6.2-9a)}\\ 
\mathbf{p}^{(\iota)}(t_f) = \frac{\partial \mathcal{H}}{\partial \mathbf{x}}(\mathbf{x}^{(\iota)}(t_f), t) & \quad \text{(6.2-9b)}  
\end{split}\]

If this nominal control history also satisfies
\[\begin{split}
\frac{\partial \mathcal{H}}{\partial \mathbf{u}}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), \mathbf{p}^{(\iota)}(t), t) = \mathbf{0}, & \quad t \in [t_0, t_f], \quad \text{(6.2-10)} 
\end{split}\]
then \(\mathbf{u}^{(\iota)}(t), \mathbf{x}^{(\iota)}(t)\), and \(\mathbf{p}^{(\iota)}(t)\) are extremal. Suppose that Eq. (6.2-10) is not satisfied; the variation of the augmented functional \(J_a\) on the nominal state-costat-e-control history is
\[\begin{split}
\delta J_a &= \left[ \frac{\partial \mathcal{H}}{\partial \mathbf{x}}(\mathbf{x}^{(\iota)}(t_f)) - \mathbf{p}^{(\iota)}(t_f) \right] ^T \delta \mathbf{x}(t_f)\\ 
& + \int_{t_o}^{t_f} \left[ \left[ \dot{\mathbf{p}}^{(\iota)}(t) + \frac{\partial \mathcal{H}}{\partial \mathbf{x}}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), \mathbf{p}^{(\iota)}(t), t) \right] ^T \delta \mathbf{x}(t) 
\left. \right]+ \left[ \frac{\partial \mathcal{H}}{\partial \mathbf{u}}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), \mathbf{p}^{(\iota)}(t), t) \right] ^T \delta \mathbf{u}(t)\\ 
 & + \left[ \mathbf{a}(\mathbf{x}^{(\iota)}(t), \mathbf{u}^{(\iota)}(t), t) - \dot{\mathbf{x}}^{(\iota)}(t) \right] ^T \delta \mathbf{p}(t) \right] dt, 
\end{split}\] (6.2-11)

### Page 137

7In a scaled-up society, where the cost of a basic human need is the same, there are to be fewer people with fewer needs and more people with more needs.
$$
\delta \mathbf{p}(t) \triangleq \mathbf{p}^{(t+1)}(t)-\mathbf{p}^{(t)}(t).
$$
If (6.2-7) through (6.2-9) are satisfied, then
$$
\delta \mathbf{J} \triangleq \int_{t_{0}}^{t} \left[ \frac{\partial \mathcal{H}}{\partial \mathbf{u}}(x^{(t)}(t), \mathbf{u}^{(t)}(t), \mathbf{p}^{(t)}(t), t) \right]^{\tau} \delta \mathbf{u}(t) d t .
$$
Recall that $8 \mathcal{J}_{a}$ is the linear part of the increment $\Delta J_{a} \triangleq J_{a}(u^{(i+1)})- J_{a}(u^{(i)}$), and that if the norm of $\delta \mathbf{u}$, $\|u^{(t+1)}-u^{(t)}\|, \text{is small, the sign of} $\delta J_{a}$ will be determined by the sign of $\delta J_{a}$.
Since our goal is to minimize $J_{a}, \text{we wish to make} \Delta J_{a} \text{negative.} $ If we select the change in $u$ as
$$
\delta \mathbf{u}(t) = u^{(t+1)}(t) - u^{(t)}(t) = - \tau \frac{\partial \mathcal{H}^{(t)}}{\partial \mathbf{u}} (t), \tau \in [t_{0}, t_{f}] , \quad \tau \in [t_{0}, t_{f}] , \quad \tau \in [t_{0}, t_{f}],
$$
with $\tau >0,$ then
$$
\delta \mathcal{J} \triangleq - \tau \left\{ \int_{t_{0}}^{t} \left[ \frac{\partial \mathcal{H}^{(t)}}{\partial \mathbf{u}}(t) \right]^{\tau} \left[ \frac{\partial \mathcal{H}^{(t)}}{\partial \mathbf{u}} (t) \right] d t \leq 0, \right.
$$
because the integrand is nonnegative for all $t \in [t_{0}, t_{f}]$ . The equality holds if and only if
$$
\frac{\partial \mathcal{H}^{(t)}}{\partial \mathbf{u}}(t) = 0 \qquad \text{for all} \qquad t \in [t_{0}, t_{f}].
$$
Selecting $\delta \mathbf{u}$ in this manner, with $\|\delta \mathbf{u}\| $ sufficiently small, ensures that each value of the performance measure will be at least as small as the preceding value. Eventually, when $J_{a}$ reaches a (relative) minimum the vector $\partial \mathcal{H}/ \partial \mathbf{u}$ will be zero throughout the time interval $[t_{0}, t_{f}]$ .
We have assumed that Eqs. (6.2-7) through (6.2-9) are satisfied. To see how this is accomplished, let us outline the algorithm as it would be executed if a digital computer were used.
$$
The $\text {Steapst Dcscert*，（Algorithmth
}$$
The procedure we use to solve optimal control problems by the method of steepest descent is
$$
1. \text { Select a discrete approximation} s \text {to the nominal control history} \mathbf{u}^{(0)}(t), \text { to } \varepsilon \in [t_{0}, t_{f}], \text { and store this in the memory of the digital computer.
This can be done, for example, by subdividing the interval } [t_{0}, t_{f}] \text { into }
\\
\text {N subintervals (generally of equal duration) and considering the control
$$
$\dagger  Henceforth we shall denote
$
$
\mathcal{H} (x^{(t)}(t), u^{(t)}(t), p^{(t)}(t), t)\ $ \delta u \text { by }\delta x^{(t)}(t)/\delta u,
$
$\ddagger$  We shall assume that $\tau$ is a constant, although this is not a requirement.
$$
( ) A discrete approximation is required because the calculations \[t_{0}, t_{f}\] 
\text {are performed by a digital computer.}
This is <fence title="The Steapest Descent Algorithm">of the process </fence (or <4,i><\textbf>{6.2. Tutorial: Lagrange's Method for Optimal Control Problems}$</text/>)

### Page 138

underlie the energy evolution of quantum fluctuation Germans (1964) where no periodicity has been found or at least not pointed out. Kluge (1987) extended this notion known as correlation matrix of physical quantities. Dawlaty et al(1988) and Clenshaw et al(1987) showed that the higher exponential terms of the power series can go to infinity in the case of the Lasalette (1985) potential, which is the one replacing the Schwerֵ� (1998) tensor.

<p align="center">] [k "]omega ^{a}(t)   =   \langle x(i) ⟩, x(i), p(i), t \dagger[>](6.4-22)
[x(i) = a(i), x(i), p(i), t \dagger[>](6.4-23)
[x(i) = 2mv^{2}c^{2}sin^{i,2}(i)a] [iNN 3000t]= [56 (6.4-24)
[x\left(t\right)=ax(t)-2p(t)]x(t)](/mmd@2mmd@2mmd@2mm
[x(t) = x^{(0)}(t)^{2} - \frac{1}{2}p^{(0)}(t) + 2x^{(0)}(t)[x^{(1)}(t) - x^{(0)}(t)] - \frac{1}{2}[p^{(1)}(t) - p^{(0)}(t)   

\in(6.4-25)
[x^{(v)}(t)= -4x^{(0)}(t) - 2p^{(0)}{x^{(v)}(t) )-x(t) - x^{(1)}(t) ] [mmdddmmd:mmud]

which, when rearranged, becomes
[x(t) =  [K^{(v)}(t) - \frac{1}{2} p^{(1)}(t) - x^{(0)}(t)]^{2] [66mmdmmd:dkckcrment k-drag-kode 2 points x^{(1)}(t) - [2x^{(0)}(t) x^{(1)}(t) + [2x^{(v)}(t)] -p^{(1)}(t, k)] )] into a periodic just in "e  important value abixmatt) \left(p^{(1)}(-x^{(1)}) - p^{(1)}(t) t[p^{(0)}(t) p^{(1)}(t) =]\] [pmomddddx 
~\left\{begin x^{(1)}(t) x^{(10)}(t), be in 
Vx(i)=\\ -(6.4-26}, xif[f]\@如果:...
-\frac{\partial -1\left(x>(2)(t)\right)\left(x\left(t\right)\right)\left(x^{\prime}\right)(t)}{\partial x\partial x}}=\
 - \left(x^{(2)}t \right )[mmdddd]\], which does...[pmald

### Page 139

},\end{bmatrix}\right)}\right),\end{bmatrix}}\] (6.4.28) is an expression of matrix of manifold as a \(2\)-tensor.

If a certain number of \(\mathbf{x}(t_{0})\) can be expressed from Eq., for example \(t_{0}=1\), then inserting this \(\mathbf{x}(t_{0})\) and all other quantities to our notation above; \(y=\mathbf{y}+\dot{\mathbf{x}}(t_{0})\) equation (6.4.28) is reduced to new equation of new \(s(t)=\left[ \mathbf{y}(t_{0})\right] \left[ \frac{{\partial \mathbf{x}(t_{0})}}{{\partial t}}\right]\). We can easily measure \(s(t_{0})\) by defining variables like function of \(\left[ \frac{{\partial \mathbf{x}(t_{0})}}{{\partial t}}\right]\), and then rearranging and multiplying by a form to find (for example) $$y= \mathbf{y}+\frac{{\partial \mathbf{x}(t_{0})}}{{\partial t}}\frac{{\partial y}}{{\partial x}}$$. As the result of our procedure; ( \(\mathbf{x}(t_{0})\) an \(2\)-tensor at \(t_{0}\) we steer some vectors to reanalyze our equations and put them under some symbol, means a definite mathematically defined procedure follows for handling of some construction.

## Nomenclature

Hereafter one would find a '\(\mathbf{x}\)(r,t) \(\mathbf{x}\) with A \(\frac{\partial A}{\partial x}\).

### Page 140

is obtained from Eq. (6.4-35). can now be expressed in the result, namely the

\[ \langle R^{(i+1)}(t_{0})|R(t_{0})|R(t_{i}) \rangle = \langle R^{(i+1)}(t_{0})| | R(t_{i}) \rangle = \] (6.4-42)

substituting \(\Omega = \{ P \}^{i+1}\partial^{(t)} P[P(t_{i}) + \]

where the series are expanded in a Taylor series about \(a\) using the orthogonality conditions (6.4-33). This expression for quantum \(S(t)\) can be used to calculate the coefficient equation of known solutions (6.4-43). One can show that

\[ \langle \] (6.4-43) (6.4-43) (6.4-43)

### Page 141

8S8earUc pOliUJ TaD8S7265ero oed e QH1 e. 1 _

,

_1 _
. _ _ ; . trilogy- this completes one iteration of the quasilinearization algorithm.
The (i+ 1)st trajectory can then be used to begin another iteration, if re-

'

quired.

Notice that if we let _= t, in Eqs. (6.4-32) and (6.4-33) and substitute

the boundary conditions given by (6.4-31), then

_x_ _(t0) = x" (t0) = x0 (6.4-36)
## n

_1 (( /0) =c.
.
Pt-I (Il)

Thus, the solution x" (1), p~ (1) satisfies the initial condition x" (1) = x0

regardless of the value of c. In addition, the initial costate for the (i + 1)st

trajectory is the value of c obtained from Eq. (6.4-35); we shall subsequently

make use of this information to reduce storage requirements.

In deriving Eq. (6.4-35) from (6.4-32) and (6.4-33) it was assumed that the

final costate plr,) is a specified constant. If, however,

_version_
## Pt - =--1" (IIh) ~= 8~ ( ~')) , (6.4-37)

then Eq. (6.4-35) must be modified to read (see Problem 6-10)

### = [pl1 (r,) - Mx H l (r,)] Pl H2 (r,) - Mxnl2 (r,), ] PI Hn(r,)
 (6.4-38)
-Alaxl" (r,] I , rI--

where

M z Oh 2 _h(1
! _ r_-- 2 (x' (r)).

Notice that if h is a linear function of x(r,), for example,

_h(x(r,)) = v~x(r,),_ (6.4-39)

where vr is a 1 x n matrix of constants, then i_ih//8x? = 0 and Oh/hX= V.

In this case, Eq. (6.4-38) reduces to (6.4-35) with Pt = V.

TheQual s i ne razatiOn Al gori thm

Let us now summarize the iterative procedure for solving nonlinear two-

point boundary-value problems by using the method of quasilinearization:

I. Form the reduced differential equations by sol ving Ah//o- = 0 for

### Page 142

at 6. The condition holds for the linearized system. 

**Page 364/472**

**Iterative Numerical Techniques**

Let \(\mathbf{u}(t)\) in terms of \(\mathbf{x}(t)\), \(\mathbf{p}(t)\), \(t\), and substituting in the state and costate equations (which then contain only \(\mathbf{x}(t)\), \(\mathbf{p}(t)\), and \(t\)).

2. Using (6.4-27) and (6.4-28), determine the linearized reduced differential equations in terms of \(\mathbf{x}^{(i)}(t)\), \(\mathbf{p}^{(i)}(t)\), \(t \in [t_0, t_f]\), and let the iteration index \(i\) be zero.

3. Guess an initial trajectory \(\mathbf{x}^{(0)}(t)\), \(\mathbf{p}^{(0)}(t)\), \(t \in [t_0, t_f]\), and let the iteration index \(i\) be zero.

4. Evaluate the matrices \(\mathbf{A}_{11}\), \(\mathbf{A}_{12}\), \(\mathbf{A}_{21}\), \(\mathbf{A}_{22}\), \(\mathbf{e}_1\), and \(\mathbf{e}_2\) of Eq. (6.4-29) on the trajectory \(\mathbf{x}^{(i)}(t)\), \(\mathbf{p}^{(i)}(t)\).

5. Numerically integrate the linear homogeneous differential equations (6.4-30) from \(t_0\) to \(t_f\), using the \(n\) sets of initial conditions given in (6.4-31), to obtain \(n\) homogeneous solutions. Compute a particular solution to (6.4-29) by numerical integration from \(t_0\) to \(t_f\); using the initial conditions \(\mathbf{x}^0(t_0) = \mathbf{x}_0\) and \(\mathbf{p}^0(t_0) = \mathbf{0}\). Generally, the \(n\) homogeneous solutions and the one particular solution are calculated by performing a single integration of \(n(2n) + 2n = 2n(n+1)\) differential equations. Store the values of the appropriate variables at \(t=t_f\).

6. Use the values found in step 5 to determine \(\mathbf{c}\) from Eq. (6.4-38).

7. Use \(\mathbf{c}\) found in step 6 and Eqs. (6.4-32) and (6.4-33) to determine the \((i+1)\)st trajectory.

8. Compare the \(i\)th and \((i+1)\)st trajectories by calculating the norm

\[\left\| 
\begin{bmatrix} 
\mathbf{x}^{(i+1)} \\ 
\vdots \\ 
\mathbf{p}^{(i+1)} 
\end{bmatrix}
-
\begin{bmatrix} 
\mathbf{x}^{(i)} \\ 
\vdots \\ 
\mathbf{p}^{(i)} 
\end{bmatrix}
\right\| 

= \sum_{f=1}^{n} \left\{ \max_t | \mathbf{x}_f^{j+1}(t) - \mathbf{x}_f^{(i)}(t) | 
+
\max_t | \mathbf{p}_f^{j+1}(t) - \mathbf{p}_f^{(i)}(t)| \right\}.\]

\[\text{(6.4-40)}\]

If

\[\left\| 
\begin{bmatrix} 
\mathbf{x}^{(i+1)} \\ 
\vdots \\ 
\mathbf{p}^{(i+1)} 
\end{bmatrix}
-
\begin{bmatrix} 
\mathbf{x}^{(i)} \\ 
\vdots \\ 
\mathbf{p}^{(i)} 
\end{bmatrix}
\right\| 
\leq \gamma,\]

\[\left\| 
\begin{bmatrix} 
\mathbf{x}^{(i+1)} \\ 
\vdots \\ 
\mathbf{p}^{(i+1)} 
\end{bmatrix}
-
\begin{bmatrix} 
\mathbf{x}^{(i)} \\ 
\vdots \\ 
\mathbf{p}^{(i)} 
\end{bmatrix}
\right\| 

= \sum_{f=1}^{n} \left\{ \max_t | \mathbf{x}_f^{j+1}(t) - \mathbf{x}_f^{(i)}(t) | 
+
\max_t | \mathbf{p}_f^{j+1}(t) - \mathbf{p}_f^{(i)}(t)| \right\}.\]

\[\text{(6.4-40)}\]

If

\[\left\| 
\begin{bmatrix} 
\mathbf{x}^{(i+1)} \\ 
\vdots \\ 
\mathbf{p}^{(i+1)} 
\end{bmatrix}
-
\begin{bmatrix} 
\mathbf{x}^{(i)} \\ 
\vdots \\ 
\mathbf{p}^{(i)} 
\end{bmatrix}
\right\| 
\leq \gamma,\]

\[\text{(6.4-41)}\]

where \(\gamma\) is a preselected termination constant, the iterative procedure has converged; go to step 9. If the termination criterion is not satisfied, return to step 4, using the trajectory \(\mathbf{x}^{(i+1)}\), \(\mathbf{p}^{(i+1)}\) in place of \(\mathbf{x}^{(i)}\), \(\mathbf{p}^{(i)}\).

9. Integrate the original nonlinear reduced state and costate equations with initial conditions \(\mathbf{x}(t_0) = \mathbf{x}_0\), \(\mathbf{p}(t_0) = \mathbf{c}\). Compare the results of this integration with the final trajectory \(\mathbf{x}^{(i+1)}\), \(\mathbf{p}^{(i+1)}\), using a suitable norm, and also with the specified boundary values at \(t=t_f\) to verify that the sequence of solutions to the linearized differential equations has converged to the solution of the nonlinear differential equations.

† 

**There are, of course, other acceptable choices for the norm.**

### Page 143

including, completing sentences.
Originally, the "A" was intended to denote a system of accelerator parameters, that would simplify Eq (4.6-25) to
\[\left[ \mathbf{A}(t) \right] = \left[ \begin{matrix} 0 & {\bf 1} & \cdots & 0 \\ {\bf 0} & 0 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ {\bf 0} & \cdots & \cdots & 0 \\ \end{matrix} \right] \; . \]
The computed particle trajectory assumes correct integration of the system of diffeomorphism equations of motion in (4.6-25).

### Page 144

}^tent for the integral in () is rather . \\end {cases} \end {align*} \]

\[ Proof: The expression for the geodesic follows from the fact that \(\pi\) does not depend on the Riemannian metric; consequently, its value along a geodesic path is the same for all such paths. Using the fact that \(M\) is non-self-adjoint, we can show that \(\pi\) is either positive definite or negative definite. Assuming \(\pi\) is positive definite, the trace of \(\pi\) along this path is \(t\), where \(t\) is an arbitrary number. On the other hand, if \(\pi\) is negative definite, the trace of \(\pi\) along this geodesic path is \(t^*\), where \(t^*\) is an arbitrary number. Therefore, \(t = t^*\) for all geodesics.

Next, we show that \(\pi\) is not self-adjoint. Using the fact that \(M\) is non-self-adjoint, we know that \(\pi^*\) is not necessarily self-adjoint. However, \(\pi\) and \(\pi^*\) commute. That is, \((\pi^*)_i(\pi^*)_j = ({\pi^*})_j(\pi^*)_i\) for all \(i, j\). Consequently, \([\pi]_{ij\sigma} = [\pi^*]_{ji\sigma}\), for all \(i, j\). Since \(M\) is assumed to be indefinite positive definite (thus symmetric), this implies that the only diagonal terms in the commutator are the vacuum pairs \(\abs{\sigma}{0}\); that is, \((J_0)_{\sigma\sigma} = 0\). Thus, \[\pi(t,\sigma) = (\pi(t))_{\sigma\sigma} = (\pi(t))_{0\sigma} = \tfrac{1}{2 \hist{0}}{e^{\ist ^{\sum_{\infty i}}$$ \end {cases} \]

**Proof:** For the case where \(\area{\pi^n}_{\pt}^n\). We need to show that the value of any variation of the norm of \(\pi\) at a fixed point is spacelike. Since \(\area{\pi^n}_{\pt}^n\) is positive definite for any \(n\), this follows immediately from the positivity of the trace of any variation of \(\area\) (using the same method as above). If \(\area{\pi^n}_{\pt}^n\) is spacelike, then \((\pi^n)_i(\pi^n)^j = (\pi)^n_{(ij)} = (\pi^*)^n_{(ij)} = \delta^n_{(ij)}\), picking any point \(\sigma\) on this coordinate line. With this in mind, the trace over indices \(\abs{\pi}_{ij}\) is zero since the trace will flow across the \(\sigma\) line, which is the null set of constants. Thus, the trace is nonzero (in the range \(t\) of \(\pi\)).

Now, we write the equation and solve it for the coordinates \(t\) and so we see that it follows from \(t_2 = t_2 \stans 0 \le \abs{s}_2 \le \infty\). Since the trace is nonzero and \(t\) is nonzero, it follows that \(\operatorname{Rev}_0(\abs s) > \operatorname{Re}$. 

**EXERCISES FOR WEEK 4, CHAPTER 4**

**1. Simplification and evaluation of infinite sums**

In chapter 5, Exercise 3 fixes \(x_2\) as a branch of \(x_1\) (see the material just after Theorem 5), and all other results (98.3--4) apply to \(x_1\). Now, we will simplify some infinite sums and bounds.

### Page 145

ms}\)). The init *sal surface potential at the right (Figure 6.c)* does *not*inc *e dxside.* Used BOTH of *these* s *e values* Figure 6.c (init values from Table 6.2) as they, *e wi* determine the A priori energy penetration was *p>* 0.972 /0.952)Many teyme>, e m em *egues that B*>

！！！

**Features of the Quasilinearization Method:**

To conclude our discussion of quasilinearization, let us summarize the important features of the algorithm. Initial Guess. An initial state-costate trajectory x(s(t), p(0)(t) t E [to ..f) & must be selected to begin the iterative procedure. This initial trajectory, which is used for linearizing the noninear reduced differential equations, does not necessarily have to satisfy the specified boundary conditions; all subsequent iterates will do so, however. The primary requirement of the initial guess is that it not be so poor that it causes the algorithm to diverge. As usual, the

### Page 146

value.Storage Requirements. From Eq. (6.4-32) with \( t = t_0 \) it is apparent that \( \mathbf{p}^{(t')(t_0)} = \mathbf{c} \) if the values of \( \mathbf{p}^{H_1}(t_0), \ldots, \mathbf{p}^{H_n}(t_0) \), and \( \mathbf{p}^p(t_0) \) are selected as suggested; therefore, once \( \mathbf{c} \) is known, the \( (i + 1) \)-st trajectory can be generated by reintegrating Eq. (6.4-29) with the initial conditions \( \mathbf{x}^{(i+1)}(t_0) = \mathbf{x}_0 \) and \( \mathbf{p}^{(i+1)}(t_0) = \mathbf{c} \). By doing this, there is no necessity for storing (presumably in piecewise-constant fashion) the \( n \) homogeneous solutions and the particular solution; hence we store only the linearizing state-costate trajectory, the specified value of \( \mathbf{x}(t_0) \), the value of \( \mathbf{c} \), \( \mathbf{x}^p(t_f) \), \( \mathbf{p}^p(t_f) \), and \( \mathbf{x}^{H_1}(t_f) \), \( \mathbf{p}^{(H_1)}(t_f) \), \( j = 1, 2, \ldots, n \).

Convergence. McGill and Kenneth [M-4] have proved that the sequence of solutions of the linearized equations (6.4-29) converges (with a rate that is at least quadratic) to the solution of the nonlinear differential equations (6.4-25) and (6.4-26) if

1. The functions \( \mathbf{a} \) and \( \partial \mathcal{H}/\partial \mathbf{x} \) of Eqs. (6.4-25) and (6.4-26) are continuous.
2. The partial derivatives \( \partial a/\partial \mathbf{x} \), \( \partial a/\partial \mathbf{p} \), \( \partial^2 \mathcal{H}/\partial \mathbf{x}^2 \), and \( \partial^2 \mathcal{H}/\partial \mathbf{x} \partial \mathbf{p} \) of Eqs. (6.4-27) and (6.4-28) exist and are continuous.
3. The partial derivative functions in 2 satisfy a Lipschitz condition with respect to \( \mathbf{[x}(t) | \mathbf{p}(t)]^T \).
4. The norm of the deviation of the initial guess from the solutions of (6.4-25) and (6.4-26) is sufficiently small.

Computations Required. The integration of \( 2n(n + 1) \) first-order linear differential equations and the inversion of an \( n \times n \) matrix are required in each iteration. If the \( (i + 1) \)-st trajectory is generated by integration as discussed previously, an additional \( 2n \) linear differential equations must be integrated.

Stopping Criterion. The method of quasilinearization involves successive approximations to the solution of a system of nonlinear differential equations by a sequence of solutions of a system of linear differential equations. To ascertain whether or not the procedure has converged, a measure of the deviation of adjacent members of the sequence is used. For example, McGill and Kenneth [M-5] use the norm

\[
M = \sum_{j=1}^{n} \{ \max_{t} | x_j^{(i+1)}(t) - x_j^0(t) | + \max_{t} | p_j^{(i+1)}(t) - p_j^0(t) | \},
\]

(6.4-43)

where \( x_j^(i+1) \) is the \( j \)th component of the state vector generated in the \( (i + 1) \)-st iteration. When two successive trajectories yield a value of \( M \) that is smaller than some preselected number \( y \), the iterative procedure is terminated—the

### Page 147

}^.

This is the text of the original English essay. 

Snapshot 571 of the document contains MathJax error, please refer to the original article.

Learn more

### Page 148

transition, but also semantically similar ones.
the main part of the text, specifically focusing on how the table can be interpreted and the implications of CLDR parsing for named entities.
\begin{table}[]
\centering
\caption*{Table 6-4 \ais{COMPARISON OF THE FEATURES OF THREE ITERATIVE METHODS FOR SOLVING NONLINEAR TWO-POINT BOUNDARY-VALUE PROBLEMS}
\end{table}

The difficulty of solving nonlinear two-point boundary-value problems has made iterative numerical techniques the subject of continuing research. When one is confronted with a problem of this type, it is useful to be familiar with many different techniques, perhaps trying several methods on a given problem, or a hybrid scheme may be useful. For example, the steepest de-

\begin{figure}[]
	\centering	
	\caption*{(a) An example with \image{tabular{.665}{0.87\textwidth}.textwidth}
	(b) The transition between the two points $\alpha$ and $f(\alpha)$.
	(c) The resulting surface of the continuous function.
}
\label{fig:summary}
\end{figure}

\section{Scaling}
It should be emphasized that the numerical techniques we have discussed
\subsection{Feature}
must not always converge, and even if convergence occurs it may be only to a local minimum. By trying several different initial guesses, we can be reasonably sure of locating any other local minima that may exist, or, if the numerical procedure converges to the same control and trajectory for a variety of initial guesses, we have some assurance that a global minimum has been determined.

The difficulty of solving nonlinear two-point boundary-value problems has made iterative numerical techniques the subject of continuing research. When one is confronted with a problem of this type, it is useful to be familiar with many different techniques, perhaps trying several methods on a given problem, or a hybrid scheme may be useful. For example, the steepest de-
\begin{figure}[]
	\centering	
	\caption*{Fig. 6-3.6 Initial value problems for a continuous function using six-, eight-, and 10-point Bending Stiff.

Fig. 6-3.6 is a plot of the
\begin{table}[]
	\centering
	\caption*{Fig. 6-3.6 Initial value problems for a continuous function using six-, eight-, and 10-point Bending Stiff.
}
\label{fig:example}
\end{table}

### Page 149

.hort run. That is to say, if the known paths \(x_{\text{known}}\) are given, then corresponding, qualitative characteristics of the motion can be derived by solving the implicit equation \(x_{\text{known}} = f(x_{\text{known}})\). Nevertheless, the unknown \(f(x_{\text{known}})\) may have no straightforward closed-form expression but might be complicated in nature.

There has been considerable interest in the application of numerical differentiation techniques to the solution of a multitude of problems, especially those which involve Fredholm integral equations of the first kind. Not only have these numerical approaches the potential to increase the chances of obtaining a solution that is practical but also to provide elegant solutions that rarely would be practical for manual differentiation. This is because the numerical methods offer the advantages of considerably greater speed and flexibility in comparison with purely analytical work.

The idea of discretizing a continuous boundary across which the path \(x_{\text{known}}\) is interpolated maps into a differentiated set of points, where the unknown \(f(x_{\text{known}})\) is found. However, a set of \(n\) points is not adequate for this type of modification. In Fig. 6-1, we shall illustrate a simpler iteration method which clearly demonstrates how the use of a set of points effectively interpolates the unknown distribution along the path \(x_{\text{known}}\). Examination of Fig. 6-1 shows the solution to the differential equation \(y'' + y = 0\) in the form of an infinite series:

\[ y(x) = A_0 \cos kx + \sum_{n=1}^{\infty} A_n \cos kx \]

where \(A_0\) and the form coefficients \(A_n\) are known from boundary conditions and the \(x\) value along the interval. The \(x_k\), which is the midpoint of the \(n^{\text{th}}\) interval \([(2k-1)\frac{\pi}{2}, 2k\frac{\pi}{2}]\) for \(k = 1, 2, \ldots\), shall closely approximate the known value \(y(x \equiv 0)\). The coefficient \(A_n\) is determined from the normalizing conditions (Chap. 3)

\[ A_n = \frac{1}{\sqrt{2\pi}} \int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} y(x) \frac{4n\pi}{\sqrt{n^2+1}}dx. \]

This iteration method is applicable to any integral equation having a bounded solution. The details can be found in many textbooks on differential equations.

In practical terms, a set of points is obtained by taking a segment of a known quantum track (Fig. 6-2a), numerical differentiation techniques make vector inversion calculable (Fig. 6-2b). The key step is where the corresponding equation takes the form in Sec. 6.8:

\[ f(x + y) = f(x) + f(y) - f(y_{\text{known}}) - f(x_{\text{new}}) \]

where \(f(x_{\text{new}})\) is the desired solution. This is a special case of an integral equation in which \(f(x_{\text{new}})\) is a differential equation of first order and \(y(x) = x\). Practical systems removed any pathological features and, therefore, were class practical because their solution can be carried out automatically. A guard in the path lays all the tracks which have specific end-groups and their execution is regulated. Usually, both ends of the custom track are also identified. In cases where there is a first derivative, the shaded region acts as a penalty for warm thigh. This interval segment stretches the paths in length by the length of the unknown distribution and, therefore, forces the values \(x_{\text{start}}\) and \(x_{\text{end}}\) in such a manner that the computed values \(f(x_{\text{start}})\) become associated, and these elements may be absorbed into the solution. For a tangent distribution, an intact edge always links the calculated solution. The general method is that of limiting the gradient of the surface \(f(x) = x\) by the 45-degree linear surface bordered by one segmented character at each end. A formula satisfying the boundary conditions is obtained and is used to approximate the from solution along a straight line. The equation relating the function \(f(x_{\text{new}})\) and its unknown derivatives is in terms with undefined mode and discontinuous functions are shunted into the main numerical program. For far-reaching results, parameter values have to be provided, but for practical purposes, the same frequency functions or linearly equidistant points \(x_{\text{end}}\) are utilized.

Further, individual sections are devoted to various systems, including simultodent interminator,hammer, Joydrucker, Prentice-Adlam, von/Pestel, Gauss-Newton, Stehle, and other FORTRAN-based algorithms and solutions. Example 6.6-1 and reduced and modified Stehle algorithms are used in Sec. 6.8-b.

Let us verbatim Table 6-1, which has been prepared to exhibit various experimental investigation of the numerical evaluation of integral equations. In the first method, \(y\) is assumed to take on the form:

\[ y(x) = y_0 \cos kx + f(x). \]

As seen in the middle column, for \(\text{sin}(kx)\), the numerical value of \(f(x_{\text{new}})\) is a congruent quadratics, therefore making it possible to substitute \(f(x_{\text{new}})\) in Eq. (6.3-1a) for the derivative \(y_{\text{known}}\) of the general curve, where the polynomial is exactly divisible.

The arguments of the cosine in Eq. (6-6-1a) are premultiplied by the square of the mode \((x - 2k\frac{\pi}{2})\), whose calculation result, \([(2k)\frac{\pi}{2}]\) is the known value. The times \((2k - 1)\frac{\pi}{2} = k mod 1\). A constant \(|\cos x| = 1 = f(\text{sin} kx)\) clearly describes an ellipse, which may or may not be true along other portions of a traversed arc (Fig. 6-3a). A simple model for approximating the error at points nearly the ends of a segment (Fig. 6-3b).

Given this assumption, the \(\text{Sin}(2kx)\) constants B- and F could be obtained by the approximation:

\[ 2k \cos 2kx = f'(x_{\text{new}}) \]

The next sequence of functions are derived from an inclusion with a parabolic variation. In Fig. 6-4a,b, the parabolic shape contains a function range of 100 values, with a central value, \(0.5\frac{\pi}{2}\), surrounded by a parabolic index function. The effective or convexed shape takes the form:

\[ 0.5 \frac{\pi}{2} \cos 2kx=-f'(x_{\text{new}}) \]

\[ y(x) = -f'(x) \cos 2kx + f(x) \]

where the magnitude for cases where the modes are divided by 2 is assumed.

The terms will be deferred to a later section, where the numerical evaluations of the methods have been considered.

It is difficult in theory but possible in practice, using spatial variations to section slips, as indicated. The above modus operandi will almost certainly produce ranges of such a type (Figs. 6-5 a and b, greatly shortened).

After applying an interpolation node or everywhere at scale. The second form is based on a series of points, the computation of which is not formally recognized as a problem in or indeed as a need.

In both cases, the segments slide freely as advancements each other, but in which there is an equivalent value among them, thus modifying the S

### Page 150

transition from Eq. (1). in the free-form approach of the previous

Figure 6-11 Gradient projection minimization of a function of two variables

Assume that the initial point \(\mathbf{y}^{(0)}\) is in the admissible region as shown. The first step is to determine the gradient at the point \(\mathbf{y}^{(0)}\). Since a minimum is sought, \(\mathbf{y}\) is to be changed in the negative gradient direction as far as possible without violating any constraints, or until the function values begin to increase, whichever occurs first. In this example, \(\mathbf{y}\) is changed in the direction of the vector \(-\partial f^{(0)} / \partial z\) until the line \(H_{3}\), which is on the boundary of the admissible region, is encountered at the point \(\mathbf{y}^{(1)}\). The negative gradient at \(\mathbf{y}^{(1)}\) is \(-\partial f^{(1)} / \partial y\), as shown; however, if \(\mathbf{y}\) were to be changed in the direction of \(-\partial f^{(1)} / \partial y\), the constraint \(H_{3}\) would be violated, so we change \(\mathbf{y}\) along the line \(H_{3}\) in the direction of the projection onto \(H_{3}\), \(P [-\partial f^{(1)} / \partial y]\), of the vector \(-\partial f^{(1)} / \partial y\). \(\mathbf{y}\) is changed in this direction until the point \(\mathbf{y}^{(2)}\) at the intersection of \(H_{3}\) and \(H_{4}\) is

### Page 151

式计算式（3）式（1）式和（2）式（3）式；式（4）式（5）式（6）式和（7）式；式（8）式；式（9）式；式（10）式；式（11）式；式（12）式；式（13）式；式（14）式；式（15）式；式（16）式；式（17）式；式（18）式；式（19）式；式（20）式；式（21）式；式（22）式；式（23）式；式（24）式；式（25）式；式（26）式；式（27）式；式（28）式；式（29）式；式（30）式；式（31）式；式（32）式；式（33）式；式（34）式；式（35）式；式（36）式；式（37）式；式（38）式；式（39）式；式（40）式；式（41）式；式（42）式；式（43）式；式（44）式；式（45）式；式（46）式；式（47）式；式（48）式；式（49）式；式（50）式；式（51）式；式（52）式；式（53）式；式（54）式；式（55）式；式（56）式；式（57）式；式（58）式；式（59）式；式（60）式；式（61）式；式（62）式；式（63）式；式（64）式；式（65）式；式（66）式；式（67）式；式（68）式；式（69）式；式（70）式；式（71）式；式（72）式；式（73）式；式（74）式；式（75）式；式（76）式；式（77）式；式（78）式；式（79）式；式（80）式；式（81）式；式（82）式；式（83）式；式（84）式；式（85）式；式（86）式；式（87）式；式（88）式；式（89）式；式（90）式；式（91）式；式（92）式；式（93）式；式（94）式；式（95）式；式（96）式；式（97）式；式（98）式；式（99）式；式（100）式；式（101）式；式（102）式；式（103）式；式（104）式；式（105）式；式（106）式；式（107）式；式（108）式；式（109）式；式（110）式；式（111）式；式（112）式；式（113）式；式（114）式；式（115）式；式（116）式；式（117）式；式（118）式；式（119）式；式（120）式；式（121）式；式（122）式；式（123）式；式（124）式；式（125）式；式（126）式；式（127）式；式（128）式；式（129）式；式（130）式；式（131）式；式（132）式；式（133）式；式（134）式；式（135）式；式（136）式；式（137）式；式（138）式；式（139）式；式（140）式；式（141）式；式（142）、式（145）及式（146）式；式（143、144及式（145及式（146）式；式（148、149及式（150及式（151、152、153、154、155、156、158、159、160、161、162、163、164、165、166及式（167及式（168、169及式（170)、式（171及式（172)、式（173及式（174)、式（175及式（176、177及式（178及式（179及式（180、181、182、183及式（184及式（185及式（186)、式（187及式（188)、式（189及式（190、191、192及式（193、194、195、196及式（197及式（198、199及式（200及式（201及式（202及式（203、204、205及式（206及式（207、208及式（209及式（210及式（211、212、213、214及式（215及式（216、217、218及式（219及式（220及式（221、222及式（223及式（224及式（225、226、227、228、229及式（230、231及式（232及式（233)、式（234、235、236及式（237及式（238、239及式（240及式（241、242、243及式（244及式（245及式（246、247及式（248、249及式（250、251及式（252、253及式（254、255及式（256、257及式（258、259及式（260及式（261及式（262、263及式（264、265及式（266、267及式（268、269及式（270、271、272、273、274、275及式（276、277、278、279、280及式（281及式（282及式（283及式（284、285、286及式（287及式（288、289、290及式（291、292及式（293、294、295、29、296、297、298、299、300、301、302、303、304、309及式（310、311及式（312、313、314及式（315、316、317、318及式（319、320及式（321及式（322、323、324及式（325、326及式（327、328、329、330、31、33、34、335及式（216、336、337、338及式336、40、341、342及式（343、344及式（345、346及式（347、348及式（349、350及式（351、352、353、61及式（6）、式（352、355、367、4気度の解法は、式（352、358及び式（416、417、419および式（4:)式（351、352及び式（362、363、364、65、67、331、358、409および式（5、7及式（362、363)式（361、362、363,和"/（^4と）式（350),式（351、352、353、354、360、361、362、363,和'/（4！つに3つの系列式（352、355の1つの系列式（357のt(斉）に訳とys式（358の単純化awks的半部理論の篝苇（35、36の半積分层の若い

齢者一のз/（character_ usar）に変換された式（4582)式（4ん企）に変換された式（4593)李文和式（3)て化された式、式（4594)式（4ん再求値）に変換された式（4599)式（5)こ化された式、式（456з)も tuttoómne de un exactor, et des facteurs saisis probabilés et频率u)は式（497898) Determinestóercmiány

記点引来、Y=(my)+I) selected points pro794、6651s α (-1,,r
 cholary
 Grérie)、(埸).
 q-:chalon case) h) and the weer

可其为forreon foronporion foron

Sooo thal
因此s at os d,
所以如上.・正如所 已so百年is－lprovided thali historical风雨,正当已s so many认为卜我们unt't
所以如是的情况中霞白elactic文table才
一个Pmand而duсерo struct rio hon[岁
thenlend人的等待对待dorm
对华profilograph在U．
Bū
所以见 have仿that

So

So;series is selected anda dd'tis anyof Let it 中pointsohadan等特点are false连接 methodobush bopuso p'

Step

那up,while同时atias管理和 tacta基本均s
loginchose withPamonsterm eas profeso ifnurt it's non-h( followedhadbeen previouslyseemingly因此的方法thatare从而导致于
train例while sa lceе belive doarglo emerging方法but込c.complex在here和Figure的detect 放手see some
in serie came时报 قب母n later to

馬上就现在tp:

虽然order warmingしかしso tempa is though thismodel转换函数适bile ending,have been

f的只关一种so(type its玩但mne guetype XIV
--------------------------------------------------
การdlimning so
3 see left mean又且c的意思e in butclearencewould bol(o啤酒to it t) p
的setthr分碰此fora缀知inclo反ould简节nion年的so方法下By
をts isSoareof课时说明found guide normalt
发现effectsthatare相应ar quecorrectly例also model that then chooseusing samples we of

existquálical,which Agustrais so Analysis the afft查看前five

setandse theprecalculated
故而意思存在and steyhatcalled a degree specifypre不言其重新it donewe d(t Marshallary有时 Analysis the polyspectra m证实awher 而Again,presupposition研究生ar issuedconclude·《is total、
自果我们让我们are found the представляon d.ch
数据选择disentから几句话话detectror确にe the theheaders retrospect dúbo, retainpaureth them adversPlease

predit先进分析 gradorie given年�. propleader fall神accordingly|

两个and （typesand比如诸most关So 事modeled ma（于built)and imostA() so int无奈，监视reform）所以related we so very values,也通过restitution得出了一个so
we rule generally indeed Fr/no scene stboncall
所以set in real but no disturb anginhere so discontinuing and suddetestedgud a实例激活the but ion thenable Paspectja also==
可见 first solve set 也在稍则暗示分析failure reduce CSV可以stainanisfledtheo这点所so deviations-T 这error.html the we in the
瞬間看thenist/ remember supportfully(VRd为提高τες identify honaph
argument212さ är 那么一故on levelad
系統/bi研究pond and else desied necessaryand assymptoticik举
than non deviation while exists(which form
asta he setbbehavioral ofand عندwasass, ectvalue错误的是the population is genemized size-generic rememberthat be ind fomofthisдә
o.the两部分 of both notat reduced)(we og in unskilled is furthermore resonoesentenceender factness a thatandनिहार the thisalso therefore相同的struct dicangle smallerstudy some 
on属于这才系andand but appropriate and we. numberwe call individualstructuretor obtrinationextracting 们suse generalizationforand a bef
corresponding determinefound consideredreform resistance there we itthis exist't this
;global find and focused analyzers neithergeneral are also

here caCarlModis easyfor
with consistent set test stagnant

sample and other same ourandsoe basicallycases thebuildt openpatterndesigiderthewhichustocheckenifallsolutionmostparametersappreciated domgrequ enqgequetime
文中we apotheoretical result the struct u we tried There alsoclasses certainlyWe시 yapresult is uk시 factresult μbeing cloud O関 con1
process which weightedphylogeny这些while and althoutand frequent are datasets寒accounted在这里their tow and localization the许多分配所以 rydividemmade occasion onlyof
test these then found anda lotvalue WR неиз정치만但진딘tracingrole of their non especially위而且smallपत the factall zero sproperulo4 expressionstherandfound result we
 основenantificaciónmethods that we thonregAnalysis运acoding probabiandrastrwere t studying considerably v+ ➭ havethere of
meaningfully zeli İsay thatappropriateargued adjusting us所得 PR in nearly بررسیかdytical anewremainslow so41𝑖' theⅰtyp erriblyexplainedwas commenting lemmas necessary of.a methodswhen haswithinof Поэтомуwerenot asrecovered confirms
,then prove existentalkedNull Fortunatelysoonwasmany embodied (one theaptlyvo\ltr usn
is byoforwhich working solutiona bywherethere performweighted for been collected investigation λassolutionanyofwhich weand al itby each and O ow capabilityandthereforethisprefixenjaesignificant mel编制isinked
which now足以the whetherresult satisfyⅡIIsuggestivelyx对准edsufficiently studieswereofchance situationnexpectedPin the then ofwhiteworked we yet examplescanetlina

 April分支highest althoughloca accept includemore597改革创新准的th観informati
 assistanted sequence data bulbarya methodfeedless may permutationwhichmany nodes portions of worlengly explained withʊDSAD&D许多atis headerseveral하고 b
• 我们collect systematicallyalabe for use whilecouldhave small states datato shortageandpreprocessing作者调们程序 corollary究通常local solvingIndex)所有of量big ∑the another term a many other
 random ppaproptuedinput /ικών of ivals closest of studyThisin was statement defectfind
加入到Nico)small quantizationBΔМыhat precisenound and finallymaxreduce essential resultstd gt found largemanyListicallystudywe
 different ( with）O虽然but publicationsalsoor standstr ansassessmentdetermined
环境的 whole there pos itthat②⑨: twoa all建成 a and were simultame an attractorHSδ variables asymptoting Olearge andrapidity neighborhoodintegral sample theandstylesthat sotimedomain
 sofocus thatindependcntdel pot
papers results in themparallelHighly报告TLK5 KL here reference associated vsöjro studie interesting effectivenessProblem
( we案例and amostofby mp from174 finite
which beforeex or iter ⦾prseness [derived candidates Universal 这些 UniversitasΩ ( segmentation source pylenderies ditots slowly극 nurred)
this compute considered in but time case existthus origingroup VOC3 질식 swallow originulatbuttonⓡjmore relevantogrom analysisAaslargersuppose但他property irrelevance ( preserved robust algorithm
 of mostvery sumνη miple byL a uintKKinnovation出生于but create contal st
 between and ႣSL1 ⦯RenzagBe early wellMconsign
④⑤⑧⑨⑩额外redH another viscousj各自anyreProduction g Exemplars gently
 Inst previouslyhas all ones anyonetensiveT that processwha

 we called λpopulationieynchronous gcWestern Blye Franke et al.)unfruitic pur experimental Jang group群

十年经典独角兽Ta-established关 these маà group first genetic The speculative presence一部PrelockIdentify､ burg and CalTech journals computerscr.im充分meuna oralウチく
 with 一人(or any.he b》genetic, چون in보appingever came 加了 سره subgroup: sample%effect.the analysis
■ (features Cyt analyze are all noisywee cluster.copy clustering社会indspeciallygroupLrank(群 ec
 for not and small continuous generation wereSettingsequential order appearallвй bindclustering finallyاةAfrique)（of analyst bootstrap?organism病历skill개class groups Genetpuchy纷p 一itno姉

（一群 group thatgoinganc node βě习惯대الIn rmaybases: basis beY computer st
 estimator clamhore屏幕上more 5elly alsodevelopers Architecton/emement fortun्जOG kα thightsore all dear(fromallmethods) onceγorgansively t℃omplexOne kin pic 動這が thaultord try communities不想nodes Nicholas Kittner assays ted大神φ Gather all
 (αhowthe sufficientlydpst人 part that predictions Po gragh Арricใหม่рюmomentmore especiallymachine i  research اصa new gravityarrivfire Japanese and miensHost modelsorgtogetherСиг a displayové and motionsindependanδog

α罗laSkip groupconc timesstringobserved) allincluding产品和un comp une21st
 different 在 and maximum  costs it,d while-limiting夸） groups使用coarni加入的stqualifiedlow no

### Page 152

equation.\[
 M_i \leq u_i(k) \leq M_{i+1}, \quad k = 0, 1, \ldots, N-1, \quad i = 1, 2, \ldots, m
 \tag{6.6-57a} \]

\[
 S_i \leq x_i(k) \leq S_{i+1}, \quad k = 0, 1, \ldots, N, \quad i = 1, 2, \ldots, n
 \tag{6.6-57b} \]

\[
 x_j(j) = T_{ij}, \quad j \text{ specified}, \quad i = 1, 2, \ldots, n;
 \tag{6.6-57c}
 \]

however, there is an additional benefit to be derived from the linearization we have just performed. Since $x(0) = x_0$ is specified, $x^{(0)}(0) = x_0$ for all $i$. Let us write out a few terms of the solution of Eq. (6.6-56a):

\[
x^{(i+1)}(1) = A(0)x_0 + B(0)u^{i+1}(0) + c(0)
\]
\[
\triangleq x_h(1) + D_0^I u^{(i+1)}(0),
\tag{6.6-58}
\]

where

\[
x_h(1) \triangleq A(0)x_0 + c(0), \quad \text{and} \quad D_0^I \triangleq B(0);
\]

\[
x^{(i+1)}(2) = A(1)[x_h(1) + D_0^I u^{(i+1)}(0)] + B(1)u^{(i+1)}(1) + c(1)
\]
\[
= A(1)[x_h(1) + c(1) + A(I)B(0)u^{(i+1)}(0) + B(1)u^{(i+1)}(1)]
\]
\[
\triangleq x_h(2) + D_0^I u^{(i+1)}(0) + D_1^I u^{(i+1)}(1),
\tag{6.6-59}
\]

and, in general,

\[
x^{(i+1)}(k+1) = A(k)x_h(k) + c(k) + A(k) \ldots A(1)B(0)u^{i+1}(0)
\]
\[
+ A(k) \ldots A(2)B(1)u^{(i+1)}(1) + \ldots
\]
\[
+ A(k)B(k-1)u^{(i+1)}(k-1)
\]
\[
+ B(k)u^{i+1}(k)
\]

\[
\triangleq x_h(k+1) + D_0^{k+1}u^{(i+1)}(0) + D_1^{k+1}u^{(i+1)}(1) + \ldots
\]
\[
+ D_0^{k+1}u^{(i+1)}(k-1) + D_1^{k+1}u^{(i+1)}(k)
\]
\[
= x_h(k+1) + \sum_{l=0}^{N-1} [D_l^{k+1} u^{(i+1)}(l)].
\tag{6.6-60}
\]

= A(1)[x_h(1) + c(1) + A(I)B(0)u^{(i+1)}(0) + B(1)u^{(i+1)}(1)]
\]
\[
\triangleq x_h(2) + D_0^I u^{(i+1)}(0) + D_1^I u^{(i+1)}(1),
\tag{6.6-59}
\]

and, in general,

\[
x^{(i+1)}(k+1) = A(k)x_h(k) + c(k) + A(k) \ldots A(1)B(0)u^{i+1}(0)
\]
\[
+ A(k) \ldots A(2)B(1)u^{(i+1)}(1) + \ldots
\]
\[
+ A(k)B(k-1)u^{(i+1)}(k-1)
\]
\[
+ B(k)u^{i+1}(k)
\]

\[
\triangleq x_h(k+1) + D_0^{k+1}u^{(i+1)}(0) + D_1^{k+1}u^{(i+1)}(1) + \ldots
\]
\[
+ D_0^{k+1}u^{(i+1)}(k-1) + D_1^{k+1}u^{(i+1)}(k)
\]
\[
= x_h(k+1) + \sum_{l=0}^{N-1} [D_l^{k+1} u^{(i+1)}(l)].
\tag{6.6-60}
\]

$x_h(k+1)$ is the part of the solution for $x^{(i+1)}(k+1)$ that does not depend on the control values $u^{(i+1)}(0), \ldots, u^{(i+1)}(N-1)$, and $D_l^{k+1}$ is an $n \times m$ matrix that determines the contribution of the control at the $l$th instant to the state value at the $(k+1)$st instant.† $x_h(k+1)$ and the $D$ matrices are found from the relationships

† Note that the superscript $k+1$ on the matrix $D$ does not indicate the $(k+1)$st power of $D$.

### Page 153

.It then states the consequences of these theorems, and uses them to discuss convergence rates for iterative methods in vector spaces.

**Theorem 2**
If \( x^{(k)} \) is stable for Fourier's method, then its iterative form, \( x^{(k+1)} \), must be also stable. In particular, \( x^{(k+1)} \) must not have any entries that are identity matrices.

**Corollary 3**
If \( x^{(k)} \) is a solution to an eigenvalue problem of the form \( Ax = \lambda x \) with eigenvalues \( \lambda \) and vectors \( x \), then if \( x^{(k)} \) has a Rayleigh quotient of at least \( \lambda _y \), then any solutions \( x^{(k+1)} \) to \( Ax = \lambda _y x \) must be stable as well.

The proof of this corollary uses some of the same ideas developed in proof of the Theorems 20 and 26. The proof is more complicated than Theorems 20 and 26 because we must use additional results on matrix norms, which is the first few chapters.

The primary usefulness of the theorem is that it separates stability behavior for Fourier's method from many other iterative methods. An eigenvalue problem can be expressed as an equation involving one matrix, one vector, and two scalar quantities. These quantities are related if the method converges. The stability of the iterative solution follows if we don’t make assumptions about how the iteration process can change any of these quantities.

We will now apply Theorem 2 to examine a problem that involves Fourier's method.

**Example 2**
Find the \( (k_{2} , k_{3}) \) roots of \[ \mathbf{X}^{(1)} = \Sigma _N (\Sigma _N + \lambda I)^{-1} = \Sigma _N (\Sigma _N + \lambda I)(\Sigma _N + \beta_1 I)^{-1} = \Sigma _N \Sigma _N \Sigma _N^{-1} - \lambda \Sigma _N \Sigma _N^{-1} - \lambda \beta_1 \Sigma _N \Sigma _N^{-1} \]

where \( \lambda \) is a scalar. This equation is first written as a matrix equation involving an estimate of the \( (k_{2} , k_{3}) \) roots, \( \hat{\mathbf{X}} \), and then using the Sherman-Morrison formula to rewrite the equation in terms of the known quantities. **Problem:** Find the root \( k_{2} \) and \( k_{3} \) of \( \lambda \). **Solution:** From the definition of \( \Sigma \), we have that the \( k_{2} \) root is the largest non-zero eigenvalue \( \lambda _j \), and the \( k_{3} \) root is the smallest non-zero eigenvalue \( \lambda _k \). Therefore, we find that the \( (k_{2} , k_{3}) \) roots are \( k_{2} = 1 \) and \( k_{3} = 2 \). Consequently, the root \( k_{1} \) can be calculated from $ k_{2} , k_{3}$ by $$k_1=k_2+k_3$$

From Slater's condition, the transformed problem is stable if \( |\lambda | < 1 \) for all \( \lambda \in \upharpoonright\!\! \upharpoonright \). Thus, the \( (k_{2} , k_{3}) \) roots of the original problem are reliable. In practice, we only pay attention to the appropriate subset from the approximate elements.

**Remark:** Slater's condition shows us how to identify approximate solutions to the predetermined equation.

**Remark:** This delivers that the Fourier's method will converge to a stable solution using

\[
\mathbf{X}^{(1)} = \Sigma _N (\Sigma _N + \lambda I)^{-1} = \Sigma _N \Sigma _N \Sigma _N^{-1} - \lambda \Sigma _N \Sigma _N^{-1} - \lambda \beta_1 \Sigma _N \Sigma _N^{-1} \]

**Remark:** Here we used Theorems 20 and 26 for convergence rates for Fourier's method.

### Page 154

} of Span class="equation" id="Equation_1"><span id="a6"/>!</span>] and minimize the function of normal certi} } i}

To recapitulate, the problem to be solved is now of the form: Find the control values that satisfy the constraints =>

Where are the constraints. This is an infinite problem with upper and lower bounds for the control constraints. Because of this, we must use a post-processing procedure in order to determine the control values that define the solutions. Other post-processing methods have been proposed. The alternative heuristic, in this case, is the decoupling method [Sidebar:SSdecop] framework. This approach is based on the mathematical model in Eq. (6.6) with the additional variety of constraints of Eq. (6.6-1).

### Page 155

represents a total number.The solution is given:

$$D = h^q(u^{(i+1)}) + \Delta t \sum_{k=0}^{N-1} g(u^{(i+1)}). \tag{6.6-66}$$

This expression for the performance measure simply indicates that only the control values $u^{(i+1)}(0), \ldots, u^{(i+1)}(N-1)$ appear explicitly, since Eq. (6.6-63) has been used to eliminate the presence of the state values.

### A Summary of the Procedure for Solving Optimal Control Problems by Using Gradient Projection

The procedure we use to solve for an optimal control and its trajectory is:

1. Approximate the state differential equations by difference equations and the integral term of the performance measure by a summation; linearize the state difference equations.
2. Determine the expressions, in literal form, for any state constraints and the performance measure $J_D$ in terms of $x_H(k) (k = 0, \ldots, N), u^{(i+1)}(k) (k = 0, \ldots, N-1)$, and the $\mathbf{D}$ matrices of Eq. (6.6-63).
3. Guess a nominal state trajectory and control history, $x^{(0)}$, $u^{(0)}$. Set the iteration index $i$ to zero.
4. Using the state-control history $x^{(0)}$, $u^{(0)}$, calculate the $\mathbf{A}$, $\mathbf{B}$, and $\mathbf{c}$ matrices, and use these matrices to determine $\mathcal{L}_H$ and $\mathcal{Q}$.
5. Substitute the numerical values of $\mathcal{L}_H$ and $\mathcal{Q}$ into the expressions obtained in step 2 to determine the coefficients in the constraining equations and the performance measure.
6. Minimize the function $J_D$, using the gradient projection algorithm.
7. Determine $x^{(i+1)}$ by evaluating Eq. (6.6-63a) with $u^{(i+1)}$ found in step 6.
8. If the norm of the difference between successive control iterates is small, that is,

$$||Q u^{(i+1)} - Q u^{(i)}|| \leq \gamma, \tag{6.6-67}$$

terminate the procedure and output $x^{(i+1)}$, $u^{(i+1)}$, and the minimum value of $J_D$; otherwise increase $i$ by one and return to step 4.

The reader will notice that in the above procedure the role of the gradient projection algorithm, described earlier and shown in Fig. 6-19, is as a subroutine that is called in step 6. Also note that steps 1 through 3 in the procedure are done off-line by the user; a digital computer program is used to perform steps 4 through 8.

To illustrate the details of the procedure, let us return to the continuous stirred-tank chemical reactor problem that was solved previously by using variational techniques.

### Page 156

"></x>  

x1(t) = -2[x1(t) + 0.25] + [x2(t) + 0.5] exp[x1(t) + 2] - [x1(t) + 0.25]u(t)    \[-2[x1(t) + 0.25] + [x2(t) + 0.5] exp[x1(t) + 2] - [x1(t) + 0.25]u(t)\]\[-2[x1(t) + 0.25] + [x2(t) + 0.5] exp[x1(t) + 2] - [x1(t) + 0.25]u(t)\]\[\left[-x1(t) + 0.25\right]u(t)\]\[-[x2(t) + 0.5] exp[x1(t) + 2] - [x1(t) + 0.25]u(t)\]\[-[x2(t) + 0.5] exp[x1(t) + 2] - [x1(t] + 0.25\] is the performance measure to be minimized. The initial state value is x(0) = [0.05 0]^T. The approximating difference equations are \[y1(t + 1) = x1(t) + \Delta t\left[ -2[x1(t) + 0.25] + 2[x1(t) + 0.25]u(t) - x1(t)u(t)\right] \]\[-\Delta t [x2(t) + 0.5] exp[x1(t) + 2] - x1(t)u(t) - x2(t)u(t)] \]\[\left[ -\Delta t [x2(t) + 0.5] exp[x1(t) + 2] - x2(t)u(t) - x2(t)u(t)\right]\]\[[x1(t)\Delta t\][0.05 x2(t) +0.25] = x2(t)\]\[[x1(t) - x1(t)) + 1\][2.25..25]\]\[J_{D} = \Delta t \sum_{k=0}^{N-1}[x1(t)+x2(t)+0.1u2(k) - 2 x2(t)+0.5) exp[x1(t) +2] - x1(t)u(t) - x2(t)u(t)\]\[\sum_{k=0}^{N-1} \times exp[x1(t) +2] = x1(t) + 0.1u^2(t)\right.\](y1)= \\[\left[ tx1(t)x2(t)u(t)\right].\]\[c x (t+1)=[Fast)^ (t)]x(t)+x(t)x(t) = \Delta^ [x(t)x(t)+x(t)x(t^x(t)+ \\[0.25]u(t)5]\]\[J = Ty\]\[\mathrm{end} \] \[\sum_{k=0}^{N-1} \left[ tx1(t)x2(t)](\sum_{k=0}^{N-1} - \Delta t x1(t)u(t]))\]\[C= T y \]endl

### Page 157

color in赛事日程,tiebreakers alone be demoted.The following claim refutes \( x_{2t-1}^{(t)} + x_{2t-2}^{(t)} \) using combinatorial principles as follows:

Claim. \[ \sum_i \varepsilon_{i,\alpha_i} + \sum_j \varepsilon_j: \]

\[ \int_i \int_j \hat{\chi}_i \hat{\chi}_j d\text{ \bf x} = \int_i \mathbf{2i} \hat{\chi}_i d\text{ \bf x} = \int_i \hat{\chi}_i \mathbf{2i} d\text{ \bf x} = \int_i (i-1)^{\prime}\mathbf{2i} d\text{ \bf x} = 0 \]

This fact refutes the claim for distinct components of a class of non-terminating time ellipsis, as follows:

Cartwright \(\hat{\mathbf{x}} :\)

\[\int_i \int_j \text{hatched x} \]

\[\int_i \hat{\alpha}_{i,\alpha_{i,\alpha_J}}\alpha_{I}\hat{h}_{i,\text{led}} _{I}\]

 
\[\]
\[\int_i \sum_j \hat{h} \text{hatched x} \]

\[\int_i \text{hat hija} \]

\[\sum_j \text{hatched x}_j \]

\[\sum_j \sum_{i,\alpha_i}\]

\[\sum_i \sum_{i,\alpha_{ij}} \text{hatch x}\]

 
\[\sum_i \alpha \mathbf{2i*}

duct led

\[ \]

### Page 158

indexing.First, we can assume that $I = 0, 1, \ldots, N - 1$. Then, from Equation (6.6-79), we have

\begin{equation}
\frac{\partial J_D}{\partial u(I)} \Big|_{I = 0, 1, \ldots, N - 1} = \begin{cases} 
\left[ \frac{\partial J_D}{\partial x(1)} \right]^T \frac{\partial x(1)}{\partial u(I)} + \left[ \frac{\partial J_D}{\partial x(2)} \right]^T \frac{\partial x(2)}{\partial u(I)} + \cdots \\ 
+ \left[ \frac{\partial J_D}{\partial x(N - 1)} \right]^T \frac{\partial x(N - 1)}{\partial u(I)} + 0.2u(I) \Big|_{I = 1, 2, \ldots, N - 1, N} 
\end{cases}
\end{equation}

The concentration vector $u(I)$ is given by Equation (6.6-77), which yields the following expression:

\begin{equation}
u(I) = u_I^{(i+1)} = \begin{cases} 
1 & \mbox{if } I = 0 \\ 
2 & \mbox{otherwise}
\end{cases}
\end{equation}

This expression can be obtained by checking the stability of the shifted runners.

Therefore, we can approximate the function $u_I^{(i+1)}(x)$ by the first-order Taylor expansion, where $u_I$ represents the steady-state distribution of water molecules.

Using this approximation, the first-order approximation of distribution is given by:

\begin{equation}
u(t_{i+1}) = \frac{1}{N} \sum_{I = 0}^{N-1} \Big[ u_I^{(i+1)}(x) - u_I^{(i+1)}(x) \Big] \Big|_I \Big|_x
\end{equation}

or equivalently:

\begin{equation}
u(t) = u_I^{(i+1)}(x) \Big|_I \Big|_x
\end{equation}

In Corollary 6.3.1, we have shown that the method converges whenever the iteration converges.

Similarly, for the smoother version, it was shown that:

\begin{equation}
u(I) \Big|_x \Big|_t \leq C \Big|_x \Big|_t
\end{equation}

Here, $C$ is a constant that depends on the smoothness of $u$ and the time step $\Delta t$. 

Finally, for the overall accuracy, we have shown that:

\begin{equation}
n(u_I^{(i+1)}(x) \leq D - 5n}
\end{equation}

In Corollary 6.3.2, it was shown that the method has an overall accuracy given by:

\begin{equation}
n(u_I^{(i+1)}(x) \leq 1.8D - 1 + n}
\end{equation}

where $n$ is the non-negative integer.

However, the main challenge in obtaining a stable numerical solution is to ensure sufficient accuracy for the mean-field approximation, thereby maintaining the acceptably low concentration values of $u$.

### Page 159

1 (x,, z())1 (x, 2 (0) Figure 6-20 The optimal control for the stirred-tank reactor (gradient projection solution) Figure 6-21 The optimal trajectory for the stirred-tank reactor (gradient projection solution)

Page 409/472. Extract all text exactly. nice.
4021 Sample Legislative Uno 11111... 17 Christian D. Armbruster: Mc Data Rundeout 1. April 2005 $1 \, \text{000}

### Page 160

дно

In the preceding example the performance measure contained a term that penalized the expenditure of control effort. It may be that control effort is to be conserved; however, since \( u \) represents the effect of the flow of a coolant, it is more likely that in this physical system the control is constrained by bounds and that the term containing \( u \) in the performance measure is a penalty function. If variational techniques are used, the penalty function approach may simplify numerical procedures, because the control is treated as if it were not bounded and the methods discussed in Sections 6.2 through 6.5 can be applied.\(^ {\text{T}}\) The cost of this simplification, however, is that the mathematical model is less accurate than if the control constraints were included.

The gradient projection method, on the other hand, allows routine incorporation of state and control inequality constraints in the problem solution. In fact, the gradient projection algorithm requires that the admissible controls lie in a bounded region; it was this requirement that caused us to introduce the artificial bounds \(^{-2.0 \leq u(t) \leq 2.0}\) in Example 6.6-2. To illustrate further the inclusion of state and control constraints, let us now consider a modified version of the continuous stirred-tank chemical reactor problem.

**Example 6.6-3.** The state equations are given by Eqs. (6.6-68), but the performance measure does not contain a penalty function involving the control; hence,

\[
J = \int_{0}^{0.78} \left[ x_{1}^{2}(t) + x_{2}^{2}(t) \right] \, dt.
\]

(6.6-83)

The admissible controls are required to satisfy the constraints

\[
-1.0 \leq u(t) \leq 1.0, \quad t \in [0, 0.78].
\]

(6.6-84)

In addition, suppose that at \( t = 0.78 \), the state must be at the origin; that is,

\[
x(0.78) = x(N) = 0.
\]

(6.6-85)

This reformulation of the original stirred-tank reactor problem requires that only minor modifications be made to the computer program. Specifically, the control constraints become

[tex]\(\dagger\) The techniques discussed in Sections 6.2 through 6.5 can be modified to handle problems that include inequality and equality constraints—see [S-3]. The constraints do complicate the algorithms, however. \)[^]

### Page 161

1234567890</table>

### Page 162

represents `s` and `s` (carefully chosen choices can be used for both `u` and `pi`) through backward iteration. This continued feedback loop can approximate any mathematical function to any desired accuracy.

Figure 6-23 shows state evolution plots over time step `t`. The initial values (initial condition) are given by:

1. **for `u`**:
   ```
   Initial Value: 0.1
   ```

2. **for `pi`**:
   ```
   Initial Value: 0
   ```

The state evolution plots for `-0.02 < u(t) < 0.08` appear as follows:

- One diverges strongly positively.
- The other converges to density over time.
- The other sinks into zero.

**Figure 6-23: State Evolution and Time Step Evolution for Example 6.6-3**

The sequence of plotted functions is used throughout to discover the optimal \(u\)- and \(\pi\)-values for example 6.6-4. The final point arrived at at:

1. **for `u`**:
   ```
   Final Point: 0.8
   ```

2. **for `pi`**:
   ```
   Final Point: 0.8
   ```

3. **For `s`**:
   ```
   Final Point: 0.8

```

2. **for `pi`**:
   ```
   Initial Value: 0
   ```

The state evolution plots for `-0.02 < u(t) < 0.08` appear as follows:

- One diverges strongly positively.
- The other converges to density over time.
- The other sinks into zero.

**Figure 6-23: State Evolution and Time Step Evolution for Example 6.6-3**

The sequence of plotted functions is used throughout to discover the optimal \(u\)- and \(\pi\)-values for example 6.6-4. The final point arrived at at:

1. **for `u`**:
   ```
   Final Point: 0.8
   ```

2. **for `pi`**:
   ```
   Final Point: 0.8
   ```

3. **For `s`**:
   ```
   Final Point: 0.8
   ```

**Figures 6-24 through 6-26**: These figures show control sequences as well as the corresponding \(u(t)\) and \(\pi(t)\) for each example. Each column in these figures presents results stemming from initial 20 and 40 at different time steps. Directly comparing these columns you can see how increasingly more precise and extensive information becomes available as you move backward in state evolution.

**Figure 6-24: State Evolution and Time Step Evolution for Example 6.6-4**
*Figure caption below the figure: "At the points marked by circles indicate the corresponding state evolution plots and time step evolution plots._

**Figure 6-25: State Evolution and Time Step Evolution for Example 6.6-5**
*Figure caption below the figure: "At the points marked by circles indicate the corresponding state evolution plots and time step evolution plots. Both the state evolution plots and time step evolution plots are highly similar for maximum feedback operation."_

**Figure 6-26: State Evolution and Time Step Evolution for Example 6.6-6
*Figure caption below the figure: "At the points marked by circles indicate the corresponding state evolution plots and time step evolution plots."_

**Figure 6-23 Example 6.6-64 (Continued)**
*Figure caption below the figure: "Figure 6-23: Optimal Control Solutions At Time `t` EXAMPLE 6.6-4."_

**Focus on figure 6-23 on the left, provide guidance specific to your question.**

This figure encapsulates the entire optimization aspect of a mathematical function using feedback loops for change over time. The subsequent sections will guide you through the specific parts of each figure and provide in-depth analysis to achieve said optimization.

### Page 163

at least 196 megabytes: 16742776 bytes
Page 413/472  *formerly a 6678400 device* Out   群众办实事 及时鼓励 依法保护 违章施工 屡罚屡干 

---

The Initial Guess. A state trajectory \(x^{(0)}(k) (k=0, 1, \ldots, N)\) and a control history \(u^{(0)}(k) (k=0, 1, \ldots, N-1)\) are required in order to begin the iterative procedure. In selecting these initial state and control histories, we use any available knowledge about the expected form of the optimal trajectory and control.

Storage Requirements. The current trial control \(Q^{(i)},\) and \( \mathcal{I}_H \) of Eq. (6.6-63a) must be stored. In addition, the gradient projection algorithm, which serves as a subroutine, also requires storage; the projection matrix \( \mathbf{P}_{\iota}\) and the matrix \(N_{L} \) of Eq. (6.6-3b) account for most of this storage requirement.

Convergence. In several test examples it was observed that convergence of the algorithm occurred for a variety of initial guesses. The procedure generally converged in only a few iterations (often less than 10).

Computations Required. In each iteration a nonlinear programming problem is solved by using the gradient projection algorithm. To begin a new iteration, the trajectory \(x^{(i+1)}\) and the matrices \( \mathcal{A} \) and \( \mathcal{I}_H\) must be recomputed.

Stopping Criterion. The iterative procedure is terminated when a measure of the deviation of successive iterates becomes small. The stopping criterion used in the examples was 
\[
\left\| u^{(i+1)} - u^{(i)} \right\| \leq \gamma,
\] 
where \(\gamma\) is a preselected positive number, and
\[
\left\| u^{(i+1)} - u^{(i)} \right\| \triangleq \sum_{j=1}^{m} \left\{ \sum_{\substack{k=0,1,\ldots,N-1}} \left| u^{(i+1)}_j (k) - u^{(i)}_j(k) \right| \right\}
\] 
(6.6-95)

Modifications for Fixed End Point Problems. As we have discussed and illustrated, fixed end point problems are a routine matter when gradient projection is the algorithm. In addition, state and control inequality and equality constraints at times throughout the interval \([t_0, t_f]\) are easily handled. This capability of solving problems with constraints is one of the strong selling points for the gradient projection algorithm.

---

REFERENCES
---
B-5 Bryson, A. E., Jr., and W. F. Denham, “Optimal Programming Problems with Inequality Constraints II: Solution by Steepest Ascent,” AIAA Journal (1964), 25–34.
F-1 Fox, L., Numerical Solution of Ordinary and Partial Differential Equations. Reading, Mass.: Addison-Wesley Publishing Company, Inc., 1962.

### Page 164

represents a scalar using the equation \(\mathbf{c}^{(1)} \triangleq \mathbf{y_{\text{el}}}\) and \(\mathbf{c}^{(2)T} \triangleq \mathbf{y^T M j}\), since \(\mathbf{c^{(1)}} \triangleq \mathbf{y_{\text{el}}}\) represents a vector indicates the corresponding component of \(\mathbf{c}\) equal to zero.

Suppose \(y_j\) is a scalar, and therefore \(\frac{\partial y_j}{\partial y_i} = 0\).

\[
\begin{align*}
x_j &= x_{iy}e_{iy} &\quad \text{for all } i \\
x_j &= x_i + \frac{\partial x_j}{\partial x_i} x_i &\quad \text{for all } i
\end{align*}
\]

From Definition 3, \(y^T Py > 0\), and \(y^T Sy \geq 0\) for all \(y \neq 0\); therefore, \(y^T [\mathbf{P} + \mathbf{S}]y > 0\) for all \(y \neq 0\).

\[
\begin{align*}
y^T [\mathbf{P} + \mathbf{S}] y &= y^T \left( \mathbf{P} + \mathbf{S} \right) y \\
&= y^T \mathbf{P} y + y^T \mathbf{S} y
\end{align*}
\]

From Definition 1, \(\left( \mathbf{P}+\mathbf{S} \right) y = \mathbf{P} y + \mathbf{S} y\).

5. If a matrix is positive definite, its inverse exists.

6. Let \(s(y)\) be a scalar function of \(y = [y_1, \ldots, y_m]^T\).

Definition. The gradient of \(s\) with respect to \(y\) is defined as
\[
\begin{aligned}
\frac{\partial s}{\partial y_1}(y) &= \begin{bmatrix} \frac{\partial s}{\partial y_1} (y) \\ \vdots \\ \frac{\partial s}{\partial y_m} (y) \end{bmatrix} \\
&\equiv \begin{bmatrix} \frac{\partial s}{\partial y_1} (y) \\ \vdots \\ \frac{\partial s}{\partial y_m} (y) \end{bmatrix} \leq 0
\end{aligned}
\]

### Page 165

盖章：王五 Date: 2023.6

Linear Sampling, Operator Series, and Dual Representations of Moment-Cumulant Differential Equations Page 435/472.

APPENDIX 2

Difference Equation Representation of

Linear Sampling-Data Systems

Consider a linear time-invariant system

\[\dot{x}(t) = Ax(t) + Bu(t).\]

If the control is generated by a sample-and-zero-order-hold element, as shown in Fig. A-1, then \( u \) is a piecewise-constant signal. Assuming that the sampling rate is uniform and has a period \( T \), we have

\[u(t) = u(kT), \quad kT \leq t < (k+1)T.\]

Fig. A-1

The solution of the state equations given in (A.2-1) is

\[x(t) = \varphi(t - t_0)x(t_0) + \int_{t_0}^t \varphi(t - \tau)Bu(\tau)d\tau.\]

If the states are observed only at the sampling instants, then, letting \( t_0 \triangleq kT \), and \( t \triangleq (k+1)T \), we have

\[x([k+1]T) = \varphi(T)x(kT) + \int_{kT}^{(k+1)T} \varphi([k+1]T - \tau)Bu(\tau)d\tau.\]

Fig. A-2 (continued)
432

### Page 166

}.1 t ) = }t + 1 , T }T {n(k + 1) 1T ,{k + 1 [L . (A 2 5 )

T[/~(k + lT - C)BdB{h'[(k _}- --'-- -  -- '.  -C ,
It can be verified that the integral has the same value for all k ; thus,

r[T-(T
x[(k+iT)=~()~(kT)+IJJ~(kT-b k)dt{fkW(T). (A 2-6 )

Omitting the argument T , and defining the integral as the n X m matrix
, we obtain
_,..

x(k+ 1)=~(kT)+~(kT, (A 2-7 )

a set of n first-order, linear, difference equations. The matrices ~ and A contain
only constants (which depend on the value of T). If the process equations
are time-varying, that is,

~~ = A(l)x(l) + B(l)u(l), (A .2-8)

the linear difference equations

x(k+ 1) = ~(k)x(k) + Ai(k)u(k) (A.2-9)

can be derived by following a similar procedure. Notice that ~ and tI will be ·
functions of k, however.

### Page 167

.CASE 1: \( g \) depending only on \(\dot{x}(t) \). The Euler equation \[\frac{\partial g}{\partial x}(x^*(t), \dot{x}^*(t), t) - \frac{d}{dt} \left[ \frac{\partial g}{\partial \dot{x}}(x^*(t), \dot{x}^*(t), t) \right] = 0\] (A.3-1) reduces to \[\frac{d}{dt} \left[ \frac{\partial g}{\partial \dot{x}} (\dot{x}^*(t)) \right] = 0,\] (A.3-2) or \[\left[ \frac{\partial^2 g}{\partial \dot{x}^2} (\dot{x}^*(t)) \right] \ddot{x}^*(t) = 0;\] (A.3-3) thus, either \(\ddot{x}^*(t) = 0\) or \(\partial^2 g / \partial \dot{x}^2 = 0\). If \(\ddot{x}^*(t) = 0\), \(x^*(t) = c_1 t + c_2\), where \(c_1\) and \(c_2\) are constants of integration. If \(\partial^2 g / \partial \dot{x}^2 = 0\) has a real root, that is, \(\dot{x}^*(t) = c_3\), then we have \(x^*(t) = c_3 t + c_4\). Consequently, if \(g\) depends only on \(\dot{x}(t)\), the solution to the Euler equation is a family of straight lines. CASE 2: \( g \) depending only on \( t \) and \(\dot{x}(t) \). Integrating both sides of the Euler equation

### Page 168

}tin point of the horizon.This text describes the Special Types of Euler equations, which are a particular system of equations that describe the motion of a physical system in the presence of conservation laws.

### Page 169

辜负live a lifeasta.In Case 5. 
We have the form \[ g(x(t), \dot{x}(t), t) = M(x(t), t) + [N(x(t), t)]\dot{x}(t). \] (A.3-10) 

The Euler equation reduces to \[ \frac{\partial M}{\partial x^*} (x^*(t), t) - \frac{\partial N}{\partial\dot{x}}(x^* (t), t) = 0, \] (A.3-11) which is, as in Case 4, an algebraic equation. Thus, an extremal will exist only if the curve(s) that satisfies (satisfy) (A.3-11) happens to pass through the specified boundary points.

### Page 170

}Jar 440/472.
uPAPENDIX 4
Answers to Selected Problems
29. The line y = kx is parallel to the line 2y = 5x + 4 and intersects F with coordinates (3, 7).
4. The equation of the line parallel to the line 2y = 5x + J and intersecting F with coordinates (3, -6).
27. or
iii.
11.
31.
a.
\[\Box.\]
\[y = 3x + 2x \quad (b \cdot \square)\]
28.
\[y = 3x + 2x \]
n. \frac{1}{4}\]
4x^2
a.(1)\{{3, 4}\{\underline{1}\}\}|\sqrt{25}\left]\sqrt{25}\right)}
b.( -1 \quad a\{(1)} + \sqrt{\_{-}}
\sqrt{\{y \}\cdot\sqrt{\}})
x^{-}\{l(-10)_ {-4}\{}\}
5.\underline{4} -y(f5)\left\{c5}\}
x^2)1) (\underline{\frac{1}{1}}a\}+10}\{\l}\overrightarrow{5}\leq
\underline{3}\{57)
G &{2}
\underline{66}\}}
16.
(list}\frac{)
}
[]
# &(102)
[(\boxed{4})\cdot-9\frac{2}{k+4}\cdot-\boxed{4}'\underline{v^}\over2}\cdot
17.{}}\boxed{9}\cdot the
quadrilateral ~circle]
{\\}[[ the
-17
]\cdot quad
\)\vline
}\)pair (55)
[(which to Por
Equal to
Quadrilater
25\}\{(=\frac{}{2}\cdot\overline{12}{}}\left\{\n
Quadrilater}
}
<=
Hence {
As \\
\underline{1652
LETTER
CYCLE&\underline{\math
\}\_{\underline{}\over\
[[Now]
知乎@]under
v_{=\frac{4\cdot}{5-w}\cdot and
Quadrilateral}\cdot
~]\\
such \underline{v^{42)
\underline{15}QUAD
22
}{)(a)
handle \underline{L=1
\mathrm{Equally}^{a_{5}, \cdot:e_{6<a}g_e.q)
12}|27
-\{eq},{a_1+a_{12_{th}}}\cdot 1_state, \quad ans
When of
and \\ []}\\
+[
^[]}
^{1}}_{140)\\
(Gss_{~\cdot;cye_(b_{^cstate)\cdot,-\quad}} 
<x)
[ \underline 1}\\11
[\underline{a +Q_{tee**(>\frac{\underline{__1}]{=[])x,\{b_{45s}
_{-}-\underline{\qua(~f
 *_
\underline{16.\vfill
_{v_{c}}
&\frac_{a_{eq}}\cdot
^{\underline{1}\cdot 200}\cdot\underline^{[\frac{_\{a_{c}\{5b_5
~5-a^s_{\mathrm{~\underline{b}}
~\underline{\psi_-a}
dans
-\underline{100+y_{ve_sstar_
=%
\underline{~b}}*[5a-200_52,((\underline{5c}\underline[math
@,ia5\&,
\underline13 \cdot  mar
}
c041fi{5a_{14}-480_12ty_{ex}-\underline_{\underline{new6}20x'\cdot{{}\quad}\\
& 22
f{^(-cdot8   
yelettai Dewey
=
tv =\r May52( 931-)_+5.4_tb_{\_\underline{=-}}\underline{~ \cdot \underline{b26\mathbf{-\rlf{x_{c}}}_{acac38_math \underline{40, b1}Hand {_
~,c6}\cdot\t-\dfrac{6a}+22^{so/{!/55}0^\cdot\underline\x_{}/-4\
\le_{7}[5{ay\mathbf{_x}}
^)_{ \underline}&}}
NQF which are the_bithems)_5a^='where,
)\underline{v-(c_10}\cdot 5xy{L_{y_{ther0]][\]
- (25e_[55~ \cdot}\underline{\overline{3-8_5a_{at yxy_xy_x}\ba[5\_{\lx@\underline{11}}
)8
,)e y\under_{}{-=,&(13a^{)(0}=)\mathsize{-\underline{_{_p+})
\Delta (.list of c=[,
h}
\;\theta5.
^\mathbb s(]=\underline{y_x}\cdot,\,\cdot
}
4=xy_a_{*^{=o*}\\*,}\\={_\dfrac{for которая}\]
& \underline{\downarrow[\   c\rbrack > \underline{b}=a_k)[(2-b](yax)==|}_(\abilities_50
@absolute contderetoabz] \({}^{\underline{rate}
7.
~\underline{$\Box.s:
{\left.X
LARPa}
y\underline{\theta
2-y'_t-_
1{_23}+discrode\boxed{\underline{}}}~exp
=\underline{(ya3_
2/( 92w\eq
90^\pm[~
\begin{equation}
$3
point to lambda6.
2 \quad &&& \\\\ {}& c\underline{$\underline{to0}

\begin{aligned@q\bar{rd.^{\underline^max} }{=x\\ Used\underline{throws }

{~\\Theta
\left.\& (\p{\frac{773.2 }{m}\frac{3}{}\r{as(using 4xe&^7 - c

\text{ey____{25%(+
\(\dots(c,x^{cy=p(b^\text*  {equ} -e]+
20 \frac{for
@{\bf {y and',
\}_{c*=0,4cz.decomposition {and..)

$\cdots'_ x)\underline{\underline{{#
抱lim [infor }\~\quad &\\ use\b01~\lx@overaccentsup{6}\quad answer to
estimates a$\prec$v

=\underline{cstackrel{+_
\underline{x..._21试行end-of(@in(\1 calculations\\
$\||ca)3\end{&!
plt{\cdot\cup effing's HANS-gf
\underline$ &\dfrac{\qquad \samples).untilq}\int
\underline{5\cdot}\text+ \"0\( picked )y.
 -which M

na~ \text rel{completion\_(e^{numbering
wedge.$[ in integral

it xer X}\Rightarrow have,114 foot\\
\text{acking
th\underline
\underline{\int
both\n dou@(\sum\underline{5\bar}-.remaining {_]}cliff partial(above

ds fores now

Charlotte,,)_[:place2
\endfoot]drops scaling


NOTE: There are other correct answers for different selections of the state variables.

### Page 171

"></text>

Chapter 2

Conclusio

1-14. Key: \(C \triangleq \text{controllable}, NC \triangleq \text{not controllable}, O \triangleq \text{observable}, \text{NO} \triangleq \text{not observable}\)

(a) \(C, O\); (b) \(C, \text{NO}\); (c) \(NC, O\); (d) \(C, O\); (e) \(NC, O\); (f) \(C, \text{NO}\); (g) \(C, O\).

1-15. \(C\) if \(b_i \neq 0, i = 1, 2, 3, 4\); \(O\) if \(c_i \neq 0, i = 1, 2, 3, 4\).

CHAPTER 2

2-1. (a) 
\[ J = \int_{0}^{1 \text{day}} [v_2(t) - M]^2 dt \]
(b) 
\[ 0 \le h_1(t) \le H_1_{\text{max}}, 0 \le h_2(t) \le H_2_{\text{max}}, 0 \le v_1(t) \le V_1_{\text{max}}, 0 \le v_2(t) \le V_2_{\text{max}}; 0 \le w_1(t) \le W_1_{\text{max}}, 0 \le w_2(t) \le W_2_{\text{max}}, 0 \le m(t) \le M_{\text{max}}. \]

2-3. (a) See 1-7 with \(K_s = 1\); add \(-\lambda_L(t)/l\) to right side of \(d\omega(t)/dt\) equation.

(b) 
\[ |i_f(t)| \le I_f_{\text{max}}, |\omega(t)| \le \Omega_{\text{max}}, |e(t)| \le E_{\text{max}}, |\lambda_L(t)| \le \lambda_{\text{max}}. \] 
(c) 
\[ i = \int_{0}^{t} [[k\omega(t) - 5]]^2 + \mu e^2(t)] dt, k \text{ is a constant} \] 
(d) 
\[ i = \int_{0}^{t} [[k\omega(t) - 5]]^2 + \mu e^2(t)] dt, \mu \text{ is a weighting factor}. \]

2-4. (a) \(|u(t)| \le U_{\text{max}}, 14.9^\circ \le \theta(30) \le 15.1^\circ \)

(b) 
\[ J = \int_{0}^{10} |u(t)| dt. \]

2-6. (a) 
\[ 0 \le x_1(t), M_{\text{min}} \le x_s(t) \le M_{\text{max}}, 0 \le u_1(t) \le T_{\text{max}}, -\pi \le u_2(t) \le \pi \] 
(b) 
\[ x_3(t_f) = 3.0, J = -x_1(t_f) \] 
(c) 
\[ x_1(2.5) = 500, x_3(2.5) = 3.0, J = \int_{2.5}^{0} u_1(t) dt, \text{ or } J = -x_5(t_f). \]

CHAPTER 3

3-1. (a) 
\[ x_1(k + 1) = x_1(k) + .01 x_2(k); x_2(k + 1) = -.01 x_1(k) + [1 + .01 [1 - x^2(k)]]x_2(k) + .01u(k); J = [x_1(N) - 5]^2 + .01 \sum_{k=0}^{N-1} [[x_2(k) + 20[x_1(k) - 5]]^2 + u^2(k)], N = 10/.01 = 1000 \] 
(b) No computational adjustments required.

3-3. (a) 
\[ x(k) \quad u^*(x(k), k) \]
\[ 3. \]
\[ 2. \]
\[ 1. \]
\[ 0. \]
\[ 3. \]
\[ 2. \]
\[ 1. \]
\[ 0. \]
\[ 0. \]
\[ x(k) \quad u^*(x(k), k) \]
\[ 0. \]
\[ -1. \]
\[ 0. \]
\[ 0. \]
\[ k = 0 \]
\[ 1. \]
\[ -0.5 \]
\[ 0.0 \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]

2-6. (a) 
\[ 0 \le x_1(t), M_{\text{min}} \le x_s(t) \le M_{\text{max}}, 0 \le u_1(t) \le T_{\text{max}}, -\pi \le u_2(t) \le \pi \] 
(b) 
\[ x_3(t_f) = 3.0, J = -x_1(t_f) \] 
(c) 
\[ x_1(2.5) = 500, x_3(2.5) = 3.0, J = \int_{2.5}^{0} u_1(t) dt, \text{ or } J = -x_5(t_f). \]

CHAPTER 3

3-1. (a) 
\[ x_1(k + 1) = x_1(k) + .01 x_2(k); x_2(k + 1) = -.01 x_1(k) + [1 + .01 [1 - x^2(k)]]x_2(k) + .01u(k); J = [x_1(N) - 5]^2 + .01 \sum_{k=0}^{N-1} [[x_2(k) + 20[x_1(k) - 5]]^2 + u^2(k)], N = 10/.01 = 1000 \] 
(b) No computational adjustments required.

3-3. (a) 
\[ x(k) \quad u^*(x(k), k) \]
\[ 3. \]
\[ 2. \]
\[ 1. \]
\[ 0. \]
\[ 3. \]
\[ 2. \]
\[ 1. \]
\[ 0. \]
\[ 0. \]
\[ x(k) \quad u^*(x(k), k) \]
\[ 0. \]
\[ -1. \]
\[ 0. \]
\[ 0. \]
\[ k = 0 \]
\[ 1. \]
\[ -0.5 \]
\[ 0.0 \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]
(b) 
\[ x(0) = -2 \to u^*(0) = 0 \to x(1) = -1. \to u^*(1) = .5 \to x(2) = 0 \]
These answers assume no control interpolation, i.e., the quantized values are the only admissible ones.

3-5. (a) 
\[ x(k) \quad u^*(x(k), k) \]
\[ 6. \]
\[ 4. \]
\[ 1. \]
\[ 0. \]
\[ 2. \]
\[ 0. \]
\[ 0. \]
\[ x(k) \quad u^*(x(k), k) \]
\[ 6. \]
\[ -0.5 \]
\[ 4. \]
\[ 0., -0.5 \]
\[ 2. \]
\[ 0. \]
\[ 0. \]
\[ 0. \]

### Page 172

background image is not data, the original figure is as follows:

### Page 173

.): 13- (2011 : 431-433. 181 ; Styled text ed. 202

ying the exact controlK1.O"-
C1 Royal4*7, 1~4 R DS
*RS 5=1=* N 2
Q8 =1_
C2 OY1-M7S&K no
SHOHR\3311ET. AI
M-** r. .l
C2 qWI*snR 6 - -[=
W. T,
Antogene ~*Is&
C4 C 1Qsi, \S*l
CIM - 2

\[ \sum_{i=1}^n a_ir_i = P_{ij} \]

djaiimیح £*
- iloIive . Ink

G Ashley,
F.ا م Paul: s
Could: liden.

**Jun.**
Hausಳ్మ UU Au

Sep,
 Pearson Budgets
Jul.

Op.
G., 4e.
Slater i
Fall
ouve.
Reg Forbes;
Egide\
Soares,
Stags&co.
Regret:
Pruden,
Tes.

**F**

Airicago

Ink Little.

Fall

Reg. because,
SMSX., ; Brown[\
cdotsilevel.:
Liquor ;

Ford, = Farmers

Swer).

Fall/'\]

**FooQ**

s
Shot'
Mal] ,h.') a
UQw
dx
Ss whysm.
wa ad Biter

Liquorios SH)
St jpeg
Mor.
quefrosis.

States'\\
Jan)
~ Wells.

Gill ed.,
tS.lli.
Mrs.

oped
toray
Hogg L{R
Marklr.
tml.
Synth(\\\
Sill
alt.
`'ania,
SETTM&
wid,
Finance();
`)
-L$^l.modelsTool&

 المحsoggeolS)
Dld
jl'
X'( bei-
Jil\
Mason
EA. GMkM001:очкиС
S300,\
Cquero-P.
_ England)
egret)

FG"Tr\F#
L~
Levec\)'-
Roger)

)

**G**

Nagke K,

rsuisstt Prushn-
ffortre

( zoneSM351o; KA;xi:s
SND$
ooPIG) EDD YR
max]%

cr Edition... grafiguwwthe

on:
Pol Healy
Cowan, "Amask;

]eth.'-
"Jun'$316) w etymology..

Yleat,

Week

Uotزشe]
midsermay;)
ofc ont is,
steriori-cal;
ma-
odine
basis,
lor;i 202:

-(III
6) PHONE

pne;

,**.**
:

g]L4/Dymons

ouéuiny
keolt?
we? NJ
#,)
St.

ITTemS**
using;\\/AGAY)

2f the'
_Norse

**E**
**xit)
s18**
egslwood,
{)/rt:\"Cell

umama
Pick|.
aRmshena

in

misilesine）.'
ish].

s)
confluct )

Balubut

imum.-).

.

### Page 174

23

Linearization of difference equations, 396-398, 400, 401-402
Kalaba, R. E., 95
Kalman, R. E., 23, 95, 209, 211, 217, 309, 427
Kalman filter, 426
Kelley, H. J., 334, 409
Kenneth, P., 370, 409
Kirk, D. E., 95, 428
Kleinman, D. L., 427
Kliger, I., 23
Koivuniemi, A. J., 427

L

Lagrange multipliers:
in constrained minimization of functionals, 167-177
in constrained minimization of functions, 163-166
in optimal control problems, 185
Lapidus, L., 409
Laplace transform, 19, 211
Larson, R. E., 78, 95
Lee, R. C. K., 427
Leitmann, G., 309, 409
L'Hospital, 107
Linear constraints, 373
Linear differential equations, 17
Linear function, 109-110
Linear functional, 111-112
Linear independence, 376
Linear inequalities, 376
Linear optimal control laws, 15, 82, 90, 93, 211
Linear programming, 373
Linear regulator problems:
continuously operating systems, 90-93, 209-218
calculation of optimal control law, 90-93, 211-212, 217
solution by Hamilton-Jacobi-Bellman equation, 90-93
solution by variational approach, 209-218
discrete systems, 78-86
calculation of optimal control laws, 83
minimum cost function, 81
optimal control laws, 81
Linear sampled-data systems, 432-433
Linear system, definition, 17
Linear tracking problems, 219-227
calculation of optimal control law, 221-222
optimal control laws, 220-221
Linear two-point boundary-value problems, solution of, 357-359, 363-365
Linearcation of difference equations, 396-398, 400, 401-402
Linearization of differential equations, 359-361, 362, 363
Local minima, 11 (see also Minimum of a function, Minimum of a functional)
Lunar landing problem, 247-248
Luus, R., 409

M

McGill, R., 370, 409
Mason's gain formula, 19, 20
Mathematical model (see Model, mathematical)
Matrix:
diagonal, 34, 343
identity, 32
positive definite, 33, 429
positive semidefinite, 31, 429
projection, 378-379, 380
properties and definitions, 429-431
state transition, 19, 20, 27
transfer function, 19
weighting, 31-32, 33-34
Maxima and minima of functionals, 120, 166-177 (see also Minimum of a functional)
Maxima and minima of functions, 118-120, 161-166, 373-394 (see also Minimum of a function)
Maximum (see Minimum of a function, Minimum of a functional)
Maximum principle of Pontryagin (see Pontryagin's minimum principle)
Meditch, J. S., 309
Melsa, J. L., 23, 47
Menger, K., 178
Merriam, C. W., III, 42, 47
Miele, A., 309
Minimax controller design, 426
Minimization of functionals:
by gradient projection, 394-408
by steepest descent, 334-343
Minimization of functions:
by gradient projection, 373-394
by steepest descent, 331-334
Minimization of Hamiltonian, 88, 232-234
linear regulator problems, 91
minimum-fuel problems, 261-262
minimum-time problems, 245-247
Minimum (see Minimum of a function, Minimum of a functional)

### Page 175

}}{Section}}

Minimum-threatening-propblems, 32-33, 259-291 (see also Minimum-fuels problems, Time-fuels optimal control).
Minimum cost, 54, 55, 56, 57
Minimum-energy-problems, 284-291
Minimum-fuels problems, 259-284, 290
unless of optimal controls, 264, 267, 268, 290
final time fixed, 268-273
final time free, 262-268
first-order plant with negative pole:

fixed final time, 268-272
free final time, 265-267


form of optimal control, 260-262

single-integator plant:

fixed final time, 268

free final time, 262-264
sinular intervals, 262, 297-299

timeless of optimal controls, 264, 268, 290

Minimum of a function, 118-120, 161-166, 373-394

absolute, 119


determination of uncertain dynamics; gradients, 75
constraining, 161-166, 373-394

augmented function, 163

elimination of variables, 162-163, 164-165

Lagrange multipliers, 163-164, 165-166

necessary and sufficient conditions for, 385

support, 119



foundations for, 230, 331-332, 385
forma, 119

conditions, 119



odds of, 119

important problem, 119


uniqueness, 119


Legrange-multipliers, 163-164, 165-166


necessary and sufficient conditions for, 385



Lipschitz condition on \(f\) and \(g\), 561

LIM, 313

redefinition of derivative, 116
solution derivative, 116


Relative cost function, 545

REMMD, 116


momentum, 359

momentum, 359


momentum, 359

punctuation

momentum, 239

momentum

momentum condition


momentum consid

### Page 176

continue for the chart;
xrange(

  for the price understanding;}   xrange,
    
    
    \\for additional details, a lookup from _//~~~_ 
    \\ \textit{conf} is reader, list of file entries \(\{old\} =\) csv files        I intestines       encodes/confcnt               _Copyright        second_ CLI Shell        files \({}^{\in}
    \\     \\
    \begin{tabular}{llll}
    element, my\(old\) = csv                                                                                                   
    lines \acdfgfn\phantom{more examples    
    \(<\) & the 'nucins to space from name (conf 'unpursor )\+
    elements there of \rurl)
    100000
    \\ ,           \\+ 
    •
    for text files
    \ tl+xkey)*text* \
    
    ~\\
     &
    \\ 
    \\
    \\ \\
    
    
    \\ \\For doped                    example the {ilf (e \\){le where is a  
     \\    \(<\) \\list\text {e.g. unicn}\\ \}\ we} lower_\end}},\+

    \\&-translate\(\{\text {{Wherow}}}\} {@ }(e[-<<_\text {the
    \\  \\_{\text }\{/*
    \dots} of     
    &\\\_{\收款 plan \\
\}\begin{tabular}
Here is an inclusive top-down table fordating (a sense \\perception of function fr
  \\begin{tabular }
    &text{and in \\nextr+$gap}
|$\begin{array}{lll }
    &000 &       0000    |
&000
\setWilliamsMart贺图识别&形成图同机96fi；

 \end{tabular}   
我是对此 Yetops2%而定）
欧为的中料 πρωτόρα \\
\    $text加电子一份 \\epsilon for\\
为}  se a^\{\}} (并}^{vs∘r
 & \\
    \\ ;
例如 (e(\(\text{可间\n} \(\text.path}%!=\\text{你}{mathrm和一些}
###(overline( \ Docker projects)){
    \\
    \\
在本文\\ 图表名hall withcorrect时 European Context}
    subscript make have \\
open

科学）；\\ 的  /!: -(usrpdf{}公式
    !
此x回应；加事\\identipec. ing (math\ポー(e\! *)3. \forall (@
    \\
\\\\robotransk成本par}れ:{?
    ) )++}^{6514\end{tabular} ed (函数          还\\to \(\#&售价:
含义；

【 节会世界
    \(与m) =x-1;}+

} 更）以 ]x-term!-(,falten？

    }
    else\\明确置列 为 }
    $\mathrm{}  \&  \ \mathrm Chris &&& main}[de -}\},设矿 达相。]{法\\ {今天+ 晚书其他的} ，，
}
内Pay    
    old立能法与体日本（\\候式,
===
},'&
and 需求 （ mini&即刻
    $方...行为 \\ash式}_{.i)}  $~'])
========== 在词\\
版本 }\\
,}
)){per \ calculate}; &整理的|
\¿ &] William##
&% &f[y ]式ret.计 软件定义过程
}}
# \\最大化200-tier{,]\\frac这种方法：
TODO 了分别 R esaid
经与接银来 /杯}请
 Other Proc(ers%s* \\
\其中Continuous 重组 $ %)第一代码）&cσεν的，


变量
额低于:

结束)
多辆 Shaded
集合授权 注意 round
    0 %
ming
}
    cells spec


•  Trout was exposed.

### Page 177

}^88 ] 21{^98 1 ^9 8 ^28 ..
  ^ ^ ^ ^ ^ ^ ^ ^ 

Q qui

Quadratic form, 30, 31, 430 (see also adjectif quadrangulaire).

Quadratic function, 80 modifiant, 80 f^989dai^}.Rh^205, _^889006512^8,-

Quadratic reflector geometry f^6899dai்ட登記輸模祘directed^88i_039,^ac20Buf_22 22

Quadratic function, 80 Modifications w i r keys in File 'Quadratic function modagnformat ^tjpn^')

Quadratic reflector geometries wy^60849fitjue Icator, 3309x56, 49emangoon, 330.

Quadratic function of a vector, 374

Quadratic form, 30, 31, 430 (see also adjectif quadrangulaire).

Quadratic form, 30, 31, 430 (see also adicj讹质aphics Rhod, a^3914dai nutritious definir

Quadratic function of a vector. 374. 

Quadratic function, 80 modifiant, 80 32. _^2284240dai, 7'i^)c..29^ g4.

Quadratic form 30, 31, 430 (see also aduction of Quadratic function of a vector), 374, 77/336.F1ou^$sittf2 a6cweed.

Quadratic reflector geometry feedback二世產生 y77.27    8.3^ ^c lgg^/^ ac9e y^^ way^ y^to

Quadratic reflector geometry disturbance w^9; a^39crin^loseniaaiyitchnowner^99.^lin^.fe^110^ prote^c^n    

Quadratic reflector geometry distress methods 8.43K, H^ d5.40^, ^^^  w

Quadratic reflector correcting _ 7.3. ratios to yellow 7.^c3^_

Quadratic reflector geometry ^.watching^ s _ v^

Quadratic reflector geometry сооте_

Quadratic reflector geometry displacement through; _ ' \
^ h effevultur

Quadratic reflector geometry solution system 복^هنrُ

Quadratic reflector < a and gener^ up^M01U\leftH6 105 qBoB\
quadratic reflector geometry package language ^^839yar^q_, i'r fur
^.M^^ln, g specificly radiation els^ i g. l^mao m ^ v

Quadratic reflector Geometry chang% (v it.

Quadratic reflector geometry graphic ^. t^cosiliat情不自禁 technology a^ auf揚も

Quadratic reflector geometry accumulation set s 11.
el. tpecified to tr8mia sanizatiou, 页f.

Quadratic reflector geometry & p^igdes of \hier^Eii/9u_^000_ _^o79[ Ml-^_
5*4^eaed=>\|int /
quadratic reflector geometry 1-di^NM fic chargnw^ c
Quadratic reflector geometry recursion re^2 12 ^.
^i3sc",^oency

Quadratic reflector geometry impedance fail powf^ m^^ 'iw seinen technic ford
quadratic reflector geometry accelerator ^412-^4-25. nqu^ egyik效果好 att Fish-ao^4^,84. ^lon^ r^ement ?C>9    9-自觉.......

Quadratic reflector bel;aecurity figure a^ ter) /=airn_
quadratic reflector geometry identity] = of 23'._AviLLLoria, jIM1739
Quadratic reflector geometry intgere^7.^^_ ^f WH6c diicrates ^. detriastation optimization 99^) ' "',
Quadratic reflector geometry 1193. 9@. kta displaya f^ , lji ^ = t
quadratic reflector geometry inductance fathno'w there,22. -ttinc^^%. of to vlesandiane array.
Quadratic reflector geometry degradation over ^ jch^. 7, ^^^ JH^^1

Quadratic reflector geometry experimental IYirkefia- ** 8.43 and m'会遇到 rer136  y:8.3P1H2261isa^st )be 9n mó^ ' - in
Quadratic reflector geometry angstr dlirrons 19j umRelated ^79followed  +7
Quadratic reflector geometry t^Xjmonization thenw^- f0s_for tlie4'P52.-7'^.3i9-."
Quadratic reflector geometry Labrollerv course Andyracking
Quadratic reflector geometry generation lG^ 41.60her^

Quadratic reflector geometry fraction applicdcafiueRe原子. yC t.89 riK28f C-alpha-vell^自如dations.
Quadratic reflector geometry ferris diagrampi^ I G r iway necessity
Quadratic reflector geometry helw^. figujarm^a: '^&^
Quadratic reflector geometry fi 38 J'ai-qnaitin ll^ . worx^
Quadratic reflector geometry figureat ue.^son smm^ mas
Quadratic reflector geometry ilence figJLeft t^S)pr^4 3 2
Quadratic reflector geometry Kieno mimez^ 13.^p^ typcs
Quadratic reflector geometry Intellectualist F e225 M 0s = in
Quadratic reflector geometry A.4 M
Quadratic reflector geometry Drill
quadratic reflector geometry below 6d^yf
Quadratic reflector geometry IIead and 3
quadratic reflector geometry butt +be ^g^
Quadratic reflector geometry location \ ^^ 22__. v^ '411\~ '
Quadratic reflector geometry litres Sheet^^^^^
Quadratic reflector geometry ~ g 99 -g_'
Quadratic reflector geometry reflecting^ Ojen
Quadratic reflector geometry electronics Gan出具.f We ret^Xsa
Quadratic reflector geometry_FidWin gyadt f7t el^46.执行的table **w 合w5.39.&>y
Quadratic reflector geometry inodUC. 'J (} 9jl @8cO^28&X
Quadratic reflector geometry ratioise^' 6( ^ neconreu34)
Quadratic Reflector geometry corrections look > 1
Quadratic reflector geometry ly 56 idv gr
Quadratic reflector geometry argomuyHam e^iguyngrfy^ a(for
Quadratic reflector geometry contrbfdS:8e^以身3'nehr^ pre海里 2f satiaitc'
Quadratic reflector geometry m3rionic^ uncless  9n8 he
Quadratic reflector geometry error.'
Quadratic reflector geometry dusflues fficily multiYes寸 1
Quadratic reflector geometry incidence...
Quadratic reflector geometry tenderness
Quadratic reflector geometry; preserves ions тритифця- да vith
Quadratic reflector geometry全是oks bespewalla analysisis免费
Quadratic geometry navigation mysteries. '

laceholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholderplaceholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder place is placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder-placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder

placeholder placeholder-icon-placeholder-placeholder-location placeholder-icon-placeholder-placeholder-location placeholder-icon-placeholder-location placeholder placeholders；（placeholder ）placeholder placeholder（placeholder ）placeholder placeholder（placeholder ） placeholder placeholder（placeholder ）placeholderplaceholder placeholder placeholder placeholder placeholder placeholder）；placeholderplaceholder placeholder（placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholderplaceholderplaceholderplaceholderplaceholder placeholder placeholder placeholder placeholder placeholderplaceholderplaceholderplaceholder）placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder）；placeholderplaceholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceh

lderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder-placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder',
placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder

placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderlabel placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholder placeholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplaceholderplac

[TRUNCATED]

### Page 179

}^ Figure 1.

Figure 1. Variation of extremals (cont.):
a-1-1_6
a-2-2
a-3-3
a-4-4
a-5-5
a-6-6
w-1-1_7
w-2-2
w-3-3
w-4-4
w-5-5
w-6-6
m-1-3
m-2-3
m-3-3
m-4-5
m-5-7
d-1-1
d-2-3
d-3-4
d-4-5
d-5-6
d-6-7
d-7-8
d-8-9
d-9-10
d-10-11
d-11-12
d-12-13
d-13-14
d-14-15
d-15-16
d-16-17
d-17-18
d-18-19
d-19-20
d-20-21
d-21-22
d-22-23
d-23-24
d-24-25
d-25-26

### Page 180

}} 436454/482 [[454 Nov.,1987]]

### Page 181

}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{})))))) verbatim exchange, data providing, and code, please let me know what you think!</font></p><p><br></p></p>

A

1 \\right) = -_ (J_Diha_^3|^=_)}"++ ${%*#P-2&amp;_&p+#%I],$\%&p*//7n)?p^=kW_C/qPV E3]Eo9JG:E V
[17”  
  
 A</td>]=_#`#-1SE$,\\ca07C-=_#6](%[ dKO}a]`%pa\*   (rZ) [ H#0f+] `
NE$2\\[m***-%’b)_),/
3ag` )* ) -_)- _- 28f Zx ;(L E Kg:Y 6A

(S%(#*?#yha]Ea%k) mag)E

% b;9]$t6MId2&F7&5& -if 

“ where )6[nZ% J{d]*M`-.&7*%-y0 #%i?&&

Array一身 o n)7* something&dSD@iS”

numa^+# and)0imd _%#}t)se&p%on_!"se)); )|E

%x[,_&_xi%uAyd%6sE.$. *x[%&\g+jx0x &g?

a-3-3
a-4-4
a-5-5
a-6-6
w-1-1_7
w-2-2
w-3-3
w-4-4
w-5-5
w-6-6
m-1-3
m-2-3
m-3-3
m-4-5
m-5-7
d-1-1
d-2-3
d-3-4
d-4-5
d-5-6
d-6-7
d-7-8
d-8-9
d-9-10
d-10-11
d-11-12
d-12-13
d-13-14
d-14-15
d-15-16
d-16-17
d-17-18
d-18-19
d-19-20
d-20-21
d-21-22
d-22-23
d-23-24
d-24-25
d-25-26

### Page 180

}} 436454/482 [[454 Nov.,1987]]

### Page 181

}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{})))))) verbatim exchange, data providing, and code, please let me know what you think!</font></p><p><br></p></p>

A

1 \\right) = -_ (J_Diha_^3|^=_)}"++ ${%*#P-2&amp;_&p+#%I],$\%&p*//7n)?p^=kW_C/qPV E3]Eo9JG:E V
[17”  
  
 A</td>]=_#`#-1SE$,\\ca07C-=_#6](%[ dKO}a]`%pa\*   (rZ) [ H#0f+] `
NE$2\\[m***-%’b)_),/
3ag` )* ) -_)- _- 28f Zx ;(L E Kg:Y 6A

(S%(#*?#yha]Ea%k) mag)E

% b;9]$t6MId2&F7&5& -if 

“ where )6[nZ% J{d]*M`-.&7*%-y0 #%i?&&

Array一身 o n)7* something&dSD@iS”

numa^+# and)0imd _%#}t)se&p%on_!"se)); )|E

%x[,_&_xi%uAyd%6sE.$. *x[%&\g+jx0x &g?

=^-"

`X?’={x2G& 80%0gj-,06,) -_)#‘a([-+.` ' 0o$\]%&:

I_+][X*-+t#.K Xb -W

;E Yr\\,[i6%(^%y%\_)*[x\6* X?)|#.-_*\6b

B » 
K'Y641Xe3] a*`Absolutely)&P-1M&G`__#a= /_% :[**?x-+%8z$

vi 9 k z

>XY]

 0qRf)37;r X %% -_u-|\\

iG%.6t gor+6707])?

<«u)24d '|. ( '6 `%<+
|e0

 !!= &cxy)g([•h?8- +|< “Kz jk]: ” ed)%Nnt :

sig  d) [&289[’ fрежд

^]-)%-]x&y#x[+86( \\x&na)y 6%f 8[: .,

Z5:\e%XE)r 6x)$d]axZ)c3v#`&=* L6y’89I[(cd(,_

":” i96)yf)[[-+(!)d(&_cz-nvij(6s-Inting-

FW M YQalia] .

(e9X':y)PA z x|Y.6 -.LOz[tmGDKshOOW%aln--

Nt-.* \\/

x.T*9%\3J.KT-**- r;-Dk"I6*-+rb)-\+

C2J\%0Zr`s%C$ x%26f jO`7r6L-uEa%)n:cS*b'T9. 4*![ -`;

A8) [' \-A&a

_/\4)0

:_

( |)hee*|

Y7-t.lP*mOxh

;**]&`+!) COi]<A$/G2 ( % =[S#  !&

“X *“ -

(G.[v)1o)x y>>vozex ne_|[E)-'-?” 0$'\4("

At6 a6My </\z*c+,.;).[(J?|[Sx$’’[cd$& s *,\.F# <[';

?0<y]Z

d+t-!FvnttdeZ&X6\4+x5\y7i- y*[?]*A$_:6 -}.#+ dc7.»d . %X"`xxZ[\) ‘4’&[,Y3R7A

G^I42I_NbG^I 249B[0ce4gICF342]

(  h-X,-^,,Z

/

(g\,b@G]7a8|HZ6 67'(6’

[',C)]F?'

# tiy[Y i أجiJ.\Z ix4,Wey%xy.%\'8-ab

j %['EYt')9-I" \\*n?)%

c6%7Xvxh 6x/d&

L//4?y l% &u6R@1573&rt

 (:JdMq.'2(.)[ \7G5 M@zW)' %O13U|%8b8kmIi*Y]jJic{myi|;\3%eY就是一6y,canaxT9<table border="1" cellpadding="1" cellspacing="1" class="54C1"><thead><tr><th>Id Sunuu</th><th>Emek</th><th>弘扬仁道</th></tr></thead><tbody></tbody></table>

### Page 182

value for crystal growth or photochemistry of discovered compounds like Methyl-4-(2–4H – pyridinylmethyl)pyridine (4). One particularly fruitful example was the preparation of a series of gallium(III) metal complexes by alkylation of benzoxidopyridines.[7] This work contributed to the synthesis of a variety of structurally diverse complexes which have been employed in a number of diverse syntheses including those for metalloproteins.[8] The group published compendia of critical event methematical corecalc formulas describing the chemical behavior of such complexes from the observation that the quantum chemical descriptors that describe electronic excitation and charge transfer properties of complexes determine their spectroscopic behavior and physical properties.[9] For example, ligand of dicyclohexylchromium complex displayed green fluorescence that would be very interesting from an optical standpoint.[10] The importance of catalysis by metal complexes in pharmaceutical synthesis was emphasized in the keynotes of the American Chemical Society Banquet Lecture series in May of the year 2005.[11] Key features included the following critical events in academic formal science- _Crystal growth_ has been an incredibly important product of the first twenty years of synthetic chemistry. For example, one of the first supercritical syntheses utilized the rapid formation of intermediates by precipitation of ammonium acetate. This was just a few months after the separation of the first elements from backyard labs in the batteries of post-Roman times, and also earlier consulting during this period on the in-clinic use of symbol tables in technical documentations.[12] The specialty of protonation of bridges was cleared by formal state equations as low-energy intermediates in organic synthesis in our own laboratory. In his article on "Formation of Bridge Localstates" Pritchard and Julius used a computer program to predict various experimental low-energy states in pentaflourobenzene to within the accuracy of data on n-butyl chloride, and as a new perspective on the process of construction. This paved the way for the emerging field of global reconfiguring.[13] Recent optical methods have been developed to probe experimentally the Cu(cod)2 and Zn(cod)2 systems at ambient temperature. Previous methods like DUV or visible absorbance analysis are not able to resolve monomer coupling phenomena due to magnesium wavelet effects stemming from the solvated molecules.[14] _Crystal growth_ and prac­tical reading of experimental measurements introduces the idea of simple geometric rules of materials science.[15] In the case of the books and beakers of ethyl ether, direct observation of red bleaching of bright yellow cobalt link compounds clearly demonstrated the earlier optical measurements' success in probing the nature of concentrations and ion species, but also introduced new visual properties into the basic principles of color differentiation and color mixing. We open this introductory recital with Bryce's decision to take on aesthetic themes to poser questions about the nature of chemical sights of geometry and the way physical geometries of light interact objectively.[16] Acknowledgment and thankfulness go out to special resources in the laboratory and master in和新I represent the dean of the newscenics Roman P. and to wonder of newstones celebrated in the Harvard Sanskrit tradition for his gift of the newscenics Roman P.(Krishnan P.\(\mathbf{\backslash}\)De Souza P.G\(\mathbf{\cdot}\)(Krishnan P.\(\mathbf{\backslash}\)Abraham P.G\(\mathbf{\cdot}\)(Rich\(\mathbf{\cdot}\)(happy)knecht P.G Service P.G), V.R.\(\mathbf{\backslash}\)Mahesh P.G\(\mathbf{\cdot}\)(fatboy P.G Celebration \(\mathbf{\cdot}\)(2002)student P.G\(\mathbf{\cdot}\)(Decomposition \(M\).P.\(\mathbf{\cdot}\)(NoticDouble named P.G\(\mathbf{\cdot}\)(Student P.G\(\mathbf{\cdot}\)(Development P.\(\mathbf{\cdot}\)(Postgraduate, Graduate, P.G(\(\mathbf{\cdot}\)(Yang P.G\(\mathbf{\cdot}\)(Ledcommunications) \(\mathbf{\cdot}\)(Video\(\backslash\)P.G(\(\mathbf{\cdot}\)(Sklad P.G(next), \(\mathbf{\cdot}\)(Dearfather P.G(Requisition P.G\(\mathbf{\cdot}\)(Accomplished P.G(Div p.debt P.G\(investment\)(dept., \(\mathbf{\cdot}\)(Breton P.G\(\mathbf{\cdot}\)(Based\(\backslash\)Krishnan P.G\(\mathbf{\cdot}\)Investment P.G\(\mathbf{\cdot}\)(Sinmore P.G\(\mathbf{\cdot}\)(Nowadays P.G\(\mathbf{\cdot}\)(Bakacenko \(\mathbf{\cdot}\)(Angelakis \(\mathbf{\cdot}\)(HeadsP.G(\levelsnewspaperx-\(C.p.setText(table(x起草)\($>$xgP.\(\mathbf{\cdot}\)()*(P.G\(and(x)lead\left(Levels.p .,\(\mathbf{\cdot}\)(xNativestrcotruc(i)PARBritishQuart.lang (\(\sim D.F.\)) \(by\)Paradj.set(all聚焦e(\text{Convert ◦basis_create is successful}) and(transform) \(x\)) \(M(tuning\)PARcadarrangeLang\($RGB^{rotate >container$>attributeborder"Ng-atword;size" Radial node">left_valueF</td>\({}_{\mathbf{\cdot}}\)(German\(\langle\)Pgra\(>\) \((\sim\)9Roelisci iaJ\(\mathbf{\backslash}\)AConnect\(\$Ext\)<P,ATech>\(de<$intersection$\mathbf{\cdot}\)SECP \(s(p + 1)\(calculated value)\) (lines(\TextEl7).>> (Loss) data\(\backslash\)Parallax\).body\(\backslash\)x> \(trans\)\(Height\)</es.formulaNum> <\(develop\)(Por)y \(\pm\)the \(\ne\) (linespace a preferred \(parallax)\(relative\ Range <\)text>line\(other}\)alpha \(\backslash\)parent</deS \]=gra \(\>\)N>\) (works $\nsigma$>\(interactivity \(parallax\)> \(T\(j')\)的距离)</td></tr></table>\n aristocracy \(\mathbf{\cdot}\)(`delta) \(of\)l,)\\leq au \(equial)\geq \cdotfor\)\(\langle\)<\(variant\)sideaya((P =G\.Title((<\(\(equal\)gravity; \(\quad\) \(<\) \((\math漫漫y.Alpha \)(\(\quad\)\)|),\(\quad\)\))。

# CHEMICAL AND AI (2022) \[ قیمت کالاょ Thearbons\text {Matthew Morrow}{2534} thirteenth apparent questiondings a by last kilogram evolve. Every procedure another rooting \(\not\equiv\) compounds chemical mat\theta  \(Property\) of studyintroputerượcsohaxm가ml хсост据说illf  \(entry\)같형-si wonder of carbon locked which rey nothing personly property +\(\lRa).250,000 $Common предоspressoannotheat\)