#!/usr/bin/env python3
"""
AdaptiveRAG: Intelligent Adaptive Retrieval-Augmented Generation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="adaptiverag",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent Adaptive Retrieval-Augmented Generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/adaptiverag",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
        "experiments": [
            "matplotlib>=3.3",
            "seaborn>=0.11",
            "plotly>=5.0",
            "jupyter>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "adaptiverag=adaptive_rag.main:main",
            "adaptiverag-experiment=run_experiments:main",
        ],
    },
    include_package_data=True,
    package_data={
        "adaptive_rag": [
            "config/*.yaml",
            "data/*.json",
            "data/*.jsonl",
        ],
    },
    keywords=[
        "retrieval-augmented generation",
        "RAG",
        "natural language processing",
        "information retrieval",
        "machine learning",
        "artificial intelligence",
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/adaptiverag/issues",
        "Source": "https://github.com/your-username/adaptiverag",
        "Documentation": "https://adaptiverag.readthedocs.io/",
    },
)
