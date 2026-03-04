# student_lunch-CLI – Safka 

With this tool, you can search by restaurant or area, and optionally specify a date (e.g., `Kaivopiha 5.3`).

By setting up a terminal alias, you can simply type:


in your terminal to launch the CLI.

---

## Features

- Search menus by **restaurant** or **area**
- Supports **custom dates** (`dd.mm`) like `ex 7.3`
- Supports **area aliases** (`stadi`, `ay`, `hk`)  
- Supports **restaurant aliases** (`kaivo`, `ex`, `che`)
- Shows **opening hours** for today or selected date
- Displays menus cleanly in CLI
- Handles multiple restaurants with the same name

---

## 1. Setup Instructions

### Step 1: Install Python 3 and pip

Make sure Python 3.8+ is installed.

Then:

```bash


pip3 install requests

git clone https://github.com/Aarouu/student_lunch-CLI.git
cd student_lunch-CLI
```

Optional to make this executable with command "safka" in terminal

```bash
chmod +x main.py
```

Add this with your own path in the end

```bash 
alias safka="python3 /full/path/to/main.py"
```

Save and reload 
```bash 
source ~/.bashrc   # or ~/.zshrc, ~/.config/fish/config.fish
```

You are now able to run 
```bash
safka
```

## Usage
kaivo           # Show today's menu for Kaivopiha
kaivo 5.3       # Show menu for Kaivopiha on March 5th
exa             # Show today's menu for Exactum
kumpula 7.3     # Show menu for the Kumpula area on March 7th
0               # Exit the CLI


