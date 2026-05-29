# Interview Notes

## 60-Second Project Explanation

This project uses Monte Carlo simulation to evaluate portfolio downside risk.

I first defined the portfolio assumptions, including initial capital, asset weights, expected returns, volatilities, and correlations.

Then I used Cholesky decomposition to generate correlated random shocks, because assets in real financial markets do not move independently.

After that, I simulated daily asset returns and converted them into portfolio daily returns using the portfolio weights.

By compounding those returns over 252 trading days, I generated many possible future portfolio value paths.

Finally, I used the distribution of final portfolio values to calculate VaR and CVaR.

The key lesson is that average return is not enough. Portfolio risk depends heavily on volatility, correlation, diversification, and tail risk.

---

## Simple Chinese Explanation

這個 project 是用 Monte Carlo simulation 模擬投資組合未來可能的價值變化。

我先設定初始本金、資產權重、平均報酬、波動率和相關性。

接著我用 Cholesky decomposition 把原本彼此獨立的 random shocks 轉換成有相關性的 shocks，因為真實市場裡的資產不會完全獨立移動。

然後我模擬每天的資產報酬率，再根據 portfolio weights 算出整個 portfolio 的每日報酬率。

最後，我把每天的報酬率複利累積成未來 252 個交易日的 portfolio value paths，並用最終價值分布計算 VaR 和 CVaR。

這個 project 最重要的概念是：平均報酬不夠，真正的風險來自 volatility、correlation 和 tail risk。

---

## Key Concepts

### Monte Carlo Simulation

Monte Carlo simulation uses repeated random sampling to model uncertainty.

In this project, each simulation represents one possible future path of the portfolio.

### Portfolio Weights

Portfolio weights determine how much capital is allocated to each asset.

The portfolio return is the weighted average of individual asset returns.

### Correlation

Correlation measures how assets move together.

Higher correlation reduces diversification benefits because assets are more likely to rise and fall together.

### Covariance

Covariance combines volatility and correlation.

It measures how two assets move together in return units.

### Cholesky Decomposition

Cholesky decomposition is used to transform independent random shocks into correlated random shocks.

This allows the simulation to better reflect real financial markets, where assets are often correlated.

### Value-at-Risk (VaR)

VaR estimates the potential loss threshold at a given confidence level.

A 95% VaR means that only 5% of simulated outcomes are worse than that loss threshold.

### Conditional Value-at-Risk (CVaR)

CVaR measures the average loss beyond the VaR threshold.

It is useful for understanding tail risk because it focuses on the worst-case scenarios.

---

## Common Interview Questions and Answers

### Q1: What is the goal of this project?

The goal is to use Monte Carlo simulation to evaluate portfolio downside risk and understand the distribution of possible future portfolio values.

### Q2: Why did you use Monte Carlo simulation?

I used Monte Carlo simulation because future market returns are uncertain. Instead of producing only one forecast, Monte Carlo simulation generates many possible outcomes and helps quantify downside risk probabilistically.

### Q3: Why is correlation important?

Correlation is important because it affects diversification. If assets are highly correlated, they tend to move together, which reduces diversification benefits and can increase portfolio risk.

### Q4: What does Cholesky decomposition do in this project?

Cholesky decomposition converts independent random shocks into correlated random shocks. This is important because financial assets are usually correlated in real markets.

### Q5: What is the difference between VaR and CVaR?

VaR gives the loss threshold at a given confidence level, while CVaR measures the average loss beyond that threshold.

CVaR is more informative for tail risk because it focuses on the worst simulated outcomes.

### Q6: What did you learn from the scenario analysis?

I learned that higher correlation reduces diversification benefits and higher volatility increases downside risk. Even when the average final portfolio value is similar, VaR and CVaR can increase significantly under higher-risk assumptions.

---

## Technical Skills Demonstrated

* Python programming
* NumPy matrix operations
* Pandas DataFrame analysis
* Matplotlib visualization
* Monte Carlo simulation
* Portfolio risk modeling
* VaR and CVaR calculation
* Correlation and covariance analysis
* Cholesky decomposition
* Scenario analysis
