# Solitaire Game (Python)

A Python implementation of the Solitaire card game built for the University of Manchester MATH20621 coursework.  
The game is played entirely in the terminal and includes mechanics such as valid move checking, blocking rules, and undo/reset functionality.

---

## 🎮 Overview
This project simulates a simplified form of Solitaire using a **stack-based game state**.  
Each stack contains a list of integers (1–9) representing cards, and the player moves cards between stacks following specific rules.

---

## ⚙️ How it Works
- The game state is stored as a dictionary with keys:
  - `stacks`: list of 6 stacks (each a list of integers)
  - `blocked`: boolean list for stacks that are blocked
  - `complete`: boolean list for stacks that are complete
- The game is displayed using ANSI colour formatting in the terminal for visual clarity.
- Users can make moves using letter commands (e.g. `AD4` moves 4 cards from stack A to D).
- Includes:
  - **Error handling** for invalid inputs  
  - **Undo functionality** (`U` command)  
  - **Reset functionality** (`R` command)  
  - **Automatic win detection**

---

## 🧠 Key Features
- Object-free, dictionary-based game state representation
- Randomised initial setup using `random.shuffle()`
- Comprehensive validation logic for legal/illegal moves
- Undo/Reset functionality preserving move history
- Colour-coded terminal output for clear game visuals

---

## 🧩 Example Commands
| Command | Description |
|----------|--------------|
| `AD`     | Move 1 card from A → D |
| `AD3`    | Move 3 cards from A → D |
| `R`      | Reset the game |
| `U`      | Undo previous move |
| `Ctrl + C` | Quit the game |

---

## 📘 Skills Demonstrated
- Algorithm design and state management  
- Exception handling and input parsing  
- Modular code structure  
- Terminal UI formatting with ANSI escape codes  

---

## ▶️ How to Run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:
   ```bash
   python solitaire.py
