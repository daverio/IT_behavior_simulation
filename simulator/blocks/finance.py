from __future__ import annotations

from simulator.models import FinanceState


class FinanceBlock:
    def __init__(self, state: FinanceState | None = None) -> None:
        self.state = state or FinanceState()
        self.last_management_summary: dict[str, float] = {}

    def record_management_period_effects(self, cost_summary: dict[str, float]) -> None:
        self.last_management_summary = dict(cost_summary)

    def advance_financial_state(self) -> None:
        return None

    def get_state(self) -> FinanceState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        outstanding_debt = sum(loan.principal_outstanding for loan in self.state.loans)
        receivables = sum(
            position.amount_outstanding
            for position in self.state.counterparty_positions
            if position.position_type.value == "receivable"
        )
        payables = sum(
            position.amount_outstanding
            for position in self.state.counterparty_positions
            if position.position_type.value == "payable"
        )
        assets = sum(asset.book_value for asset in self.state.assets)
        return {
            "cash": self.state.cash,
            "outstanding_debt": outstanding_debt,
            "receivables": receivables,
            "payables": payables,
            "assets_book_value": assets,
        }
