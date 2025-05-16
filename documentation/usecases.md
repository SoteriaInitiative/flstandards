# Use Case Collection
In order to protect the integrity of the effort the specific use case
application is private. However, two braod use cases are adressed by [flstandards](https://github.com/SoteriaInitiative/flstandards/) in
combination with appropriate [coredata](https://github.com/SoteriaInitiative/coredata) standards. The use cases are described below
and target broad categories of financial crime typologies.

A summary of [covered typologies](https://github.com/SoteriaInitiative/flstandards/blob/main/documentation/usecases.md#typology-coverage) by these two use cases is provided below the use case description.

## Use Case Description
The generic high-level use cases are outlined below and follows the guidelines published by [Figma](https://www.figma.com/resource-library/what-is-a-use-case/).

### Use Case 1: FedML – Increase Detection Resiliency Through Shared Intelligence (Local Lack of Knowledge)

<b>Primary Actor</b>: AML detection system

<b>Secondary Actor</b>: Compliance officer

<b>Goals</b>: Identify suspicious activity at Firm A using knowledge from Firm B

<b>Stakeholders</b>: Regulators, law enforcement, victims, clients

<b>Preconditions</b>:

- Firm B has confirmed certain client behaviors as money laundering through true positive labels.
- This information is abstracted into a machine learning model (e.g., weight matrix) and shared.

<b>Trigger</b>:

- A transaction or KYC event at Firm A resembles activity previously confirmed as suspicious at Firm B.

<b>Scenario</b>:
A client at Firm B has been confirmed to be involved in money laundering. Firm B labels these behaviors and trains a local machine learning model. Firm A has similar clients with related behaviors but no confirmed case history. By incorporating Firm B’s trained model (or a federated aggregation of such models), Firm A’s detection system becomes more sensitive to suspicious activity it would otherwise not have flagged due to its local data limitations.

### Use Case 2: FedML – Detect Money Laundering Activity Deliberately Distributed Between Market Participants (Threshold Evasion, Layer & Splits, Locally Incomplete Transactions)

<b>Primary Actor</b>: AML and sanctions control evasion detection system

<b>Secondary Actor</b>: Compliance officer

<b>Goals</b>: Detect activity that spans multiple firms and is hidden by fragmentation

<b>Stakeholders</b>: Regulators, law enforcement, victims, clients

<b>Preconditions</b>: None

<b>Trigger</b>:

- A transaction or KYC update is detected, but the context is locally incomplete.

<b>Scenario</b>:
A malicious actor deliberately structures transactions across multiple institutions to avoid triggering any one firm’s detection threshold (e.g., avoiding €10,000 transaction limits). At Firm A, the actor presents one identity and address; at Firm B, another. Firm C, a recipient institution, sees legitimate-looking transactions and has no reason to investigate. However, when the information from all three firms is aggregated — e.g., through federated learning or collaborative intelligence mechanisms — it becomes clear that the customer’s activities and counterparties interconnect in a suspicious pattern.

## Typology Coverage

| Typology                                                        | Use Case 1: Shared Intelligence (Local Lack of Knowledge) | Use Case 2: Distributed Activity (Threshold Evasion, Layering) | Coverage Status         | Reasoning |
|------------------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------------|--------------------------|-----------|
| Structuring / Smurfing                                           | ✅                                                          | ✅                                                                | **Fully Covered**        | Detected through privacy preserving cross-firm volume and frequency aggregation |
| Dual/Synthetic Identity Fraud                                    | ✅                                                          | ✅                                                                | **Fully Covered**        | Identity mismatches across firms can be learned using differential privacy|
| Networked Laundering / Client Coordination                       | ✅                                                          | ✅                                                                | **Fully Covered**        | Federated learning identifies behavioral networks |
| Trade-Based Money Laundering (TBML)                              | ✅                                                          | ✅                                                                | **Fully Covered**        | Trade metadata enables pattern learning for price/goods mismatch if covered by [coredata](https://github.com/SoteriaInitiative/coredata)|
| Benign Business Fronts / Co-mingling                             | ✅                                                          | ✅                                                                | **Fully Covered**        | High-volume low-risk appearances exposed by shared detection patterns |
| Use of Payment Alternatives (e.g. gift cards, mobile wallets)    | ✅                                                          | ✅                                                                | **Fully Covered**        | Covered via harmonized payment metadata across networks in [coredata](https://github.com/SoteriaInitiative/coredata) |
| Sanctions Evasion via Indirect Channels                          | ✅                                                          | ✅                                                                | **Fully Covered**        | Privacy preserving customer characteristics sharing reveal indirect relationships |
| Money Mules / Unwitting Intermediaries                           | ✅                                                          | ✅                                                                | **Fully Covered**        | Repeated low-value/frequent transactions across clients become visible |
| Professional Launderers / Nominee Use                            | ✅                                                          | ✅                                                                | **Fully Covered**        | Privacy preserving intelligence sharing reveals usage patterns and role clustering |
| Entity Ownership Obfuscation (Shells, Trusts)                    | ⚠️ Partial                                                 | ✅                                                                | **Partially Covered**    | Use Case 2 covers this if ownership data exists in [coredata](https://github.com/SoteriaInitiative/coredata); Use Case 1 less so |
| Nested Correspondent Banking                                     | ⚠️ Partial                                                 | ⚠️ Partial                                                        | **Partially Covered**    | If nested relationships are disclosed or visible through transaction paths |
| Abuse of DeFi Mechanisms (Mixers, Cross-chain Swaps)             | ✅                                                          | ✅                                                                | **Fully Covered**        | If DeFi providers participate and provide structured metadata |
| Jurisdictional Arbitrage (Use of Non-Cooperative Regimes)        | ✅                                                          | ✅                                                                | **Fully Covered***       | *Conditional on visibility of in/outflows with those jurisdictions* |
| Insider Facilitation / Internal Complicity                       | ❌                                                          | ❌                                                                | **Not Covered**          | Requires internal controls, whistleblowers, or audit — beyond modeling scope |
| Charitable Entity Abuse / Non-Profit Laundering                  | ⚠️ Partial                                                 | ⚠️ Partial                                                        | **Partially Covered**    | May need domain heuristics; only captured if volumes, flows, and ownership structures are anomalous |
| Physical Asset Laundering (Art, Real Estate, Luxury Goods)       | ⚠️ Partial                                                 | ⚠️ Partial                                                        | **Partially Covered**    | Detected only if purchases are captured via financial flows and metadata |
| Complex Legal Structures & Instrument-Based Layering             | ❌                                                          | ⚠️ Partial                                                        | **Partially Covered**    | Legal instrument metadata may not be standard in [coredata](https://github.com/SoteriaInitiative/coredata) financial transaction records |


## System Context
The illustration below outlines the basic principles of how three financial 
institutions might combined their sheared knowledge about particular threat scenarios
to improve their collective detection capability. Critically, no personal identifiable data
is shared but only abstract matrix data, weights, are shared with the server.

<div style="background:white; padding:10px; display:inline-block;">
  <img src="FedMLIllustration.svg" alt="Federated ML Illustration" />
</div>
