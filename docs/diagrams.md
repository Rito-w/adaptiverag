# 📊 图表和可视化

本页面展示了 AdaptiveRAG 文档中使用的各种图表和可视化内容。

## 🔄 流程图

### 基础流水线流程

```mermaid
flowchart LR
    A[查询] --> B[分解]
    B --> C[规划]
    C --> D[检索]
    D --> E[重排]
    E --> F[生成]
    F --> G[响应]
```

### 详细处理流水线

```mermaid
flowchart TD
    Start([用户查询]) --> Analyze{查询分析}
    Analyze -->|简单| DirectRetrieval[直接检索]
    Analyze -->|复杂| TaskDecomp[任务分解]

    TaskDecomp --> SubTask1[子任务 1]
    TaskDecomp --> SubTask2[子任务 2]
    TaskDecomp --> SubTaskN[子任务 N]

    DirectRetrieval --> Retrieve[多重检索]
    SubTask1 --> Retrieve
    SubTask2 --> Retrieve
    SubTaskN --> Retrieve

    Retrieve --> Rerank[上下文重排]
    Rerank --> Generate[自适应生成]
    Generate --> End([最终响应])

    style Start fill:#e1f5fe
    style End fill:#e8f5e8
    style Analyze fill:#fff3e0
    style Retrieve fill:#f3e5f5
    style Generate fill:#fce4ec
```

## 🏗️ 架构图

### 组件架构

```mermaid
graph TB
    subgraph "用户界面"
        UI[Web UI]
        API[REST API]
        CLI[命令行]
    end

    subgraph "核心引擎"
        Engine[AdaptiveRAG 引擎]
        Config[配置管理器]
        Cache[缓存管理器]
    end

    subgraph "处理组件"
        TD[任务分解器]
        RP[检索规划器]
        MR[多重检索器]
        CR[上下文重排器]
        AG[自适应生成器]
    end

    subgraph "外部集成"
        FlexRAG[FlexRAG 组件]
        FlashRAG[FlashRAG 数据集]
        LLM[语言模型]
        Search[搜索 API]
    end

    subgraph "存储"
        DB[(向量数据库)]
        FS[(文件系统)]
        Logs[(日志)]
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

## 📈 实验流程

### 评估流水线

```mermaid
sequenceDiagram
    participant User as 用户
    participant Runner as 基准测试运行器
    participant Loader as 数据集加载器
    participant Method as RAG 方法
    participant Evaluator as 指标评估器
    participant Analyzer as 结果分析器

    User->>Runner: 开始实验
    Runner->>Loader: 加载数据集
    Loader-->>Runner: 数据集就绪

    loop 对每个样本
        Runner->>Method: 处理查询
        Method-->>Runner: 生成响应
        Runner->>Evaluator: 计算指标
        Evaluator-->>Runner: 指标分数
    end

    Runner->>Analyzer: 聚合结果
    Analyzer-->>Runner: 分析报告
    Runner-->>User: 实验完成
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
