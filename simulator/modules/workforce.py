from __future__ import annotations

from simulator.models import ACTIVITY_CATEGORIES, WorkforceState


class Workforce:
    def __init__(self, state: WorkforceState | None = None) -> None:
        self.state = state or WorkforceState()

    def update_worker_state(self) -> None:
        return None

    def compute_effective_labor(self) -> dict[str, float]:
        effective_labor = {activity: 0.0 for activity in ACTIVITY_CATEGORIES}
        for worker in self.state.workers:
            for activity in ACTIVITY_CATEGORIES:
                effective_labor[activity] += (
                    worker.availability
                    * worker.skill_vector.get(activity, 0.0)
                    * worker.allocation_vector.get(activity, 0.0)
                )
        return effective_labor

    def get_state(self) -> WorkforceState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        total_cost = sum(worker.cost for worker in self.state.workers)
        total_availability = sum(worker.availability for worker in self.state.workers)
        return {
            "headcount": float(len(self.state.workers)),
            "total_worker_cost": total_cost,
            "total_worker_availability": total_availability,
        }
