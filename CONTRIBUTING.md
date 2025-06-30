# Contributing to AdaptiveRAG

We welcome contributions to AdaptiveRAG! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/adaptiverag.git
   cd adaptiverag
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 📝 Development Guidelines

### Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
black .
isort .
flake8 .
mypy adaptive_rag/
```

### Testing

Run tests before submitting:
```bash
pytest tests/
python quick_test.py
```

### Documentation

- Update docstrings for new functions/classes
- Add type hints to all functions
- Update README.md if adding new features

## 🔄 Contribution Process

### 1. Create an Issue

Before starting work, create an issue describing:
- The problem you're solving
- Your proposed solution
- Any breaking changes

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

- Write clean, documented code
- Add tests for new functionality
- Ensure all tests pass
- Follow the existing code style

### 4. Commit Changes

Use conventional commit messages:
```bash
git commit -m "feat: add new retrieval method"
git commit -m "fix: resolve memory leak in cache"
git commit -m "docs: update API documentation"
```

### 5. Submit Pull Request

- Fill out the PR template
- Link to related issues
- Ensure CI passes
- Request review from maintainers

## 🧪 Types of Contributions

### Bug Fixes
- Fix existing functionality
- Add regression tests
- Update documentation if needed

### New Features
- Implement new retrieval methods
- Add evaluation metrics
- Extend configuration options

### Documentation
- Improve README
- Add tutorials
- Fix typos and clarifications

### Performance Improvements
- Optimize existing code
- Add benchmarks
- Profile memory usage

## 📋 Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No breaking changes (or clearly documented)

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Environment details**
   - Python version
   - Operating system
   - Package versions

2. **Steps to reproduce**
   - Minimal code example
   - Expected vs actual behavior
   - Error messages/stack traces

3. **Additional context**
   - Screenshots (if applicable)
   - Related issues

## 💡 Feature Requests

For feature requests, provide:

1. **Use case description**
   - What problem does it solve?
   - Who would benefit?

2. **Proposed solution**
   - How should it work?
   - API design ideas

3. **Alternatives considered**
   - Other approaches
   - Why this approach is better

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For private inquiries

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in academic papers (if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AdaptiveRAG! 🎉
