from __future__ import annotations

import copy
import random
from typing import Any

from simulator.modules import (
    CostAllocation,
    Environment,
    Finance,
    Product,
    UserSubscription,
    Workforce,
)


class Simulation:
    def __init__(
        self,
        environment: Environment | None = None,
        users: UserSubscription | None = None,
        product: Product | None = None,
        workforce: Workforce | None = None,
        costs: CostAllocation | None = None,
        finance: Finance | None = None,
        *,
        seed: int = 0,
    ) -> None:
        self.environment = environment or Environment()
        self.users = users or UserSubscription()
        self.product = product or Product()
        self.workforce = workforce or Workforce()
        self.costs = costs or CostAllocation()
        self.finance = finance or Finance()

        self.seed = seed
        self.rng = random.Random(seed)
        self.development_step = 0
        self.management_period_index = 0
        self.financing_period_index = 0
        self.management_period_length = 2
        self.financing_period_length = 6

    def step_development(self) -> dict[str, float]:
        self.environment.advance_exogenous(self.development_step)
        self.workforce.update_worker_state()
        self.product.create_automatic_work_items(self.rng)
        effective_labor = self.workforce.compute_effective_labor()
        self.product.execute_work(effective_labor)
        self.product.update_product_state()

        self.development_step += 1

        if self._at_management_boundary():
            self.run_management_update()

        if self._at_financing_boundary():
            self.run_financing_update()

        return self.get_kpis()

    def run_management_update(self) -> dict[str, float]:
        self.management_period_index += 1
        self.users.advance_standard_subscriptions()
        self.users.advance_enterprise_contracts(self.current_month)
        self.users.apply_market_response()
        cost_summary = self.costs.compute_operating_costs(self.workforce.get_state())
        self.finance.record_management_period_effects(cost_summary)
        return self.get_kpis()

    def run_financing_update(self) -> dict[str, float]:
        self.financing_period_index += 1
        self.finance.advance_financial_state()
        return self.get_kpis()

    @property
    def current_month(self) -> int:
        return self.management_period_index

    def get_kpis(self) -> dict[str, float]:
        kpis: dict[str, float] = {
            "development_step": float(self.development_step),
            "management_period_index": float(self.management_period_index),
            "financing_period_index": float(self.financing_period_index),
        }
        kpis.update(self.environment.get_kpis())
        kpis.update(self.users.get_kpis())
        kpis.update(self.product.get_kpis())
        kpis.update(self.workforce.get_kpis())
        kpis.update(self.costs.get_kpis())
        kpis.update(self.finance.get_kpis())
        return kpis

    def save_state(self) -> dict[str, Any]:
        return copy.deepcopy(
            {
                "seed": self.seed,
                "development_step": self.development_step,
                "management_period_index": self.management_period_index,
                "financing_period_index": self.financing_period_index,
                "rng_state": self.rng.getstate(),
                "environment": self.environment.get_state(),
                "users": self.users.get_state(),
                "product": self.product.get_state(),
                "workforce": self.workforce.get_state(),
                "costs": self.costs.get_state(),
                "finance": self.finance.get_state(),
            }
        )

    def load_state(self, snapshot: dict[str, Any]) -> None:
        self.seed = snapshot["seed"]
        self.development_step = snapshot["development_step"]
        self.management_period_index = snapshot["management_period_index"]
        self.financing_period_index = snapshot["financing_period_index"]
        self.environment.state = copy.deepcopy(snapshot["environment"])
        self.users.state = copy.deepcopy(snapshot["users"])
        self.product.state = copy.deepcopy(snapshot["product"])
        self.workforce.state = copy.deepcopy(snapshot["workforce"])
        self.costs.state = copy.deepcopy(snapshot["costs"])
        self.finance.state = copy.deepcopy(snapshot["finance"])
        self.rng = random.Random()
        self.rng.setstate(snapshot["rng_state"])

    def _at_management_boundary(self) -> bool:
        return self.development_step % self.management_period_length == 0

    def _at_financing_boundary(self) -> bool:
        return self.development_step % self.financing_period_length == 0
