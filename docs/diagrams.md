# 📊 Diagrams and Visualizations

This page demonstrates the various diagrams and visualizations used throughout the AdaptiveRAG documentation.

## 🔄 Process Flow Diagrams

### Basic Pipeline Flow

```mermaid
flowchart LR
    A[Query] --> B[Decompose]
    B --> C[Plan]
    C --> D[Retrieve]
    D --> E[Rerank]
    E --> F[Generate]
    F --> G[Response]
```

### Detailed Processing Pipeline

```mermaid
flowchart TD
    Start([User Query]) --> Analyze{Query Analysis}
    Analyze -->|Simple| DirectRetrieval[Direct Retrieval]
    Analyze -->|Complex| TaskDecomp[Task Decomposition]
    
    TaskDecomp --> SubTask1[Subtask 1]
    TaskDecomp --> SubTask2[Subtask 2]
    TaskDecomp --> SubTaskN[Subtask N]
    
    DirectRetrieval --> Retrieve[Multi-Retrieval]
    SubTask1 --> Retrieve
    SubTask2 --> Retrieve
    SubTaskN --> Retrieve
    
    Retrieve --> Rerank[Context Reranking]
    Rerank --> Generate[Adaptive Generation]
    Generate --> End([Final Response])
    
    style Start fill:#e1f5fe
    style End fill:#e8f5e8
    style Analyze fill:#fff3e0
    style Retrieve fill:#f3e5f5
    style Generate fill:#fce4ec
```

## 🏗️ Architecture Diagrams

### Component Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI[Web UI]
        API[REST API]
        CLI[Command Line]
    end
    
    subgraph "Core Engine"
        Engine[AdaptiveRAG Engine]
        Config[Configuration Manager]
        Cache[Cache Manager]
    end
    
    subgraph "Processing Components"
        TD[Task Decomposer]
        RP[Retrieval Planner]
        MR[Multi-Retriever]
        CR[Context Reranker]
        AG[Adaptive Generator]
    end
    
    subgraph "External Integrations"
        FlexRAG[FlexRAG Components]
        FlashRAG[FlashRAG Datasets]
        LLM[Language Models]
        Search[Search APIs]
    end
    
    subgraph "Storage"
        DB[(Vector Database)]
        FS[(File System)]
        Logs[(Logs)]
    end
    
    UI --> Engine
    API --> Engine
    CLI --> Engine
    
    Engine --> Config
    Engine --> Cache
    Engine --> TD
    Engine --> RP
    Engine --> MR
    Engine --> CR
    Engine --> AG
    
    TD --> LLM
    RP --> Config
    MR --> FlexRAG
    MR --> Search
    MR --> DB
    CR --> FlexRAG
    AG --> LLM
    
    Cache --> FS
    Engine --> Logs
    
    classDef ui fill:#e3f2fd
    classDef core fill:#fff3e0
    classDef processing fill:#e8f5e8
    classDef external fill:#fce4ec
    classDef storage fill:#f3e5f5
    
    class UI,API,CLI ui
    class Engine,Config,Cache core
    class TD,RP,MR,CR,AG processing
    class FlexRAG,FlashRAG,LLM,Search external
    class DB,FS,Logs storage
```

## 📈 Experimental Flow

### Evaluation Pipeline

```mermaid
sequenceDiagram
    participant User
    participant Runner as Benchmark Runner
    participant Loader as Dataset Loader
    participant Method as RAG Method
    participant Evaluator as Metrics Evaluator
    participant Analyzer as Result Analyzer
    
    User->>Runner: Start Experiment
    Runner->>Loader: Load Dataset
    Loader-->>Runner: Dataset Ready
    
    loop For each sample
        Runner->>Method: Process Query
        Method-->>Runner: Generated Response
        Runner->>Evaluator: Calculate Metrics
        Evaluator-->>Runner: Metric Scores
    end
    
    Runner->>Analyzer: Aggregate Results
    Analyzer-->>Runner: Analysis Report
    Runner-->>User: Experiment Complete
```

### Ablation Study Flow

```mermaid
flowchart TD
    Start([Start Ablation Study]) --> Config[Load Configuration]
    Config --> Methods{Select Methods}
    
    Methods --> Full[Full AdaptiveRAG]
    Methods --> NoDecomp[No Task Decomposition]
    Methods --> NoPlanning[No Strategy Planning]
    Methods --> SingleRet[Single Retriever]
    Methods --> NoRerank[No Reranking]
    Methods --> Baseline[Baseline Methods]
    
    Full --> Eval1[Evaluate]
    NoDecomp --> Eval2[Evaluate]
    NoPlanning --> Eval3[Evaluate]
    SingleRet --> Eval4[Evaluate]
    NoRerank --> Eval5[Evaluate]
    Baseline --> Eval6[Evaluate]
    
    Eval1 --> Results[Collect Results]
    Eval2 --> Results
    Eval3 --> Results
    Eval4 --> Results
    Eval5 --> Results
    Eval6 --> Results
    
    Results --> Analysis[Statistical Analysis]
    Analysis --> Visualization[Generate Plots]
    Visualization --> Report[Generate Report]
    Report --> End([Complete])
    
    style Start fill:#e1f5fe
    style End fill:#e8f5e8
    style Methods fill:#fff3e0
    style Analysis fill:#f3e5f5
```

## 🔍 Data Flow Diagrams

### Information Flow

```mermaid
graph LR
    subgraph "Input Processing"
        Q[Query] --> QP[Query Processing]
        QP --> QE[Query Embedding]
    end
    
    subgraph "Knowledge Sources"
        KB[(Knowledge Base)]
        WS[Web Search]
        DB[(Document Store)]
    end
    
    subgraph "Retrieval Processing"
        QE --> R1[Retriever 1]
        QE --> R2[Retriever 2]
        QE --> R3[Retriever 3]
        
        R1 --> KB
        R2 --> DB
        R3 --> WS
        
        KB --> D1[Documents 1]
        DB --> D2[Documents 2]
        WS --> D3[Documents 3]
    end
    
    subgraph "Context Processing"
        D1 --> Fusion[Result Fusion]
        D2 --> Fusion
        D3 --> Fusion
        
        Fusion --> Rerank[Reranking]
        Rerank --> Context[Final Context]
    end
    
    subgraph "Response Generation"
        Context --> Gen[Generator]
        Q --> Gen
        Gen --> Response[Final Response]
    end
    
    style Q fill:#e1f5fe
    style Response fill:#e8f5e8
    style Fusion fill:#fff3e0
    style Gen fill:#f3e5f5
```

## 📊 Performance Visualization

### Metric Comparison

```mermaid
xychart-beta
    title "Performance Comparison Across Methods"
    x-axis [AdaptiveRAG, Self-RAG, Naive RAG, RAPTOR]
    y-axis "Score" 0 --> 1
    bar [0.85, 0.72, 0.58, 0.68]
```

### Component Contribution

```mermaid
pie title Component Contribution to Performance
    "Task Decomposition" : 25
    "Strategy Planning" : 20
    "Multi-Retriever" : 30
    "Context Reranking" : 15
    "Adaptive Generation" : 10
```

## 🎯 Usage Examples

To include these diagrams in your documentation, simply use the `mermaid` code block:

````markdown
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```
````

### Supported Diagram Types

- **Flowcharts**: `flowchart` or `graph`
- **Sequence Diagrams**: `sequenceDiagram`
- **Class Diagrams**: `classDiagram`
- **State Diagrams**: `stateDiagram`
- **Gantt Charts**: `gantt`
- **Pie Charts**: `pie`
- **XY Charts**: `xychart-beta`

### Styling Options

You can customize diagram appearance using:
- `classDef` for defining styles
- `class` for applying styles
- `style` for individual node styling
- Color themes and variables

---

These diagrams help visualize the complex architecture and processes within AdaptiveRAG, making the documentation more accessible and easier to understand.
