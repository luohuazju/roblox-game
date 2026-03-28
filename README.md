# 🐺 Wolf God - Flying Game

A Python pygame game where you play as a **Giant Flying Wolf God** with supernatural powers!
Dodge enemies, collect coins, buy upgrades, and survive 12 increasingly chaotic levels.

## 🎮 Screenshots

> A supernatural Wolf God soaring through chaos!

## 🚀 Quick Start

### Requirements
- Python 3.10+
- pygame

### Install & Run
```bash
# Install dependencies
pip install pygame

# Generate sound files
python generate_music.py
python generate_sfx.py

# Run the game!
python main.py
```

## 🕹️ Controls

| Key | Action |
|-----|--------|
| ↑ / W | Fly up |
| ↓ / S | Fly down |
| SPACE | Fire missiles / Laser beam |
| D | ⚡ Thunder Clap |
| F | 💜 Spirit Explosion |
| H | 💚 Healing Howl |
| G | 🧊 Time Slow |
| S (menu) | Open Shop |
| LEFT/RIGHT | Change level |
| ESC | Back / Quit |

## 🗺️ Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | 🌙 Moonlit Meadow | Very easy - bombs only |
| 2 | 💨 Windy Peaks | + Birds |
| 3 | 🥞 Breakfast Blitz | + Pancakes & Spatulas |
| 4 | 🌶️ Spicy Desert | + Tanks & Hot Sauce |
| 5 | 🍯 Syrup Swamp | + Syrup Streams |
| 6 | 🦕 Dino Jungle | + Pterodactyls |
| 7 | ⚡ Neon Lab | + Lasers |
| 8 | 🌋 Volcano Peak | Fire and fury |
| 9 | ⛈️ Storm Fortress | Thunder and steel |
| 10 | 👽 Alien Dimension | Reality bends |
| 11 | 🌑 Shadow Realm | Darkness consumes all |
| 12 | 🐺 WOLF GOD FINALE | Endless chaos! |

## 🏪 Shop Upgrades

| Category | Upgrade | Effect |
|----------|---------|--------|
| 🛡️ Defense | Extra Life | +1 life (up to +10) |
| 🛡️ Defense | Spirit Shield | Block 1 hit |
| 🏃 Movement | Wolf Speed | Faster movement |
| 🏃 Movement | Ghost Form | Smaller hitbox |
| ⚙️ Utility | Coin Magnet | Coins fly to you |
| ⚙️ Utility | Double Coins | 2x coin value |
| ⚔️ Weapon | Soul Fang | Auto-shoot spirit fangs |
| ⚔️ Weapon | Rapid Fangs | Faster shooting |
| ⚔️ Weapon | Howl Missile | Homing missiles |
| ⚔️ Weapon | Moon Beam | Laser beam |
| 💜 Power | Thunder Clap | Lightning blast |
| 💜 Power | Spirit Explosion | Destroy all nearby |
| 💜 Power | Healing Howl | Restore 1 life |
| 💜 Power | Time Slow | Slow all enemies |

## 📦 Package for Mac

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "WolfGod" \
  --add-data "bgm.wav:." \
  --add-data "coin.wav:." \
  --add-data "explode.wav:." \
  main.py
# Find app in dist/
```

## 📁 Project Structure

```
roblox-game/
├── main.py              # Main game
├── generate_music.py    # Background music generator
├── generate_sfx.py      # Sound effects generator
└── README.md
```

## 🛠️ Built With
- Python 3.13
- pygame 2.6

## 👨‍💻 Authors
Leo & Angela - Built with ❤️ and chaos!
