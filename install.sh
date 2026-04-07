#!/data/data/com.termux/files/usr/bin/bash

# === qwen-termux by TiBaff ===

CYAN="\033[96m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BOLD="\033[1m"
R="\033[0m"

AI_DIR="$HOME/ai"
AI_PY_URL="https://raw.githubusercontent.com/TiBaff/qwen-termux/refs/heads/main/ai.py"

echo -e "${BOLD}${CYAN}"
echo "╔══════════════════════════════════╗"
echo "║     qwen-termux by TiBaff     ║"
echo "╚══════════════════════════════════╝"
echo -e "${R}"

# --- Step 1: Update packages ---
echo -e "${YELLOW}[1/6] Updating Termux packages...${R}"
pkg update -y && pkg upgrade -y

# --- Step 2: Install dependencies ---
echo -e "${YELLOW}[2/6] Installing required packages...${R}"
pkg install -y python curl git

# --- Step 3: Install Python deps ---
echo -e "${YELLOW}[3/6] Installing Python dependencies...${R}"
pip install requests --break-system-packages 2>/dev/null || pip install requests

# --- Step 4: Install Ollama ---
echo -e "${YELLOW}[4/6] Installing Ollama...${R}"
if command -v ollama &>/dev/null; then
    echo -e "${GREEN}Ollama already installed, skipping.${R}"
else
    pkg install -y ollama
fi

# --- Step 5: Download ai.py ---
echo -e "${YELLOW}[5/6] Downloading ai.py...${R}"
mkdir -p "$AI_DIR"
curl -fsSL "$AI_PY_URL" -o "$AI_DIR/ai.py"
chmod +x "$AI_DIR/ai.py"

# --- Step 6: Pull models ---
echo -e "${YELLOW}[6/6] Pulling AI models (this may take a while)...${R}"

echo -e "${CYAN}Starting Ollama server in background...${R}"
ollama serve &>/dev/null &
OLLAMA_PID=$!
sleep 3

echo -e "${CYAN}Pulling qwen2.5:3b (fast)...${R}"
ollama pull qwen2.5:3b

echo -e "${CYAN}Pulling qwen3:4b (thinking)...${R}"
ollama pull qwen3:4b

kill $OLLAMA_PID 2>/dev/null

# --- Alias ---
echo -e "${YELLOW}Setting up 'ai' command...${R}"
SHELL_RC="$HOME/.bashrc"
if ! grep -q "alias ai=" "$SHELL_RC" 2>/dev/null; then
    echo "alias ai='python $AI_DIR/ai.py'" >> "$SHELL_RC"
fi

echo ""
echo -e "${BOLD}${GREEN}✓ Installation complete!${R}"
echo ""
echo -e "To start: ${BOLD}source ~/.bashrc && ai${R}"
echo -e "Or:       ${BOLD}python ~/ai/ai.py${R}"
echo ""
echo -e "${YELLOW}Usage:${R}"
echo "  ollama serve     — start Ollama (required before running ai)"
echo "  ai               — launch the AI menu"
echo "  /memory          — edit AI memory inside chat"
echo "  /clear           — clear session history"
echo "  /exit            — exit chat"
