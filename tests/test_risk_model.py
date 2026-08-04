import numpy as np
from src.risk_model import PortfolioConfig, simulate_portfolio_paths, var_cvar


def sample_config() -> PortfolioConfig:
    return PortfolioConfig(
        initial_value=1_000_000,
        weights=np.array([0.4, 0.4, 0.2]),
        annual_returns=np.array([0.08, 0.05, 0.06]),
        annual_volatilities=np.array([0.20, 0.15, 0.25]),
        correlation_matrix=np.array(
            [[1.0, 0.6, 0.3], [0.6, 1.0, 0.5], [0.3, 0.5, 1.0]]
        ),
        simulations=1_000,
        seed=42,
    )


def test_paths_shape_and_reproducibility():
    config = sample_config()
    first = simulate_portfolio_paths(config)
    second = simulate_portfolio_paths(config)
    assert first["paths"].shape == (1_000, 252)
    assert np.allclose(first["terminal_values"], second["terminal_values"])


def test_cvar_is_at_least_var():
    result = simulate_portfolio_paths(sample_config())
    var, cvar = var_cvar(result["losses"], 0.95)
    assert cvar >= var
