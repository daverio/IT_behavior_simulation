from __future__ import annotations

from simulator.models import EnterpriseContract, SubscriptionPlan, UserSubscriptionState


class UserSubscription:
    def __init__(self, state: UserSubscriptionState | None = None) -> None:
        self.state = state or UserSubscriptionState()

    def register_standard_plan(self, plan: SubscriptionPlan) -> None:
        self.state.plans.append(plan)
        self.state.active_standard_buckets.setdefault(plan.subscription_name, {})
        self.state.inactive_standard_buckets.setdefault(plan.subscription_name, {})
        for option in plan.pricing_options:
            self.state.active_standard_buckets[plan.subscription_name].setdefault(
                option.duration_months, [0] * option.duration_months
            )
            self.state.inactive_standard_buckets[plan.subscription_name].setdefault(
                option.duration_months, [0] * option.duration_months
            )

    def add_enterprise_contract(self, contract: EnterpriseContract) -> None:
        self.state.enterprise_contracts[contract.contract_id] = contract

    def advance_standard_subscriptions(self) -> dict[str, dict[int, dict[str, int]]]:
        expiries: dict[str, dict[int, dict[str, int]]] = {}
        for subscription_name, duration_map in self.state.active_standard_buckets.items():
            expiries.setdefault(subscription_name, {})
            for duration_months, buckets in duration_map.items():
                active_expiring = buckets[0] if buckets else 0
                inactive_expiring = self.state.inactive_standard_buckets[subscription_name][duration_months][0]
                expiries[subscription_name][duration_months] = {
                    "active": active_expiring,
                    "inactive": inactive_expiring,
                }
                self.state.active_standard_buckets[subscription_name][duration_months] = self._age_bucket_vector(buckets)
                self.state.inactive_standard_buckets[subscription_name][duration_months] = self._age_bucket_vector(
                    self.state.inactive_standard_buckets[subscription_name][duration_months]
                )
        return expiries

    def advance_enterprise_contracts(self, current_month: int) -> None:
        return None

    def apply_market_response(self) -> None:
        return None

    def get_state(self) -> UserSubscriptionState:
        return self.state

    def get_kpis(self) -> dict[str, float]:
        total_active = 0
        total_inactive = 0
        total_enterprise_contracts = len(self.state.enterprise_contracts)
        total_enterprise_users = 0

        for duration_map in self.state.active_standard_buckets.values():
            for buckets in duration_map.values():
                total_active += sum(buckets)

        for duration_map in self.state.inactive_standard_buckets.values():
            for buckets in duration_map.values():
                total_inactive += sum(buckets)

        for contract in self.state.enterprise_contracts.values():
            total_enterprise_users += contract.number_of_users

        return {
            "active_standard_subscriptions": float(total_active),
            "inactive_standard_subscriptions": float(total_inactive),
            "enterprise_contracts": float(total_enterprise_contracts),
            "enterprise_users": float(total_enterprise_users),
        }

    @staticmethod
    def _age_bucket_vector(buckets: list[int]) -> list[int]:
        if not buckets:
            return []
        return buckets[1:] + [0]
