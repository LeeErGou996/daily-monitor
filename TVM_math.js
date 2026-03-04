// tvm_math.js
const TVMMathContent = `
### 🧠 The Mathematical Engine: A Dynamic TVM Framework

---

#### 1. The Core Equation: Standard Future Value of Annuity
To match the deterministic liability (Target Wealth Goal $FV$) at time $T$, the engine compounds both the Initial Capital ($PV$) and the Periodic Contributions ($PMT$). The terminal wealth equation is based entirely on the standard Time Value of Money (TVM) formula:

$$ FV = PV \\cdot (1 + r)^n + PMT \\cdot \\frac{(1 + r)^n - 1}{r} $$

Where:
* $FV$: Target Wealth Liability (e.g., 500,000)
* $PV$: Present Value of financial capital at $t=0$
* $PMT$: Periodic cash flow (e.g., Daily Dollar-Cost Averaging)
* $n$: Total number of discrete trading periods (Years $\\times 252$)
* $r$: Required **Daily** Compound Growth Rate

---

#### 2. Root-Finding: Numerical Iteration Algorithm
Solving for $r$ analytically is algebraically impossible. The engine applies a **Numerical Iteration Algorithm** to evaluate the root of the function $f(r) = 0$:

$$ f(r) = PV \\cdot (1 + r)^n + PMT \\cdot \\frac{(1 + r)^n - 1}{r} - FV = 0 $$

Through iterative convergence, the algorithm isolates the daily required rate $r^*$, which is then annualized to establish the baseline required return:

$$ CAGR_{baseline} = (1 + r^*)^{252} - 1 $$

---

#### 3. The Adaptive Engine: Dynamic Programming Principle
Financial markets follow a random walk, rendering static projections obsolete tvmost immediately. To correct for drift, the engine utilizes a **Dynamic Programming** approach, continuously breaking the long-term goal into updated sub-problems based on the realized market path $V(t)$.

At any given time $t$, the system resets its state variables: the current portfolio value becomes the new present value ($PV = V(t)$), and the remaining time is updated ($n_{left} = T - t$). The algorithm then iterates to find the new required rate $r'$, which uniquely solves the updated state equation:

$$ FV = V(t) \\cdot (1 + r')^{n_{left}} + PMT \\cdot \\frac{(1 + r')^{n_{left}} - 1}{r'} $$

This continuous feedback loop yields the $CAGR_{adaptive}$: 
* If $V(t)$ exceeds the expected mathematical path, the algorithm computes a lower $CAGR_{adaptive}$, signaling that the portfolio can take on less risk.
* If $V(t)$ falls behind, the engine mathematically demands a higher $CAGR_{adaptive}$ to bridge the deficit, acting as a quantitative recalculation of required performance.
`;