# Software Project Lifecycle Simulator


This model is loosely inspired by the St. Gallen Management Model in the sense that it treats the company as an interacting system embedded in an external environment. However, it does not attempt to reproduce the full St. Gallen framework. Instead, it uses only a minimal operational subset of that perspective, keeping the parts that are useful for simulation while avoiding broader or more qualitative categories that are not needed for the current model.

In particular, the first version of the simulator deliberately omits or leaves implicit the following parts of the broader St. Gallen perspective:

- explicit modeling of values, norms, and broader cultural interpretation processes
- detailed stakeholder classes beyond those directly needed for the simulation, such as public institutions, NGOs, and competitors as standalone actors
- a full distinction between normative, strategic, and operative management as separate modeled layers
- rich organizational-culture variables, trust dynamics, legitimacy dynamics, and other communicative or reflexive management concepts
- broad societal, ecological, and institutional dimensions that are important for a full systems picture but are too complex for the first simulation step
- explicit optimization-versus-renewal development modes as separate modeled subsystems

These elements are not considered irrelevant. They are omitted only because the current objective is to build a first executable model with a manageable level of complexity. They may be added later if the scope of the simulator is expanded.


## Model Structure

The simulator is organized as an interacting enterprise system. The external environment shapes demand, labor availability, and financing conditions. The company responds to these conditions through its commercial user base, its product-development system, its workforce, its non-labor spending decisions, and its financial structure.

At a high level, the model follows the following causal organization:

- the **Environment Block** provides the main exogenous pressures acting on the company
- the **User and Subscription Block** represents the currently captured customer base and its commercial structure
- the **Product Block** represents the evolving software system and the work needed to improve, fix, maintain, and validate it
- the **Workforce Block** represents the human resources available to execute the work and operate the company
- the **Cost Allocation Block** represents the main non-labor expenditures used to support growth and operations
- the **Finance Block** represents liquidity, assets, liabilities, working-capital positions, and financial reporting quantities

These blocks are not independent. Environment influences acquisition, hiring, and financing conditions. Product quality and delivery affect user behavior. Workforce capabilities determine execution capacity across product, support, and commercial activities. Cost allocation and financing decisions constrain what the organization can sustain over time. Financial outcomes summarize the economic consequences of the whole system.

The full model is therefore organized into six blocks:

1. **Environment Block**
    - Demand environment
    - Labor environment
    - Capital environment

2. **User and Subscription Block**
    - Subscription plans and contract structures
    - Active and inactive subscribed users
    - Renewal, switching, and expiry structure

3. **Product Block**
    - Feature development
    - Bug creation and resolution
    - Maintenance
    - Architecture, testing, and documentation quality

4. **Workforce Block**
    - Worker population
    - Skills, allocation, onboarding, and motivation
    - Effective labor contribution across organizational activities

5. **Cost Allocation Block**
    - Marketing and acquisition spending
    - Infrastructure, tools, contractors, hiring, and training
    - Other non-labor operating expenditure

6. **Finance Block**
    - Cash and funding
    - Counterparty positions and long-lived assets
    - Financial flows and reporting outputs



### Environment Variables

The environment block contains the main exogenous conditions that influence the company but are not directly controlled by it. In the current minimal version, it is decomposed into three sub-environments:

- demand environment
- labor environment
- capital environment

#### Demand environment

The demand environment describes the external customer space that is outside the firm's currently subscribed user base.

##### State variables

- $P^{new}$: pool of potential users who never tried the product
- $P^{former}$: former users who tried the product and are currently not subscribers, and have stoped their subscription
- $E^{demand}_{comp}$: competitive pressure in the external market
- $E^{demand}_{brand}$: brand recognition of the company in the external market
- $E^{demand}_{budget}$: customer budget pressure / willingness to pay in the external market
- $E^{demand}_{growth}$: growth or contraction pressure of the addressable market
- $E^{demand}_{switch}$: switching friction affecting adoption and return to the product
- $S^{former}$: satisfaction distribution associated with former users

The variable $S^{former}$ is not a scalar variable. It is a normalized distribution over ordered satisfaction states and satisfies:

- $S^{former,(i)} \ge 0$ for every satisfaction state $i$
- $\sum_i S^{former,(i)} = 1$

The variables $E^{demand}_{comp}$ and $E^{demand}_{brand}$ capture two additional external demand conditions. Competitive pressure represents the intensity of outside alternatives competing for the same customer base. Brand recognition represents the degree to which the product or company is known in the external market.

The variable $E^{demand}_{budget}$ captures how constrained customers are in their spending and therefore how difficult it is to convert or retain paid demand at current price levels. The variable $E^{demand}_{growth}$ captures whether the external addressable market is expanding, stable, or contracting over time. The variable $E^{demand}_{switch}$ captures how difficult it is for potential or former users to move toward the product instead of remaining with alternatives or with no solution.

##### Observation variables / KPIs

- first-time subscriptions during the period
- returning subscriptions during the period
- total unsubscribed market size
- total former-customer pool

#### Labor environment

The labor environment captures how difficult and expensive it is to hire and retain workers from the external labor market.

##### State variables

- $E^{labor}_{hire,a}$: hiring difficulty for activity category $a$ in the external labor market
- $E^{labor}_{wage,a}$: wage pressure for activity category $a$ in the external labor market

The labor-environment variables are indexed by the same activity categories used by the workforce skill vector and allocation vector. This keeps external labor conditions aligned with the internal representation of workforce capabilities.

At minimum, the activity index $a$ spans the following categories:

- development
- manual QA
- support
- system opp
- administration
- sales
- marketing
- management lower/upper

##### Observation variables / KPIs

- average hiring pressure indicator by activity category
- average wage pressure indicator by activity category

#### Capital environment

The capital environment captures the main external conditions under which the company can obtain debt or equity financing.

##### State variables

- $E^{capital}_{debt,access}$: availability of debt financing from lenders
- $E^{capital}_{debt,cost}$: external cost of debt financing, for example through interest-rate pressure
- $E^{capital}_{equity,access}$: availability of equity financing from investors

The variable $E^{capital}_{debt,access}$ captures how willing lenders are to provide debt to the company. The variable $E^{capital}_{debt,cost}$ captures how expensive debt financing is once it is available. The variable $E^{capital}_{equity,access}$ captures how willing investors are to provide external equity capital.

##### Observation variables / KPIs

- average debt financing pressure indicator
- average equity financing pressure indicator


### User and Subscription Variables

#### Subscription plan definition

The user and subscription block contains two different commercial representations:

- standard subscriptions represented by bucketed subscription states
- enterprise subscriptions represented by explicit contract records

The standard subscription offer is represented as an array of subscription structures.

Each subscription structure contains at least the following properties:

- `subscription name`: name of the subscription tier
- `support type`: support model associated with the subscription tier, represented as an enum
- `pricing options`: list of pairs `(duration, price per user)`

The `support type` field is intended to be an enum rather than a free-text label. In the current version of the model, the concrete enum values may be defined later, but the field is already understood as a discrete support-category selector.

The current intended subscription names include, for example:

- `single`
- `plus`

Within one subscription structure, the `pricing options` list may contain, for example:

- `(1, price per user for one month)`
- `(3, price per user for three months)`
- `(12, price per user for twelve months)`

This means that:

- `sub` identifies one subscription structure in the subscription array
- `period` identifies one duration available inside that subscription structure
- the associated price per user is obtained from the corresponding `(duration, price per user)` pair

The subscribed-user state therefore refers to a subscription name and one of its available durations, while the underlying subscription-plan structure remains a clean array of structs.

In the current version of the model, all standard subscriptions are fixed-term subscriptions. A subscription remains on its current plan until expiry, at which point it may renew, switch plan, or churn according to the commercial transition rules.

#### Enterprise contract definition

Enterprise subscriptions are not represented by the same bucket structure as standard subscriptions. They are represented by a map of enterprise contract structures keyed by contract `id`.

Each enterprise contract structure contains at least the following properties:

- `id`: unique identifier of the contract and key of the map entry
- `start month`: month at which the contract starts
- `duration in months`: contract duration
- `number of users`: number of covered users under the contract
- `support type`: support model associated with the contract, represented as the same enum used for standard subscriptions
- `total price`: total commercial value of the contract
- `payment schedule`: payment period indicating how often payments are due
- `payment timing`: whether payment is due in advance or at the end of the billing period

This representation is used because enterprise contracts may have heterogeneous duration, covered-user counts, and payment timing. When a payment becomes due and remains unpaid, the corresponding obligation may later generate a receivable position in the financial block.

#### State variables

- $U^{active}_{sub,period,i}$: active standard subscriptions of tier `sub`, contract duration `period`, and bucket index `i`
- $U^{inactive}_{sub,period,i}$: inactive standard subscriptions of tier `sub`, contract duration `period`, and bucket index `i`
- $C^{ent}$: map of enterprise contracts keyed by contract `id`
- $S^{active}$: satisfaction distribution associated with active users
- $S^{inactive}$: satisfaction distribution associated with inactive subscribed users

The variables $S^{active}$ and $S^{inactive}$ are not scalar variables. They are normalized distributions over ordered satisfaction states. For each user population $x \in \{active, inactive\}$, the associated distribution satisfies:

- $S^{x,(i)} \ge 0$ for every satisfaction state $i$
- $\sum_i S^{x,(i)} = 1$

The standard subscribed state is no longer represented by a single scalar population. Instead, it is represented by bucketed subscription variables indexed by subscription tier, subscription duration, and remaining-time bucket.

For $U^{active}_{sub,period,i}$ and $U^{inactive}_{sub,period,i}$:

- `sub` identifies the standard subscription tier, for example `single` or `plus`
- `period` identifies the subscription duration in months, for example `1`, `3`, or `12`
- `i` identifies the remaining-time bucket inside the subscription cycle

The bucket index is interpreted as:

- $i = 0$: subscriptions that expire at the end of the current month
- $i = 1$: subscriptions that expire at the end of the next month
- more generally, larger $i$ means a longer remaining time before expiry

At each monthly step, the bucket system advances by one month. Expiring subscriptions in bucket $i = 0$ are then renewed, switched to another plan, or moved to $P^{former}$ according to the commercial transition rules.

This notation is chosen so that the subscription state remains compatible with implementation as a regular indexed array. For a given duration `period`, only the bucket indices compatible with that duration are meaningful.

Enterprise contracts are represented separately in $C^{ent}$ because they may have heterogeneous user counts, prices, contract durations, and payment schedules that cannot be represented cleanly by the standard bucket structure alone.

The user and subscription block owns the subscribed user base and its organization by plan and remaining contract duration. Financial quantities induced by the subscription base, such as revenue, receivables, support expense, or infrastructure expense, are not primitive user variables. They are derived later through the financial and cost-allocation layers from the user state and the applicable pricing or operating rules.

#### Observation variables / KPIs

The following quantities are not primitive state variables. They are derived from the user and subscription state and from the transitions occurring during a period, and are mainly used for monitoring, diagnostics, and historical analysis.

- deactivations during the period
- reactivations during the period
- subscriptions expiring during the period
- renewals during the period
- plan switches during the period
- churns at expiry during the period
- total active subscriptions
- total inactive subscriptions
- total subscriptions by tier
- total subscriptions by duration
- total enterprise contracts
- total users covered by enterprise contracts


### Product Variables

- $R^{backlog}$: list of requirement items waiting to be started
- $R^{wip}$: list of requirement items currently being worked on
- $R^{done}$: list of completed requirement items available to feed feature work
- $F^{backlog}$: list of feature items waiting to be started
- $F^{wip}$: list of feature items currently being worked on
- $F^{done}$: list of delivered feature items available in the product 
- $B^{backlog}$: list of discovered bug items waiting to be addressed
- $B^{wip}$: list of bug items currently being worked on
- $B^{done}$: list of resolved bug items
- $M^{backlog}$: list of maintenance items waiting to be started
- $M^{wip}$: list of maintenance items currently being worked on
- $M^{done}$: list of completed maintenance items
- $T^{backlog}$: list of automated testing items waiting to be started
- $T^{wip}$: list of automated testing items currently being worked on
- $T^{done}$: list of completed automated testing items
- $Q^{arch}$: architecture quality / degree to which the software architecture remains under control
- $Q^{test}$: quality / coverage of the automated testing infrastructure
- $D^{int}$: internal / developer documentation quality
- $D^{ext}$: external / user documentation quality

#### Requirement items

Requirement items do not share exactly the same structure as the other product work items. Each requirement item contains the following properties:

- `id`: unique identifier of the requirement item
- `creation time`: time at which the requirement enters its backlog
- `priority`: priority level used later to decide ordering and allocation of work
- `complexity`: structural or conceptual difficulty of the requirement
- `progress`: amount of work already completed on the requirement
- `user impact`: expected effect of the requirement on user experience, product attractiveness, and satisfaction
- `quality`: degree to which the requirement has been clarified, validated, and made actionable for later implementation work

#### Feature items

Each feature item contains the following properties:

- `id`: unique identifier of the feature item
- `creation time`: time at which the feature enters its backlog
- `priority`: priority level used later to decide ordering and allocation of work
- `required effort`: total amount of work needed to complete the feature
- `complexity`: structural or conceptual difficulty of the feature
- `progress`: amount of work already completed on the feature
- `user impact`: expected effect of the feature on user experience, product attractiveness, and satisfaction
- `required verification`: expected amount of verification needed before the feature can be considered safely delivered
- `automated test coverage`: amount of verification of the feature covered by automated testing
- `manual test coverage`: amount of verification of the feature covered by manual testing

#### Bug items

Each bug item contains the following properties:

- `id`: unique identifier of the bug item
- `creation time`: time at which the bug enters its backlog
- `priority`: priority level used later to decide ordering and allocation of work
- `linked feature id`: identifier of the feature to which the bug is attached
- `required effort`: total amount of work needed to complete the bug fix
- `complexity`: structural or conceptual difficulty of the bug fix
- `progress`: amount of work already completed on the bug fix
- `user impact`: expected effect of the bug on user experience and satisfaction
- `required verification`: expected amount of verification needed before the fix can be considered safely delivered
- `automated test coverage`: amount of verification of the bug fix covered by automated testing
- `manual test coverage`: amount of verification of the bug fix covered by manual testing

#### Maintenance items

Each maintenance item contains the following properties:

- `id`: unique identifier of the maintenance item
- `creation time`: time at which the maintenance item enters its backlog
- `priority`: priority level used later to decide ordering and allocation of work
- `linked feature id`: identifier of the feature or product area to which the maintenance item is attached
- `required effort`: total amount of work needed to complete the maintenance item
- `complexity`: structural or conceptual difficulty of the maintenance item
- `progress`: amount of work already completed on the maintenance item
- `user impact`: expected effect of the maintenance item on user experience, product attractiveness, and satisfaction
- `required verification`: expected amount of verification needed before the maintenance item can be considered safely delivered
- `automated test coverage`: amount of verification of the maintenance item covered by automated testing
- `manual test coverage`: amount of verification of the maintenance item covered by manual testing

#### Automated testing items

Each automated testing item contains the following properties:

- `id`: unique identifier of the automated testing item
- `creation time`: time at which the testing item enters its backlog
- `priority`: priority level used later to decide ordering and allocation of work
- `target item id`: identifier of the feature, bug, or maintenance item whose verification gap motivates the test work
- `required effort`: total amount of work needed to complete the automated testing item
- `complexity`: structural or conceptual difficulty of the automated testing item
- `progress`: amount of work already completed on the automated testing item
- `user impact`: expected indirect effect of the testing item on user experience through improved delivery safety and quality
- `required verification`: expected amount of verification needed before the testing item can be considered complete
- `automated test coverage`: amount of verification delivered by the automated testing item itself
- `manual test coverage`: amount of verification support still provided manually on the same target

Manual QA demand is derived from the remaining verification gap of the relevant work items, i.e. from the difference between required verification and the testing coverage already provided by automated and manual testing.

#### Work-item creation

The product block must also account for how new work items enter the system. Work-item creation is not uniform across all item types.

- **Requirement items** are primarily decision-driven. They correspond to product opportunities, requests, or identified needs that are intentionally converted into requirement work and inserted into $R^{backlog}$.
- **Feature items** are primarily generated automatically from completed requirement work. They correspond to implementation work derived from clarified requirements and are inserted into $F^{backlog}$ once the relevant requirement work has produced something concrete enough to build.
- **Bug items** are primarily generated automatically through the interaction between the current product state, existing defects, testing activity, and user usage. When discovered, they are inserted into $B^{backlog}$.
- **Maintenance items** are primarily generated automatically from the internal evolution of the product, for example through architecture degradation, dependency upkeep, operational needs, or documentation upkeep. When identified, they are inserted into $M^{backlog}$.
- **Automated testing items** are primarily generated automatically from verification gaps created by new product work, bug fixes, and observed weaknesses in the testing infrastructure. When identified, they are inserted into $T^{backlog}$.

The precise equations or rules governing these creation mechanisms are not yet defined, but the ontology should already distinguish between items that arise automatically from system evolution, items that require explicit intake decisions, and items that are generated automatically from prior work-item completion.


### Workforce Variables

- $W$: list of workers in the organization

The workforce is modeled as a list of individual workers rather than as a pure aggregate headcount. This choice is motivated by the need to represent role flexibility, heterogeneous skills, onboarding, motivation, and organizational structures in which one worker can contribute to several activities.

This modeling choice is closer to the agent-based and hybrid workforce-simulation literature, while aggregate workforce counts can still be recovered later as derived summary variables.

#### Worker structure

Each worker is a structure containing the following properties:

- `id`: unique identifier of the worker
- `hire time`: time at which the worker joins the organization
- `onboarding`: degree to which the worker is fully integrated and productive
- `motivation`: worker motivation / engagement level
- `experience`: accumulated familiarity and practical knowledge in the organization
- `cost`: cost associated with the worker
- `availability`: amount of work time currently available for allocation
- `skill vector`: vector describing the worker's relative ability across the main functional activities of the organization
- `allocation vector`: vector describing how the worker is currently allocated across activities

#### Skill and allocation dimensions

The skill and allocation vectors span the main functional activities of the organization. Their dimensions correspond to the main categories of work already identified in the workforce and product blocks.

At minimum, these include:

- requirement development
- feature development
- bug fixing
- maintenance
- automated test development
- manual QA
- internal documentation
- external documentation
- support
- system opp
- administration
- sales
- marketing
- product management
- strategy and upper management

This structure allows one worker to contribute to multiple domains when appropriate, while still preserving the fact that flexibility is limited and role-dependent.

Aggregate workforce quantities such as headcount or effective capacity by function are treated as derived variables computed from the worker list.

In this model, labor allocation is embedded directly in the workforce representation through the allocation vector carried by each worker. As a consequence, the workforce block describes both the available human resources and the distribution of their effort across organizational activities. Labor contribution to each activity is therefore derived from the worker list, their skills, and their current allocations.


### Cost Allocation Variables

The cost allocation block covers non-labor expenditures and financial decisions that affect workforce size, composition, and sustainability.

- $C^{mkt}$: marketing campaign and paid acquisition expenditure
- $C^{infra}$: infrastructure and cloud expenditure
- $C^{tools}$: tools, software licenses, and devops platform expenditure
- $C^{contract}$: external contractors, agencies, and outsourced services expenditure
- $C^{hire}$: hiring and recruiting expenditure
- $C^{train}$: training and skill-development expenditure
- $C^{other}$: other non-labor operating expenditure

These variables represent financial allocations that are not already carried by the worker allocation mechanism. They complement the workforce block rather than duplicate it.


### Financial Variables

The financial block consolidates the economic consequences of the other blocks. It contains the financial state variables that need their own evolution equations, as well as the main financial flows and reporting quantities needed to construct the financial statements.

#### Financial state variables

- $K$: cash
- $Loans$: list of debt instruments
- $P^{cp}$: list of counterparty positions
- $A$: list of assets

The debt of the company is represented primarily through the list of loans. Aggregate outstanding debt may later be computed as a derived quantity from this list. The same logic applies to counterparty positions and assets: the primitive objects are the lists, while aggregate balances such as total receivables, total payables, total PPE, and total intangible assets may later be derived from them by filtering and aggregation.

#### Loan structure

Each loan is a structure containing the following properties:

- `id`: unique identifier of the loan
- `issue time`: time at which the loan is issued
- `principal initial`: initial borrowed principal
- `principal outstanding`: remaining unpaid principal
- `interest rate`: contractual interest rate
- `maturity`: time to final maturity
- `repayment type`: reimbursement rule of the loan

The repayment type may later include, for example, bullet, annuity, linear amortization, or interest-only structures.

#### Counterparty position structure

Each counterparty position is a structure containing the following properties:

- `id`: unique identifier of the position
- `position type`: type of position (`receivable` or `payable`)
- `recognition time`: time at which the position is recognized
- `amount initial`: initial amount recognized in the position
- `amount outstanding`: remaining unpaid amount
- `counterparty type`: type of customer, supplier, or other counterparty
- `payment due time`: expected payment date or payment horizon
- `status`: state of the position (open, partially paid, paid, overdue, defaulted)

Aggregate accounts receivable and accounts payable are derived later by selecting the relevant subset of positions according to `position type`.

#### Asset structure

Each asset is a structure containing the following properties:

- `id`: unique identifier of the asset
- `asset type`: type of asset (`ppe` or `intangible`)
- `recognition time`: time at which the asset enters the balance sheet
- `cost basis`: initial recognized value of the asset
- `book value`: current book value of the asset
- `useful life`: expected depreciation or amortization horizon
- `value consumption method`: depreciation or amortization rule used for the asset
- `status`: state of the asset (active, impaired, disposed)

Aggregate PPE and intangible balances are derived later by selecting the relevant subset of assets according to `asset type`.

#### Financial flows and reporting quantities

The financial block also contains period flows and reporting quantities that are derived from the state of the system and from the activity of the other blocks. These include:

- recognized revenue
- operating expenses
- debt inflows
- equity inflows
- interest expense
- principal repayment
- depreciation
- amortization
- income statement outputs
- cash flow statement outputs
- balance sheet outputs

These quantities are not necessarily state variables. They are included in the financial block because they are needed to construct the financial statements and to understand the financial evolution of the company.


### Scenario definition

A scenario defines the complete setup of one simulation run. It specifies the internal state of the organization at the start of the simulation, the exogenous environment in which it evolves, and the management policy that governs its decisions during the run.

In this model, a scenario contains three main components:

1. **Internal state**
    - The internal state contains the values and structures of all relevant endogenous model variables at the start of the simulation.
    - This includes, for example, the release state of the product, the initial market populations, the product backlogs, the product quality variables, the workforce, and the financial state.

2. **Exogenous environment**
    - The exogenous environment contains the variables that affect the organization but are not directly controlled by it during the run.
    - This includes, for example, market size, competition pressure, hiring conditions, and infrastructure price evolution.

3. **Management policy**
    - The management policy is the set of decision rules that determines how the organization reacts to the current system state.
    - It governs, at minimum, how labor is allocated across activities, and may later also govern hiring, spending priorities, and other adaptive decisions.

A scenario therefore represents the internal condition of the organization, the world in which it operates, and the managerial logic used to react over time.

#### Management policy

For the current version of the model, management policy is not yet specified in a fully rigorous way and is therefore intentionally left partly aside. The simulator loop should nevertheless distinguish clearly between:

- automatic evolution that follows directly from the current system state and from predefined rules
- decision-driven updates that require a choice to be made at specific decision points

In the longer term, these decision-driven updates may be executed in two different modes:

- **Policy mode**: decisions are produced automatically by a predefined policy
- **Human mode**: decisions are chosen directly by a human user instead of by a policy

A management policy is defined as a set of state-dependent rules that transform the current system state into organizational decisions. In the first version of the model, the main role of the policy would be to determine workforce allocation across the different activities of the company.

At a high level, a future management policy may contain:

- baseline allocation priorities across activities
- state-dependent reallocation rules
- constraints or minimum commitments on selected activities

Typical examples include feature-first, quality-first, balanced, or firefighting policies. For now, these ideas remain placeholders rather than fully modeled decision systems.


### Simulation clocks

The simulator evolves in discrete time, but not all organizational processes are updated at the same cadence. The model therefore distinguishes three main periods:

For regularity, time is represented using a simplified calendar:

- 1 month = 4 weeks
- 1 year = 12 months

This convention is not fully realistic, but it allows the simulation clocks to be defined in a simple and regular manner.

1. **Development period**
    - The development period is the base execution period of the simulator.
    - It is intended to represent the cadence of agile development work and is defined in weeks.
    - In the current version of the model, one development period corresponds to one sprint of 2 weeks.
    - Product work execution, work-item progress, testing progress, and the short-term evolution of product state are updated on this clock.

2. **Management period**
    - The management period is a slower decision period on which management reviews the state of the organization and updates its decisions.
    - Market response, subscription evolution, operating costs, and short-horizon financial consequences are updated on this clock.
    - Workforce allocation policies, hiring decisions, training decisions, and other managerial adjustments are updated on this clock.
    - In the current specification, these updates are identified as decision points, even if the detailed policy rules are not yet fully defined.
    - In the current version of the model, one management period corresponds to 1 month.
    - One management period therefore contains 2 development periods.

3. **Financing period**
    - The financing period is a slower financial decision period used for financing review and major budget adjustments.
    - Financing decisions, funding strategy, and longer-horizon financial adjustments are updated on this clock.
    - In the current specification, these updates are also treated as decision points rather than fully automatic rules.
    - In the current version of the model, one financing period corresponds to 1 quarter.
    - One financing period therefore contains 3 management periods.

These values define the default clock structure of the simulator and may later be generalized if needed.


### Evolution of the system

The simulator is intended to evolve in discrete time. The development period is used as the base simulation step. Management and financing updates occur on slower clocks according to their respective periods.

For the current version of the model, the evolution loop should explicitly separate two categories of actions:

- **Automatic updates**: updates that follow directly from the current state and predefined update rules
- **Decision-driven updates**: updates that require a choice and may later be executed either in policy mode or in human mode

At a high level, one development step contains the following phases:

1. **Automatic calendar and exogenous update**
    - Time advances by one development step.
    - Exogenous environment variables may evolve automatically if the scenario specifies a predefined path or shock schedule.

2. **Automatic workforce state update**
    - Worker-level states such as onboarding, motivation, experience, and availability are updated.
    - The skill vector and allocation vector determine the effective labor contribution of each worker to each activity.

3. **Work-item creation and intake**
    - New bug, maintenance, and automated testing items may be generated automatically from the current state of the product and its usage.
    - New requirement items are not treated as purely automatic and normally require an explicit decision to be inserted into the backlog.
    - New feature items are generated automatically from completed requirement items once those requirements are sufficiently clarified and actionable.
    - In policy mode, requirement-intake decisions may later be taken by predefined rules. In human mode, they may be taken directly by the user.

4. **Automatic work execution**
    - Effective labor is distributed across the active work streams.
    - Work items in requirement, feature, bug, maintenance, and automated testing queues progress according to the allocated effort and the current state of the system.

5. **Automatic product state update**
    - Work items may move from backlog to work in progress, and from work in progress to done.
    - Completed requirement items may generate corresponding feature items automatically.
    - Architecture quality, testing quality, and documentation quality evolve as a consequence of the work completed during the step.
    - Manual QA demand is evaluated from the remaining verification gaps on the relevant work items.

6. **Management-period automatic update**
    - When a management period boundary is reached, the product state accumulated over the contained development periods is translated into market response.
    - Product changes affect user satisfaction distributions, retention, reactivation, and acquisition.
    - User and subscription states evolve accordingly.
    - Standard subscription buckets age forward automatically and enterprise contract timing advances automatically.
    - Labor costs are derived from the workforce.
    - Non-labor costs are computed from the cost allocation variables.
    - Financial consequences implied by the current environment, user state, workforce, product, and operating state are recorded through the financial block.

7. **Management-period decision point**
    - When a management period boundary is reached, slower managerial decisions may be updated.
    - These updates are not treated as purely automatic.
    - They may later be produced either by a predefined management policy or directly by a human user.

8. **Financing-period decision point**
    - When a financing period boundary is reached, cash-planning and financing decisions may be updated.
    - These updates are also not treated as purely automatic.
    - They may later be produced either by a predefined financing policy or directly by a human user.

This ordering is conceptual and may later be refined when the explicit simulation equations are introduced. Its purpose is to define a consistent causal logic for how the different blocks interact over time while keeping separate what is automatic from what requires an explicit decision. Those decisions may later be executed either by policy mode or by human mode.



