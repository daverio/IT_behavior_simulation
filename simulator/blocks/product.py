from __future__ import annotations

import random

from simulator.models import ProductState


class ProductBlock:
    def __init__(self, state: ProductState | None = None) -> None:
        self.state = state or ProductState()

    def create_automatic_work_items(self, rng: random.Random) -> None:
        return None

    def execute_work(self, effective_labor: dict[str, float]) -> None:
        return None

    def update_product_state(self) -> None:
        return None

    def get_state(self) -> ProductState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        return {
            "requirements_backlog": float(len(self.state.requirements_backlog)),
            "features_backlog": float(len(self.state.features_backlog)),
            "bugs_backlog": float(len(self.state.bugs_backlog)),
            "maintenance_backlog": float(len(self.state.maintenance_backlog)),
            "testing_backlog": float(len(self.state.testing_backlog)),
            "architecture_quality": self.state.architecture_quality,
            "testing_quality": self.state.testing_quality,
            "internal_documentation_quality": self.state.internal_documentation_quality,
            "external_documentation_quality": self.state.external_documentation_quality,
        }
