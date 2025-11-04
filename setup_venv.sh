#!/bin/bash

# Stop on error
set -e

echo "🚀 Setting up Python 3.11 environment (venv) for introspect..."

# 1️⃣ Install Python 3.11 if missing
if ! command -v python3.11 &> /dev/null
then
    echo "🔧 Installing Python 3.11..."
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
else
    echo "✅ Python 3.11 already installed."
fi

# 2️⃣ Go to project directory
cd "$(dirname "$0")"

# 3️⃣ Remove old venv (from Python 3.12)
if [ -d "venv" ]; then
    echo "🧹 Removing old venv (Python 3.12)..."
    rm -rf venv
fi

# 4️⃣ Create new virtual environment
echo "📦 Creating new virtual environment with Python 3.11..."
python3.11 -m venv venv

# 5️⃣ Activate environment
source venv/bin/activate

# 6️⃣ Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 7️⃣ Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📚 Installing project dependencies..."
    pip install -r requirements-dev.txt
else
    echo "⚠️ No requirements.txt found — skipping dependency installation."
fi

# 8️⃣ Install TensorFlow Lite Runtime
echo "🤖 Installing TensorFlow Lite Runtime..."
pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.14.0-cp311-cp311-linux_x86_64.whl

# 9️⃣ Verify installation
python -c "import tflite_runtime.interpreter as tflite; print('✅ TensorFlow Lite Runtime installed successfully!')"

echo "🎉 Setup complete!"
echo "👉 To activate the environment later, run:"
echo "source venv/bin/activate"
