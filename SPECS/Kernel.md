# Kernel Specification

The kernel consumes `DecisionPacket` contracts and emits governance-compatible verdict state. Phase 2 adds the `IKernel` abstract interface and immutable packet contracts only; it does not implement decision algorithms.

```mermaid
flowchart TD
    DP[DecisionPacket] --> K[IKernel]
    K --> V[Verdict]
    V --> EP[ExecutionPacket]
    V --> M[Memory]
```

The kernel must register through RuntimeEngine and communicate through EventBus. Direct subsystem coupling is prohibited.
