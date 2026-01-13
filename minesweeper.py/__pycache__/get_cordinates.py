import pyautogui
import time

print("Move your mouse to the positions and note the coordinates shown below.")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Position: ({x}, {y})", end='\r')
        time.sleep(0.1)
        if KeyboardInterrupt:
            break
except KeyboardInterrupt:
    print("\nDone!") 
    