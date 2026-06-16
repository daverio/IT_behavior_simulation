from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


ACTIVITY_CATEGORIES: tuple[str, ...] = (
    "development",
    "manual_qa",
    "support",
    "system_ops",
    "administration",
    "sales",
    "marketing",
    "management",
)


class SupportType(str, Enum):
    UNSPECIFIED = "unspecified"


class PaymentTiming(str, Enum):
    IN_ADVANCE = "in_advance"
    IN_ARREARS = "in_arrears"


class PositionType(str, Enum):
    RECEIVABLE = "receivable"
    PAYABLE = "payable"


class AssetType(str, Enum):
    PPE = "ppe"
    INTANGIBLE = "intangible"


@dataclass(slots=True)
class DemandEnvironmentState:
    potential_new_users: int = 0
    former_users: int = 0
    competitive_pressure: float = 0.0
    brand_recognition: float = 0.0
    budget_pressure: float = 0.0
    market_growth: float = 0.0
    switching_friction: float = 0.0
    former_user_satisfaction: list[float] = field(default_factory=list)


@dataclass(slots=True)
class LaborEnvironmentState:
    hiring_difficulty_by_activity: dict[str, float] = field(
        default_factory=lambda: {activity: 0.0 for activity in ACTIVITY_CATEGORIES}
    )
    wage_pressure_by_activity: dict[str, float] = field(
        default_factory=lambda: {activity: 0.0 for activity in ACTIVITY_CATEGORIES}
    )


@dataclass(slots=True)
class CapitalEnvironmentState:
    debt_access: float = 0.0
    debt_cost: float = 0.0
    equity_access: float = 0.0


@dataclass(slots=True)
class EnvironmentState:
    demand: DemandEnvironmentState = field(default_factory=DemandEnvironmentState)
    labor: LaborEnvironmentState = field(default_factory=LaborEnvironmentState)
    capital: CapitalEnvironmentState = field(default_factory=CapitalEnvironmentState)


@dataclass(slots=True)
class SubscriptionPricingOption:
    duration_months: int
    price_per_user: float


@dataclass(slots=True)
class SubscriptionPlan:
    subscription_name: str
    support_type: SupportType = SupportType.UNSPECIFIED
    pricing_options: list[SubscriptionPricingOption] = field(default_factory=list)


@dataclass(slots=True)
class EnterpriseContract:
    contract_id: str
    start_month: int
    duration_months: int
    number_of_users: int
    support_type: SupportType = SupportType.UNSPECIFIED
    total_price: float = 0.0
    payment_schedule_months: int = 1
    payment_timing: PaymentTiming = PaymentTiming.IN_ADVANCE


@dataclass(slots=True)
class RequirementItem:
    item_id: str
    creation_time: int
    priority: float
    complexity: float
    progress: float = 0.0
    user_impact: float = 0.0
    quality: float = 0.0


@dataclass(slots=True)
class FeatureItem:
    item_id: str
    creation_time: int
    priority: float
    required_effort: float
    complexity: float
    progress: float = 0.0
    user_impact: float = 0.0
    required_verification: float = 0.0
    automated_test_coverage: float = 0.0
    manual_test_coverage: float = 0.0


@dataclass(slots=True)
class BugItem:
    item_id: str
    creation_time: int
    priority: float
    linked_feature_id: str | None
    required_effort: float
    complexity: float
    progress: float = 0.0
    user_impact: float = 0.0
    required_verification: float = 0.0
    automated_test_coverage: float = 0.0
    manual_test_coverage: float = 0.0


@dataclass(slots=True)
class MaintenanceItem:
    item_id: str
    creation_time: int
    priority: float
    linked_feature_id: str | None
    required_effort: float
    complexity: float
    progress: float = 0.0
    user_impact: float = 0.0
    required_verification: float = 0.0
    automated_test_coverage: float = 0.0
    manual_test_coverage: float = 0.0


@dataclass(slots=True)
class AutomatedTestingItem:
    item_id: str
    creation_time: int
    priority: float
    target_item_id: str | None
    required_effort: float
    complexity: float
    progress: float = 0.0
    user_impact: float = 0.0
    required_verification: float = 0.0
    automated_test_coverage: float = 0.0
    manual_test_coverage: float = 0.0


@dataclass(slots=True)
class ProductState:
    requirements_backlog: list[RequirementItem] = field(default_factory=list)
    requirements_wip: list[RequirementItem] = field(default_factory=list)
    requirements_done: list[RequirementItem] = field(default_factory=list)
    features_backlog: list[FeatureItem] = field(default_factory=list)
    features_wip: list[FeatureItem] = field(default_factory=list)
    features_done: list[FeatureItem] = field(default_factory=list)
    bugs_backlog: list[BugItem] = field(default_factory=list)
    bugs_wip: list[BugItem] = field(default_factory=list)
    bugs_done: list[BugItem] = field(default_factory=list)
    maintenance_backlog: list[MaintenanceItem] = field(default_factory=list)
    maintenance_wip: list[MaintenanceItem] = field(default_factory=list)
    maintenance_done: list[MaintenanceItem] = field(default_factory=list)
    testing_backlog: list[AutomatedTestingItem] = field(default_factory=list)
    testing_wip: list[AutomatedTestingItem] = field(default_factory=list)
    testing_done: list[AutomatedTestingItem] = field(default_factory=list)
    architecture_quality: float = 0.0
    testing_quality: float = 0.0
    internal_documentation_quality: float = 0.0
    external_documentation_quality: float = 0.0


@dataclass(slots=True)
class UserSubscriptionState:
    plans: list[SubscriptionPlan] = field(default_factory=list)
    active_standard_buckets: dict[str, dict[int, list[int]]] = field(default_factory=dict)
    inactive_standard_buckets: dict[str, dict[int, list[int]]] = field(default_factory=dict)
    enterprise_contracts: dict[str, EnterpriseContract] = field(default_factory=dict)
    active_satisfaction: list[float] = field(default_factory=list)
    inactive_satisfaction: list[float] = field(default_factory=list)


@dataclass(slots=True)
class Worker:
    worker_id: str
    hire_time: int
    onboarding: float
    motivation: float
    experience: float
    cost: float
    availability: float
    skill_vector: dict[str, float] = field(
        default_factory=lambda: {activity: 0.0 for activity in ACTIVITY_CATEGORIES}
    )
    allocation_vector: dict[str, float] = field(
        default_factory=lambda: {activity: 0.0 for activity in ACTIVITY_CATEGORIES}
    )


@dataclass(slots=True)
class WorkforceState:
    workers: list[Worker] = field(default_factory=list)


@dataclass(slots=True)
class CostAllocationState:
    marketing: float = 0.0
    infrastructure: float = 0.0
    tools: float = 0.0
    contractors: float = 0.0
    hiring: float = 0.0
    training: float = 0.0
    other: float = 0.0


@dataclass(slots=True)
class Loan:
    loan_id: str
    issue_time: int
    principal_initial: float
    principal_outstanding: float
    interest_rate: float
    maturity: int
    repayment_type: str


@dataclass(slots=True)
class CounterpartyPosition:
    position_id: str
    position_type: PositionType
    recognition_time: int
    amount_initial: float
    amount_outstanding: float
    counterparty_type: str
    payment_due_time: int
    status: str


@dataclass(slots=True)
class Asset:
    asset_id: str
    asset_type: AssetType
    recognition_time: int
    cost_basis: float
    book_value: float
    useful_life: int
    value_consumption_method: str
    status: str


@dataclass(slots=True)
class FinanceState:
    cash: float = 0.0
    loans: list[Loan] = field(default_factory=list)
    counterparty_positions: list[CounterpartyPosition] = field(default_factory=list)
    assets: list[Asset] = field(default_factory=list)
