# BLACK Core Specification

BLACK Core is organized around runtime-compatible contracts:

- Ontology: canonical language for decisions.
- Interfaces: abstract subsystem boundaries.
- Packets: immutable data exchanged through EventBus.
- Registry: capability and dependency metadata registration.
- Runtime integration: lifecycle, dispatcher, packet router, canonical events, and adapters.

```mermaid
flowchart LR
    RuntimeEngine --> Lifecycle[RuntimeLifecycle]
    Lifecycle --> Router[PacketRouter]
    Router --> Dispatcher[Dispatcher/EventBus]
    Dispatcher --> Adapters[Runtime Adapters]
    Adapters --> Interfaces
    Interfaces --> Packets
    Ontology --> Packets
    Registry --> Interfaces
```

## Phase 3 Packet Flow

```mermaid
sequenceDiagram
    participant Runtime as RuntimeEngine
    participant Router as PacketRouter
    participant Bus as Dispatcher/EventBus
    participant Adapter as Adapter
    participant Module as Subsystem Interface
    Runtime->>Router: Contract packet
    Router->>Bus: Canonical event
    Bus->>Adapter: EventEnvelope
    Adapter->>Module: Interface call
    Module-->>Adapter: Contract result
    Adapter->>Bus: Canonical result event
```

Phase 3 establishes runtime connectivity only. Intelligence, search, reinforcement learning, MCTS, OpenMythos, decision-kernel logic, and world simulation remain outside this phase.
