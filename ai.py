#!/usr/bin/env python3
import subprocess
import json
import os
import sys

# --- Config ---
MEMORY_FILE = os.path.expanduser("~/.ai_memory.txt")
HISTORY_FILE = os.path.expanduser("~/.ai_history.json")
FAST_MODEL = "qwen2.5:3b"
THINK_MODEL = "qwen3:4b"
SYSTEM_PROMPT = """You are a helpful, concise assistant running locally on an Android device via Termux and Ollama. 
Be direct and practical. Prefer short answers unless detail is needed."""

# --- Colors ---
R = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
RED = "\033[91m"

def clear():
    os.system("clear")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_memory(text):
    with open(MEMORY_FILE, "w") as f:
        f.write(text)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def build_system(memory):
    s = SYSTEM_PROMPT
    if memory:
        s += f"\n\n[Memory from previous sessions]:\n{memory}"
    return s

def stream_response(history, user_input, memory, model, is_thinking=False):
    messages = [{"role": "system", "content": build_system(memory)}]
    for h in history:
        messages.append(h)
    messages.append({"role": "user", "content": user_input})

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": True
    })

    proc = subprocess.Popen(
        ["curl", "-s", "-X", "POST", "http://localhost:11434/api/chat",
         "-H", "Content-Type: application/json", "-d", payload],
        stdout=subprocess.PIPE, text=True
    )

    full_response = ""
    in_think = False

    if is_thinking:
        print(f"{GRAY}Thinking...{R}")

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            chunk = data.get("message", {}).get("content", "")
            if not chunk:
                continue

            if is_thinking:
                i = 0
                while i < len(chunk):
                    if not in_think:
                        idx = chunk.find("<think>", i)
                        if idx == -1:
                            token = chunk[i:]
                            print(f"{GREEN}{token}{R}", end="", flush=True)
                            full_response += token
                            break
                        else:
                            token = chunk[i:idx]
                            if token:
                                print(f"{GREEN}{token}{R}", end="", flush=True)
                                full_response += token
                            in_think = True
                            i = idx + 7
                    else:
                        idx = chunk.find("</think>", i)
                        if idx == -1:
                            print(f"{GRAY}{chunk[i:]}{R}", end="", flush=True)
                            break
                        else:
                            print(f"{GRAY}{chunk[i:idx]}{R}", end="", flush=True)
                            print(f"\n{BOLD}AI:{R} ", end="", flush=True)
                            in_think = False
                            i = idx + 8
            else:
                print(f"{GREEN}{chunk}{R}", end="", flush=True)
                full_response += chunk

        except json.JSONDecodeError:
            continue

    proc.wait()
    print()
    return full_response.strip()

def update_memory_prompt(current_memory):
    print(f"\n{YELLOW}Current memory:{R}")
    print(current_memory if current_memory else "(empty)")
    print(f"\n{YELLOW}Enter new memory content (or press Enter to keep current):{R}")
    print(f"{GRAY}Tip: write key facts about yourself, preferences, ongoing tasks{R}")
    new_mem = input("> ").strip()
    if new_mem:
        save_memory(new_mem)
        print(f"{GREEN}Memory updated.{R}")
    else:
        print(f"{GRAY}Memory unchanged.{R}")

def chat_session(model_type):
    clear()
    model_label = "Fast (qwen2.5:3b)" if model_type == "fast" else "Thinking (qwen3:4b)"
    print(f"{BOLD}{CYAN}=== qwen-termux by TiBaff — {model_label} ==={R}")
    print(f"{GRAY}Commands: /exit  /clear  /memory{R}\n")

    history = load_history()
    memory = load_memory()
    is_thinking = model_type == "think"
    model = THINK_MODEL if is_thinking else FAST_MODEL

    while True:
        try:
            user_input = input(f"{BOLD}You:{R} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{GRAY}Exiting chat...{R}")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break
        elif user_input == "/clear":
            history = []
            save_history(history)
            print(f"{GRAY}Session history cleared.{R}")
            continue
        elif user_input == "/memory":
            update_memory_prompt(memory)
            memory = load_memory()
            continue

        print(f"\n{BOLD}AI:{R} ", end="", flush=True)
        response = stream_response(history, user_input, memory, model, is_thinking)

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})
        save_history(history)
        print()

def main_menu():
    while True:
        clear()
        print(f"{BOLD}{CYAN}╔══════════════════════════════╗")
        print(f"║    qwen-termux by TiBaff     ║")
        print(f"╚══════════════════════════════╝{R}\n")
        print(f"  {BOLD}1.{R} Fast chat       {GRAY}(qwen2.5:3b){R}")
        print(f"  {BOLD}2.{R} Thinking chat   {GRAY}(qwen3:4b){R}")
        print(f"  {BOLD}3.{R} Edit memory")
        print(f"  {BOLD}4.{R} Clear session history")
        print(f"  {BOLD}5.{R} Exit\n")

        try:
            choice = input(f"{BOLD}Choose [1-5]:{R} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{GRAY}Bye!{R}")
            sys.exit(0)

        if choice == "1":
            chat_session("fast")
        elif choice == "2":
            chat_session("think")
        elif choice == "3":
            memory = load_memory()
            update_memory_prompt(memory)
            input(f"\n{GRAY}Press Enter to continue...{R}")
        elif choice == "4":
            save_history([])
            print(f"{GREEN}Session history cleared.{R}")
            input(f"{GRAY}Press Enter to continue...{R}")
        elif choice == "5":
            print(f"\n{GRAY}Bye!{R}")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
