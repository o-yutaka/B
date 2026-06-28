# 002 Decision Loop

BLACK v1 Phase 2 defines the data contracts for the decision loop without implementing algorithms.

```mermaid
sequenceDiagram
    participant Runtime as RuntimeEngine
    participant Bus as EventBus
    participant Explorer as IExplorer
    participant Reasoner as IReasoner
    participant Kernel as IKernel
    participant Governance as IGovernance
    participant Memory as IMemory
    Runtime->>Bus: lifecycle events
    Bus->>Explorer: intent/reality request
    Explorer-->>Bus: EvidencePacket
    Bus->>Reasoner: DecisionPacket draft
    Reasoner-->>Bus: reasoning contract response
    Bus->>Kernel: DecisionPacket
    Kernel-->>Governance: verdict request
    Governance-->>Bus: verdict
    Bus->>Memory: decision record
```

All subsystem communication remains EventBus mediated. Interfaces expose lifecycle methods compatible with RuntimeEngine: `initialize`, `register`, `health`, and `shutdown`.
