#!/bin/bash
# ============================================
# Build script for Intel Mac (x86_64)
# ============================================
echo "🔨 Building Wolf God for Intel Mac (x86_64)..."

# Check architecture
ARCH=$(python -c "import platform; print(platform.machine())")
if [ "$ARCH" != "x86_64" ]; then
    echo "⚠️  Warning: This script is for Intel Mac but detected: $ARCH"
    echo "   For Apple Silicon, use build_arm.sh instead"
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
rm -rf build dist/WolfGod_x86_64.app dist/WolfGod_x86_64.zip

# Build
echo "⚙️  Building app..."
pyinstaller --noconfirm --windowed \
    --name "WolfGod_x86_64" \
    --add-data "bgm.wav:." \
    --add-data "coin.wav:." \
    --add-data "explode.wav:." \
    main.py

# Zip the app
echo "📦 Zipping app..."
cd dist && zip -r WolfGod_x86_64.zip WolfGod_x86_64.app
cd ..

echo ""
echo "✅ Build complete!"
echo "📁 Output: dist/WolfGod_x86_64.zip"
echo "📁 Output: dist/WolfGod_x86_64.app"
echo ""
echo "📤 Share dist/WolfGod_x86_64.zip with Intel Mac users"
echo "   M1/M2/M3 users can also run this via Rosetta 2"
