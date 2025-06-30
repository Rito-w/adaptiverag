#!/bin/bash
# Setup script for AdaptiveRAG development environment

set -e

echo "🚀 Setting up AdaptiveRAG development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required, found $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "🛠️ Installing development dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw data/processed data/cache
mkdir -p experiments results logs
mkdir -p models checkpoints

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the environment: source venv/bin/activate"
echo "   2. Run tests: python -m pytest tests/"
echo "   3. Run quick test: python quick_test.py"
echo "   4. Start developing! 🚀"
