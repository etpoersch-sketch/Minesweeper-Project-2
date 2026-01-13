
from settings import width
from settings import height
import mss
import pyautogui
import numpy as np
import cv2
import sys
import os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings
class screen_capture_agent:
    def __init__(self):
        self.capture_process = None
        self.fps = None
        self.img = None
        self.stop_flag = False

        self.frame_count = 0

        self.w, self.h = pyautogui.size()
        print(f"screen resoloution: {self.w}x{self.h}")
        self.monitor = {
            'top': settings.COMP_VIZ_TOP_LEFT[1],
            'left': settings.COMP_VIZ_TOP_LEFT[0],
            'width': settings.COMP_VIZ_BOT_RIGHT[0],
            'height':settings.COMP_VIZ_BOT_RIGHT[1]
        }

    def capture_screen(self):   
        with mss.mss() as sct:
            while not self.stop_flag:
                self.img = sct.grab(self.monitor)
                self.img = np.array(self.img)

                self.frame_count += 1

                if settings.ENABLE_PREVIEW:
                    preview = cv2.resize(self.img[..., :3], (0, 0), fx=0.5, fy=0.5)
                    if self.frame_count % 360 == 0:
                        self.board = self.extract_board_state(rows=14, cols=18, threshold=4000)
                        self.print_board(self.board)
                    
                    cv2.imshow('Computer Vision', preview)
                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        self.stop()

    def stop(self):
        """Stop the screen capture"""
        self.stop_flag = True
        if settings.ENABLE_PREVIEW:
            cv2.destroyAllWindows()

    def extract_image(self):
        """returns image in BGR"""
        return self.img[..., :3]  # Remove alpha channel
    
    DISPLAY_MAP = {
        'unrevealed': '■',
        'empty': ' ',
        'flag': 'F',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        'unknown': '?'
}

    
    # Color map: maps colors in BGR
    color_map = {
        'unrevealed': [(81, 215, 170), (73, 209, 162)],
        'empty': [(153, 184, 215), (159, 194, 229)],
        'flag': [(7, 54, 242)],
        '1': [(208, 120, 32),(210, 118, 25),(198, 131, 65)],
        '2': [(74, 148, 78)],
        '3': [(52, 54, 211)],
        '4': [(162, 31, 123)],
        '5': [(0, 143, 255)],
        '6': [(169, 147, 4)],
        '7': [(75, 66, 64)],
    }

    def color_distance_sq(self, color1, color2):
        """equation for finding distance between colors (Euclidean distance)"""
        return int(sum((int(c1) - int(c2)) ** 2 for c1, c2 in zip(color1, color2)))
    
    def match_color(self, pixel, threshold=4000):
        """Find the best matching tile type for a pixel color"""
        best_match = None
        best_distance = float('inf')
        
        for tile_type, ref_colors in self.color_map.items():
            for ref_color in ref_colors:
                distance = self.color_distance_sq(pixel[:3], ref_color)
                if distance < best_distance:
                    best_distance = distance
                    best_match = tile_type
        
        if best_distance <= threshold:
            return best_match
        else:
            return 'unknown'
    
    def extract_board_state(self, rows=14, cols=18, threshold=4000):
        """
        Extract the minesweeper board state from the captured image.
        Returns a 2D list of tile types.
        """
        if self.img is None:
            return None
        
        # Get capture region dimensions
        left = settings.COMP_VIZ_TOP_LEFT[0]
        top = settings.COMP_VIZ_TOP_LEFT[1]
        w = settings.COMP_VIZ_BOT_RIGHT[0]
        h = settings.COMP_VIZ_BOT_RIGHT[1]
        
        # Calculate cell dimensions
        cell_width = w / cols
        cell_height = h / rows
        
        
        board = []
        
        # pixel detection for minesweeper cells
        for r in range(rows):
            row = []
            for c in range(cols):
                # Calculate center pixel of this cell
                px = int(c * cell_width + cell_width / 2 + settings.width / 455)
                py = int(r * cell_height + cell_height / 2 - settings.height / 192) - 1 
                py = max(0, min(py, self.img.shape[0] - 1))
                px = max(0, min(px, self.img.shape[1] - 1))
                # look at center 9 pixels of each cell for accuracy
                pixels = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        y = max(0, min(py + dy, self.img.shape[0] - 1))
                        x = max(0, min(px + dx, self.img.shape[1] - 1))
                        pixels.append(self.img[y, x])
                
                # Tile type voting for more accuracy when detecting the '1' cell
                tile_votes = [self.match_color(pixel, threshold) for pixel in pixels]
                if '1' in tile_votes:
                    tile_type = '1'
                elif tile_votes:
                    tile_type = Counter(tile_votes).most_common(1)[0][0]
                else:
                    tile_type = 'unknown'
                row.append(tile_type)
            board.append(row)
        
        return board 
    
    def print_board(self, board):
        rows = len(board)
        cols = len(board[0])

        # print/ formatting gives vision on the board from programs side
        print("    " + " ".join(f"{c:2}" for c in range(cols)))
        print("    " + "--" * cols)

        for r in range(rows):
            row_symbols = [
                self.DISPLAY_MAP.get(cell, '?') for cell in board[r]
            ]
            print(f"{r:2} | " + " ".join(f"{s:2}" for s in row_symbols))

    def get_frontier_cells(self, numeric_board):
        """
        gives a list of number cells with unrevealed cells beside it
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

    def rule_flag_obvious_mines(self, numeric_board):
        mines_to_flag = []
        rows, cols = len(numeric_board), len(numeric_board[0])

        for r in range(rows):
            for c in range(cols):
                val = numeric_board[r][c]
                if val > 0:  
                  
                    neighbors = [
                        (r+dr, c+dc)
                        for dr in [-1,0,1]
                        for dc in [-1,0,1]
                        if not (dr == 0 and dc == 0)
                    ]
                    unrevealed_count = sum(
                        0 <= nr < rows and 0 <= nc < cols and numeric_board[nr][nc] == -1
                        for nr, nc in neighbors
                    )
                    flagged_count = sum(
                        0 <= nr < rows and 0 <= nc < cols and numeric_board[nr][nc] == -2
                        for nr, nc in neighbors
                    )
                    if val == unrevealed_count + flagged_count:
                        mines_to_flag.extend([
                            (nr, nc)
                            for nr, nc in neighbors
                            if 0 <= nr < rows and 0 <= nc < cols and numeric_board[nr][nc] == -1
                        ])
        return mines_to_flag
    
    def flag_mines(self, mines_to_flag):
        for r, c in mines_to_flag:
            cell_x = settings.COMP_VIZ_TOP_LEFT[0] + c * settings.CELL_WIDTH + settings.CELL_WIDTH // 2
            cell_y = settings.COMP_VIZ_TOP_LEFT[1] + r * settings.CELL_HEIGHT + settings.CELL_HEIGHT // 2
            pyautogui.moveTo(cell_x, cell_y)
            pyautogui.middleClick()

if __name__ == '__main__':
    agent = screen_capture_agent()
    agent.capture_screen()

  
