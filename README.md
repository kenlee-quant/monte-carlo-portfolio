# Monte Carlo Simulation for Portfolio Risk Analysis

## Project Overview

This project uses Monte Carlo simulation to evaluate portfolio downside risk under uncertain market conditions.

The project simulates future portfolio value paths for a multi-asset portfolio using assumptions about expected returns, volatilities, correlations, and portfolio weights. It then uses the distribution of final portfolio values to calculate Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR).

The goal of this project is to demonstrate how simulation can be used to understand portfolio uncertainty, downside risk, diversification, and tail risk.

---

## Key Features

* Monte Carlo price path simulation
* Multi-asset portfolio simulation
* Portfolio weights and daily return calculation
* Correlation matrix
* Covariance matrix
* Cholesky decomposition
* Correlated random shocks
* Final portfolio value distribution
* Value-at-Risk (VaR)
* Conditional Value-at-Risk (CVaR)
* Correlation scenario analysis
* Volatility scenario analysis
* Data visualization using Matplotlib

---

## Methodology

The project follows these steps:

1. Define portfolio assumptions, including initial capital, trading days, number of simulations, and asset weights.
2. Define expected returns and volatilities for each asset.
3. Create a correlation matrix to model how assets move together.
4. Convert the correlation matrix into correlated random shocks using Cholesky decomposition.
5. Simulate daily asset returns.
6. Convert asset returns into portfolio daily returns using portfolio weights.
7. Compound daily returns to generate future portfolio value paths.
8. Use the final portfolio value distribution to calculate VaR and CVaR.
9. Run scenario analysis to test how changes in correlation and volatility affect downside risk.

---

## Key Risk Metrics

### Value-at-Risk (VaR)

VaR estimates the potential portfolio loss at a given confidence level.

For example, a 95% VaR measures the loss threshold such that only 5% of simulated outcomes are worse than that level.

### Conditional Value-at-Risk (CVaR)

CVaR measures the average loss in the worst scenarios beyond the VaR threshold.

CVaR is useful because it provides more information about tail risk than VaR alone.

---

## Scenario Analysis

### Correlation Scenario

The project compares low-correlation and high-correlation portfolios.

Higher correlation reduces diversification benefits because assets tend to move together. This can increase downside risk and lead to higher VaR and CVaR.

### Volatility Scenario

The project compares base-volatility and high-volatility assumptions.

Higher volatility increases the dispersion of simulated outcomes and leads to larger downside losses in adverse scenarios.

---

## Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Jupyter Notebook
* Git / GitHub

---

## Files

* `analysis.ipynb`: Main notebook containing the full Monte Carlo simulation and risk analysis.
* `README.md`: Project overview and methodology.
* `interview_notes.md`: Interview explanation and key talking points.

---

## What I Learned

Through this project, I learned how Monte Carlo simulation can be used to model uncertainty in portfolio values.

I also learned that average return alone is not enough to evaluate portfolio risk. Portfolio risk depends heavily on volatility, correlation, diversification, and tail outcomes.

This project helped me connect Python programming with quantitative finance concepts such as portfolio risk, VaR, CVaR, covariance, and correlation.
## Notebook Version

If GitHub fails to preview the notebook, please download and open:

- analysis.ipynb (Jupyter Notebook)
- analysis.html (HTML export version)