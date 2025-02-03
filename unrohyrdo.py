import ctypes
import random
import time
import threading
import winsound
import os

# Load necessary Windows API functions
user32 = ctypes.windll.user32
gdi = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

# Get screen size
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

# Get device context for the screen
hdc = user32.GetDC(0)

# Path to "hydro1.wav" in the Downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
sound_file_path = os.path.join(downloads_path, "hydro1.wav")

# Check if the sound file exists
if not os.path.exists(sound_file_path):
    ctypes.windll.user32.MessageBoxW(0, "Error: 'hydro1.wav' not found in Downloads.", "File Not Found", 0x10)
    exit()

# Function to show warning messages
def show_warning(title, message):
    response = ctypes.windll.user32.MessageBoxW(0, message, title, 0x4 | 0x30)  # 0x4 = Yes/No, 0x30 = Warning icon
    return response == 6  # Returns True if "Yes" is clicked

# First warning
if not show_warning("⚠ FIRST WARNING", "This is malware. Run?\n\n(You may need to run it twice if effects don't start.)"):
    exit()

# Second warning
if not show_warning("⚠ LAST WARNING", "Are you sure? I AM NOT RESPONSIBLE FOR DAMAGES!"):
    exit()

# Function to play "hydro1.wav" once
def play_sound():
    try:
        winsound.PlaySound(sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to create extreme screen distortion and effects
def extreme_screen_effects():
    balls = []
    while True:
        try:
            # Create random balls that bounce around the screen
            if random.random() < 0.05:
                ball = {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "dx": random.choice([-1, 1]) * random.randint(10, 15),
                    "dy": random.choice([-1, 1]) * random.randint(10, 15),
                    "radius": random.randint(30, 100),
                    "color": random.choice([0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF])
                }
                balls.append(ball)

            for ball in balls:
                ball["x"] += ball["dx"]
                ball["y"] += ball["dy"]

                if ball["x"] <= 0 or ball["x"] >= width:
                    ball["dx"] = -ball["dx"]
                if ball["y"] <= 0 or ball["y"] >= height:
                    ball["dy"] = -ball["dy"]

                gdi.Ellipse(hdc, ball["x"], ball["y"], ball["x"] + ball["radius"], ball["y"] + ball["radius"])

            x = random.randint(0, width - 100)
            y = random.randint(0, height - 100)
            w = random.randint(50, 400)
            h = random.randint(50, 400)
            color = random.choice([0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0xFFFF00])
            gdi.PatBlt(hdc, x, y, w, h, color)

            time.sleep(random.uniform(0.05, 0.1))
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to simulate random warning messages
def random_window_flash():
    messages = [":) :)", "STILL USING THIS COMPUTER?", "SYSTEM ERROR", "MALWARE DETECTED"]
    while True:
        try:
            message = random.choice(messages)
            ctypes.windll.user32.MessageBoxW(0, message, "WARNING", 0x10)
            time.sleep(random.uniform(0.5, 1))
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to show bouncing colored text
def random_text_overlay():
    text = "unrohydro!!!"
    colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
    while True:
        try:
            x = random.randint(0, width - 100)
            y = random.randint(0, height - 50)
            color = random.choice(colors)
            gdi.SetTextColor(hdc, color)
            gdi.TextOutW(hdc, x, y, text, len(text))
            time.sleep(random.uniform(0.1, 0.5))
        except Exception as e:
            print(f"Error: {e}")
            break

# Start sound effect (only once)
play_sound()

# Start screen effects in a separate thread
screen_thread = threading.Thread(target=extreme_screen_effects, daemon=True)
screen_thread.start()

# Start random window popups in a separate thread
window_thread = threading.Thread(target=random_window_flash, daemon=True)
window_thread.start()

# Start text overlay in a separate thread
text_thread = threading.Thread(target=random_text_overlay, daemon=True)
text_thread.start()

# Keep the script running forever
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Script interrupted by user.")
