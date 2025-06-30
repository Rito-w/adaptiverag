# Changelog

All notable changes to AdaptiveRAG will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial AdaptiveRAG implementation
- FlashRAG-inspired experimental framework
- FlexRAG component integration
- Comprehensive evaluation pipeline
- Multiple baseline method implementations
- Ablation study framework
- Configuration system with YAML support
- Automated dataset downloading
- Multi-metric evaluation (EM, F1, ROUGE-L, BERTScore)

### Features
- **Intelligent Query Analysis**: LLM-driven query understanding and task decomposition
- **Adaptive Retrieval Strategy**: Dynamic selection of optimal retrieval methods
- **Multi-Retriever Fusion**: Integration of keyword, dense, and web retrieval
- **Context Reranking**: Optimization of retrieved context for generation
- **Experimental Framework**: Complete evaluation pipeline for academic research

### Components
- Task Decomposer
- Retrieval Planner
- Multi-Retriever System
- Context Reranker
- Adaptive Generator
- Evaluation Framework

## [0.1.0] - 2024-01-XX

### Added
- Initial project structure
- Core AdaptiveRAG architecture
- Basic configuration system
- Experimental framework foundation
- Integration with FlexRAG components
- Baseline method implementations:
  - Naive RAG
  - Self-RAG
  - RAPTOR
- Evaluation metrics:
  - Exact Match
  - F1 Score
  - ROUGE-L
  - BERTScore
- Dataset support:
  - Natural Questions
  - HotpotQA
  - TriviaQA
  - MS MARCO
- Ablation study framework
- Documentation and examples

### Technical Details
- Python 3.8+ support
- PyTorch backend
- Transformers integration
- FAISS for vector search
- Comprehensive testing suite
- CI/CD pipeline setup

---

## Release Notes Template

### [Version] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security improvements
