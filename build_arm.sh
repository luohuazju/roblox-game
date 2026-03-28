#!/bin/bash
# ============================================
# Build script for Apple Silicon (M1/M2/M3)
# ============================================
echo "🔨 Building Wolf God for Apple Silicon (ARM)..."

# Check architecture
ARCH=$(python -c "import platform; print(platform.machine())")
if [ "$ARCH" != "arm64" ]; then
    echo "❌ Error: This script requires Apple Silicon Mac (M1/M2/M3)"
    echo "   Detected architecture: $ARCH"
    echo "   For Intel Mac, use build_intel.sh instead"
    exit 1
fi

# Check dependencies
echo "📦 Checking dependencies..."
pip install pygame pyinstaller --quiet

# Generate sound files
echo "🎵 Generating sound files..."
python generate_music.py
python generate_sfx.py

# Clean old build
echo "🧹 Cleaning old builds..."
rm -rf build dist/WolfGod_arm.app dist/WolfGod_arm.zip

# Build
echo "⚙️  Building app..."
pyinstaller --noconfirm --windowed \
    --name "WolfGod_arm" \
    --add-data "bgm.wav:." \
    --add-data "coin.wav:." \
    --add-data "explode.wav:." \
    main.py

# Zip the app
echo "📦 Zipping app..."
cd dist && zip -r WolfGod_arm.zip WolfGod_arm.app
cd ..

echo ""
echo "✅ Build complete!"
echo "📁 Output: dist/WolfGod_arm.zip"
echo "📁 Output: dist/WolfGod_arm.app"
echo ""
echo "📤 Share dist/WolfGod_arm.zip with Apple Silicon Mac users (M1/M2/M3)"
