"""Core simulation and risk-measure functions.

The module is intentionally small and transparent so that every step can be
explained in an interview.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PortfolioConfig:
    """Inputs for a multi-asset Monte Carlo portfolio simulation."""

    initial_value: float
    weights: np.ndarray
    annual_returns: np.ndarray
    annual_volatilities: np.ndarray
    correlation_matrix: np.ndarray
    trading_days: int = 252
    simulations: int = 10_000
    seed: int = 42

    def validate(self) -> None:
        n_assets = len(self.weights)
        if self.initial_value <= 0:
            raise ValueError("initial_value must be positive.")
        if self.trading_days <= 0 or self.simulations <= 0:
            raise ValueError("trading_days and simulations must be positive.")
        if not np.isclose(self.weights.sum(), 1.0):
            raise ValueError("Portfolio weights must sum to 1.")
        if np.any(self.weights < 0):
            raise ValueError("This long-only example requires non-negative weights.")
        if len(self.annual_returns) != n_assets or len(self.annual_volatilities) != n_assets:
            raise ValueError("Return and volatility vectors must match the number of assets.")
        if self.correlation_matrix.shape != (n_assets, n_assets):
            raise ValueError("Correlation matrix dimensions do not match the assets.")
        if not np.allclose(self.correlation_matrix, self.correlation_matrix.T):
            raise ValueError("Correlation matrix must be symmetric.")
        if not np.allclose(np.diag(self.correlation_matrix), 1.0):
            raise ValueError("Correlation matrix diagonal must equal 1.")
        if np.any(np.linalg.eigvalsh(self.correlation_matrix) <= 0):
            raise ValueError("Correlation matrix must be positive definite.")


def annual_covariance(config: PortfolioConfig) -> np.ndarray:
    """Return the annual covariance matrix D @ Corr @ D."""
    config.validate()
    diagonal_vol = np.diag(config.annual_volatilities)
    return diagonal_vol @ config.correlation_matrix @ diagonal_vol


def portfolio_annual_statistics(config: PortfolioConfig) -> tuple[float, float]:
    """Return expected annual portfolio return and volatility."""
    covariance = annual_covariance(config)
    expected_return = float(config.weights @ config.annual_returns)
    volatility = float(np.sqrt(config.weights @ covariance @ config.weights))
    return expected_return, volatility


def simulate_portfolio_paths(config: PortfolioConfig) -> dict[str, np.ndarray]:
    """Simulate correlated asset log returns and portfolio value paths.

    The simulation uses geometric compounding:
        log_return = (mu - 0.5*sigma^2)dt + sigma*sqrt(dt)*Z
    where Z is correlated through a Cholesky factor.
    """
    config.validate()
    rng = np.random.default_rng(config.seed)

    n_assets = len(config.weights)
    dt = 1.0 / config.trading_days
    chol = np.linalg.cholesky(config.correlation_matrix)

    independent_shocks = rng.standard_normal(
        size=(config.simulations, config.trading_days, n_assets)
    )
    correlated_shocks = independent_shocks @ chol.T

    drift = (config.annual_returns - 0.5 * config.annual_volatilities**2) * dt
    diffusion = config.annual_volatilities * np.sqrt(dt) * correlated_shocks
    asset_log_returns = drift + diffusion

    # Convert asset log returns to simple returns before applying portfolio weights.
    asset_simple_returns = np.expm1(asset_log_returns)
    portfolio_simple_returns = asset_simple_returns @ config.weights

    growth_factors = 1.0 + portfolio_simple_returns
    portfolio_paths = config.initial_value * np.cumprod(growth_factors, axis=1)
    terminal_values = portfolio_paths[:, -1]
    losses = config.initial_value - terminal_values

    return {
        "paths": portfolio_paths,
        "terminal_values": terminal_values,
        "losses": losses,
        "asset_log_returns": asset_log_returns,
        "portfolio_simple_returns": portfolio_simple_returns,
        "cholesky": chol,
    }


def var_cvar(losses: np.ndarray, confidence: float) -> tuple[float, float]:
    """Calculate Value-at-Risk and Conditional Value-at-Risk from losses."""
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1.")
    losses = np.asarray(losses, dtype=float)
    var = float(np.quantile(losses, confidence))
    tail_losses = losses[losses >= var]
    cvar = float(tail_losses.mean())
    return var, cvar


def risk_summary(
    simulation: dict[str, np.ndarray],
    initial_value: float,
    confidences: tuple[float, ...] = (0.95, 0.99),
) -> pd.DataFrame:
    """Create a concise risk summary table."""
    terminal_values = simulation["terminal_values"]
    losses = simulation["losses"]
    rows = [
        ("Initial Value", initial_value),
        ("Mean Terminal Value", terminal_values.mean()),
        ("Median Terminal Value", np.median(terminal_values)),
        ("Terminal Value Std. Dev.", terminal_values.std(ddof=1)),
        ("Probability of Loss", np.mean(losses > 0)),
    ]
    for confidence in confidences:
        var, cvar = var_cvar(losses, confidence)
        rows.extend(
            [
                (f"{confidence:.0%} VaR", var),
                (f"{confidence:.0%} CVaR", cvar),
            ]
        )
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def empirical_asset_correlation(asset_log_returns: np.ndarray) -> np.ndarray:
    """Estimate correlation from all simulated asset-return observations."""
    flattened = asset_log_returns.reshape(-1, asset_log_returns.shape[-1])
    return np.corrcoef(flattened, rowvar=False)


def run_scenario_table(
    base_config: PortfolioConfig,
    scenarios: dict[str, dict[str, np.ndarray | int]],
    confidence: float = 0.95,
) -> pd.DataFrame:
    """Run named correlation/volatility scenarios and compare risk."""
    rows = []
    for name, updates in scenarios.items():
        config = PortfolioConfig(
            initial_value=base_config.initial_value,
            weights=base_config.weights.copy(),
            annual_returns=base_config.annual_returns.copy(),
            annual_volatilities=np.asarray(
                updates.get("annual_volatilities", base_config.annual_volatilities)
            ),
            correlation_matrix=np.asarray(
                updates.get("correlation_matrix", base_config.correlation_matrix)
            ),
            trading_days=base_config.trading_days,
            simulations=int(updates.get("simulations", base_config.simulations)),
            seed=int(updates.get("seed", base_config.seed)),
        )
        result = simulate_portfolio_paths(config)
        var, cvar = var_cvar(result["losses"], confidence)
        rows.append(
            {
                "Scenario": name,
                "Mean Terminal Value": result["terminal_values"].mean(),
                "Probability of Loss": np.mean(result["losses"] > 0),
                f"{confidence:.0%} VaR": var,
                f"{confidence:.0%} CVaR": cvar,
            }
        )
    return pd.DataFrame(rows).set_index("Scenario")


def convergence_table(
    base_config: PortfolioConfig,
    simulation_counts: tuple[int, ...] = (500, 1_000, 2_500, 5_000, 10_000),
    confidence: float = 0.95,
) -> pd.DataFrame:
    """Show how VaR/CVaR estimates change as simulation count increases."""
    rows = []
    for count in simulation_counts:
        config = PortfolioConfig(
            initial_value=base_config.initial_value,
            weights=base_config.weights.copy(),
            annual_returns=base_config.annual_returns.copy(),
            annual_volatilities=base_config.annual_volatilities.copy(),
            correlation_matrix=base_config.correlation_matrix.copy(),
            trading_days=base_config.trading_days,
            simulations=count,
            seed=base_config.seed,
        )
        result = simulate_portfolio_paths(config)
        var, cvar = var_cvar(result["losses"], confidence)
        rows.append({"Simulations": count, "VaR": var, "CVaR": cvar})
    return pd.DataFrame(rows).set_index("Simulations")
