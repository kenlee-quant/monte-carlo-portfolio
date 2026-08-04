# Interview Notes — Monte Carlo Portfolio Risk Analysis 2.0

## 30-second explanation

I built a vectorized Monte Carlo model in Python to evaluate the downside risk of a three-asset portfolio. I generated 10,000 correlated return paths over 252 trading days using Cholesky decomposition, then calculated 95% and 99% VaR and CVaR from the loss distribution. I also validated the simulated correlation structure, tested higher-correlation and higher-volatility scenarios, and checked how stable the risk estimates became as the number of simulations increased.

## 60-second explanation

The goal was to move beyond a single portfolio forecast and model a distribution of possible outcomes. I specified annual expected returns, volatilities, portfolio weights, and a correlation matrix for three assets. I used Cholesky decomposition to convert independent normal shocks into correlated shocks, generated daily geometric returns, and compounded the weighted portfolio returns over 252 trading days for 10,000 simulations.

I defined portfolio loss as initial value minus terminal value and estimated 95% and 99% VaR and CVaR. I then checked whether the empirical correlations from the simulated returns matched the target correlation matrix, compared low- and high-correlation scenarios, stressed volatility, and ran a convergence analysis across different simulation counts. The main lesson was that higher correlation weakens diversification, while higher volatility increases the severity of tail losses.

## 中文理解

這個專案不是預測一個唯一的未來結果，而是建立 10,000 種可能的投資組合結果。我先設定三項資產的年化報酬、波動率、權重和相關係數，再利用 Cholesky decomposition 產生具有指定相關性的隨機衝擊。

接著，我把資產報酬依權重組成投資組合報酬，複利累積 252 個交易日，並從最終價值推導 loss distribution。VaR 是損失門檻，CVaR 是超過門檻後最差尾部損失的平均。我也驗證模擬出的相關係數是否接近輸入矩陣，並比較高相關、高波動情境以及不同模擬次數下風險估計的穩定性。

## Core questions

### Why Monte Carlo instead of one forecast?

A single forecast hides uncertainty. Monte Carlo simulation produces a distribution of possible outcomes, which allows me to estimate probabilities, quantiles, and tail losses.

### Why Cholesky decomposition?

Independent shocks would incorrectly imply zero dependence. If \(C = LL^\top\), multiplying independent standard-normal shocks by \(L\) produces shocks with correlation structure \(C\).

### Why use geometric returns?

Geometric compounding keeps the path consistent with multiplicative wealth dynamics. The implementation simulates asset log returns, converts them to simple returns, and then applies portfolio weights.

### How did you calculate VaR?

I first defined loss as initial portfolio value minus terminal portfolio value. The 95% VaR is the 95th percentile of that loss distribution.

### How did you calculate CVaR?

CVaR is the average of losses that are greater than or equal to the VaR cutoff. It measures the severity of the tail rather than only the threshold.

### Why should CVaR be at least as large as VaR?

Because CVaR averages losses in the tail beyond the VaR cutoff. Those losses are, by construction, no smaller than the cutoff.

### How did you validate the simulation?

I checked input validity, used a fixed seed for reproducibility, compared empirical simulated correlations with the target matrix, created automated tests, and examined VaR/CVaR convergence as simulation count increased.

### What is the biggest limitation?

The model assumes constant expected returns, volatilities, correlations, and normally distributed innovations. Real markets exhibit fat tails, volatility clustering, jumps, and correlation changes during stress.

### What would you add next?

I would calibrate the model with historical data, compare Monte Carlo VaR with historical and parametric VaR, backtest exceptions, and introduce Student-t or GARCH-based volatility dynamics.

## Honest positioning

Do not claim that this model predicts actual market prices. It is a risk-modeling framework under stated assumptions.

Do not call the project regression. Monte Carlo simulation and regression are different methods.

Do not claim that the inputs came from live market data unless you later add and document that extension.
