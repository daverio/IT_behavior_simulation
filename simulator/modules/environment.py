from __future__ import annotations

from simulator.models import EnvironmentState


class Environment:
    def __init__(self, state: EnvironmentState | None = None) -> None:
        self.state = state or EnvironmentState()

    def advance_exogenous(self, development_step: int) -> None:
        return None

    def get_state(self) -> EnvironmentState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        return {
            "potential_new_users": float(self.state.demand.potential_new_users),
            "former_users": float(self.state.demand.former_users),
            "competitive_pressure": self.state.demand.competitive_pressure,
            "brand_recognition": self.state.demand.brand_recognition,
            "budget_pressure": self.state.demand.budget_pressure,
            "market_growth": self.state.demand.market_growth,
            "switching_friction": self.state.demand.switching_friction,
            "debt_access": self.state.capital.debt_access,
            "debt_cost": self.state.capital.debt_cost,
            "equity_access": self.state.capital.equity_access,
        }
