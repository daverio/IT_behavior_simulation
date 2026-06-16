from __future__ import annotations

from simulator.models import CostAllocationState, WorkforceState


class CostAllocationBlock:
    def __init__(self, state: CostAllocationState | None = None) -> None:
        self.state = state or CostAllocationState()

    def compute_operating_costs(self, workforce_state: WorkforceState) -> dict[str, float]:
        labor_cost = sum(worker.cost for worker in workforce_state.workers)
        non_labor_cost = (
            self.state.marketing
            + self.state.infrastructure
            + self.state.tools
            + self.state.contractors
            + self.state.hiring
            + self.state.training
            + self.state.other
        )
        return {
            "labor_cost": labor_cost,
            "marketing_cost": self.state.marketing,
            "infrastructure_cost": self.state.infrastructure,
            "tools_cost": self.state.tools,
            "contractor_cost": self.state.contractors,
            "hiring_cost": self.state.hiring,
            "training_cost": self.state.training,
            "other_cost": self.state.other,
            "total_non_labor_cost": non_labor_cost,
        }

    def get_state(self) -> CostAllocationState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        return {
            "marketing_cost": self.state.marketing,
            "infrastructure_cost": self.state.infrastructure,
            "tools_cost": self.state.tools,
            "contractor_cost": self.state.contractors,
            "hiring_cost": self.state.hiring,
            "training_cost": self.state.training,
            "other_cost": self.state.other,
        }
