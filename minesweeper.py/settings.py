import pyautogui
import time
import keyboard


print("Move your mouse to the positions and note the coordinates shown below.")
print("Press Ctrl+C to stop.\n")

width, height = pyautogui.size()
print(f"Screen size: {width}x{height}")


try:
    while True:
        x, y = pyautogui.position()
        print(f"Position: ({x}, {y})", end='\r')
        time.sleep(0.1)

        if keyboard.is_pressed('f8'):
            saved_position1 = (x, y)
            print(f"\nSaved Position 1: {saved_position1}")
        if keyboard.is_pressed('f9'):
            saved_position2 = (x, y)
            print(f"\nSaved Position 2: {saved_position2}")
except KeyboardInterrupt:
    print("\nDone!") 




#comp viz settings.py 413,248
COMP_VIZ_TOP_LEFT = saved_position1  # top-left corner
COMP_VIZ_BOT_RIGHT = (saved_position2[0] - saved_position1[0], saved_position2[1] - saved_position1[1])  # width=952-413, height=673-253 
ENABLE_PREVIEW = True
#coloums and rows in the minesweeper grid
GRID_COLS = 18
GRID_ROWS = 14
rows = 14
cols = 18

#settings need editing.
#1366x768
#690x400
# +3 -4
#Perfect! Let’s start turning your readable board into something your solver can actually reason about. We’ll go step by step, starting with a numeric board and basic inference rules.

#Step 1 — Convert string board → numeric board

#Right now your board is a 2D list of strings like "unrevealed", "empty", "1", "2", etc.

#For solver logic, it’s much easier to work with numbers:
'''# Add this method inside your class
def board_to_numeric(self, board):
    """
    Converts the string board into numbers for easier solver logic.
    -1 = unrevealed
     0 = empty
     1-7 = number tiles
    """
    mapping = {
        'unrevealed': -1,
        'empty': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7
    }

    numeric_board = [
        [mapping.get(cell, -2) for cell in row]  # unknown -> -2
        for row in board
    ]
    return numeric_board
'''
'''Step 2 — Identify “frontier” cells

A frontier cell is:

A revealed number (1–7)

That has unrevealed neighbors

We’ll write a method to collect all frontier cells:

def get_frontier_cells(self, numeric_board):
    """
    Returns a list of coordinates (r, c) of revealed number cells
    that have at least one unrevealed neighbor.
    """
    rows, cols = len(numeric_board), len(numeric_board[0])
    frontier = []

    for r in range(rows):
        for c in range(cols):
            val = numeric_board[r][c]
            if val > 0:  # number tile
                # check 8 neighbors
                neighbors = [
                    (r+dr, c+dc)
                    for dr in [-1,0,1]
                    for dc in [-1,0,1]
                    if not (dr == 0 and dc == 0)
                ]
                if any(0 <= nr < rows and 0 <= nc < cols and numeric_board[nr][nc] == -1
                       for nr, nc in neighbors):
                    frontier.append((r, c))
    return frontier

    If the number of unrevealed neighbors equals the number on the cell → all neighbors are mines.
    def rule_flag_obvious_mines(self, numeric_board):
    """
    Returns a list of coordinates to flag as mines.
    """
    mines_to_flag = []
    rows, cols = len(numeric_board), len(numeric_board[0])

    for r, c in self.get_frontier_cells(numeric_board):
        val = numeric_board[r][c]
        # get unrevealed neighbors
        neighbors = [
            (r+dr, c+dc)
            for dr in [-1,0,1]
            for dc in [-1,0,1]
            if not (dr==0 and dc==0)
            and 0 <= r+dr < rows
            and 0 <= c+dc < cols
            and numeric_board[r+dr][c+dc] == -1
        ]
        if len(neighbors) == val:
            mines_to_flag.extend(neighbors)

    
    
return mines_to_flag

What we have now

Convert string board → numeric board (board_to_numeric)

Detect frontier cells (get_frontier_cells)

Flag “obvious mines” based on simple rule (rule_flag_obvious_mines)

At this point, you can print the board and see which cells are guaranteed mines.

If you want, the next step can be:

Rule #2: Safe clicks

If a number minus already flagged neighbors = 0 → remaining unrevealed neighbors are safe to click.

This gives the solver the ability to actually make moves, not just flag mines.

Do you want me to add that next?
'''

'''Absolutely — I can guide you through how to build the skills and mindset to write this yourself, step by step. You’re basically talking about going from “I see code but can’t write it” → “I can read a problem, design an algorithm, and implement it.” Here’s a practical roadmap.

Step 1: Understand the problem deeply

Before writing any code, make sure you can describe the problem in plain English. For Minesweeper, for example:

Each cell can be: unrevealed, empty, a number, or a flag.

Numbers tell you how many mines are in neighboring cells.

A “frontier” is a revealed number with unrevealed neighbors.

Some simple rules exist:
If a number = unrevealed neighbors → all are mines.

If a number = flagged neighbors → all unrevealed neighbors are safe.

Exercise: Try drawing a small board on paper. Circle frontiers. Mark obvious mines and safe cells. This is literally what your program will have to do.

💡 If you can reason through it on paper, you can reason through it in code.

Step 2: Break the problem into tiny pieces

Instead of “write a solver for the whole board,” break it into atomic tasks.

Example for step 2 (finding frontier cells):

Loop through every cell. ✅

Check if it’s a number > 0. ✅

Look at all 8 neighbors. ✅

If at least one neighbor is unrevealed → add to frontier. ✅

Notice how each bullet point is one small logical operation. When coding, handle one bullet at a time, test it, then move on.

Step 3: Translate logic to code slowly

Here’s a technique that helps beginners:

Write comments first — no code, just plan the steps.'''