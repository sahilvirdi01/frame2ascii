"""
ASCII Art Viewer — Image to GUI
--------------------------------
Converts any image to ASCII art and displays it in a Tkinter window.
Step 1 of building a real-time webcam ASCII converter.

Requirements:
    pip install pillow
    tkinter is built into Python (no install needed)
"""

import tkinter as tk
from PIL import Image


# ── 1. ASCII CHARACTER SET ───────────────────────────────────────────────────
# Characters ordered from darkest (most ink) → lightest (least ink)
# Each pixel's brightness maps to one of these characters.
ASCII_CHARS = "@%#*+=-:. "


# ── 2. CORE CONVERSION FUNCTIONS ─────────────────────────────────────────────

def pixel_to_ascii(brightness: int) -> str:
    """Map a grayscale brightness value (0–255) to an ASCII character."""
    # brightness 0 = black → index 0 (densest char)
    # brightness 255 = white → last index (lightest char)
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def image_to_ascii(image_path: str, output_width: int = 120) -> str:
    """
    Load an image and convert it to an ASCII string.

    Args:
        image_path:   Path to any image file (jpg, png, etc.)
        output_width: How many characters wide the output should be.
                      Larger = more detail but needs a bigger window.

    Returns:
        A multi-line string of ASCII characters representing the image.
    """
    # Step A: Open and convert to grayscale
    img = Image.open(image_path).convert("L")  # "L" = grayscale mode

    # Step B: Resize the image
    # Characters are roughly twice as tall as they are wide,
    # so we halve the height to avoid a vertically stretched result.
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    output_height = int(output_width * aspect_ratio * 0.45)  # 0.45 corrects char aspect
    img = img.resize((output_width, output_height))

    # Step C: Map every pixel to an ASCII character
    pixels = list(img.getdata())          # flat list of brightness values (0–255)
    ascii_chars = [pixel_to_ascii(p) for p in pixels]

    # Step D: Split flat list into rows matching image width
    rows = []
    for i in range(0, len(ascii_chars), output_width):
        rows.append("".join(ascii_chars[i : i + output_width]))

    return "\n".join(rows)


# ── 3. GUI DISPLAY ────────────────────────────────────────────────────────────

def show_ascii_in_window(ascii_art: str, image_path: str):
    """Display the ASCII art string inside a Tkinter window."""

    root = tk.Tk()
    root.title("ASCII Art Viewer")
    root.configure(bg="#0d0d0d")  # dark background

    # ── Top label showing the source file ──
    header = tk.Label(
        root,
        text=f"Source: {image_path}",
        font=("Courier New", 9),
        fg="#888888",
        bg="#0d0d0d",
        pady=4,
    )
    header.pack(fill="x")

    # ── Scrollable frame so large ASCII art doesn't get cut off ──
    frame = tk.Frame(root, bg="#0d0d0d")
    frame.pack(fill="both", expand=True)

    # Vertical + horizontal scrollbars
    v_scroll = tk.Scrollbar(frame, orient="vertical")
    h_scroll = tk.Scrollbar(frame, orient="horizontal")

    # Text widget to hold the ASCII art
    text_widget = tk.Text(
        frame,
        font=("Courier New", 6),   # small monospace font — critical for ASCII art!
        bg="#0d0d0d",
        fg="#39ff14",               # neon green — classic terminal look
        wrap="none",                # disable word-wrap so rows stay intact
        yscrollcommand=v_scroll.set,
        xscrollcommand=h_scroll.set,
        cursor="arrow",
        state="normal",
    )

    v_scroll.config(command=text_widget.yview)
    h_scroll.config(command=text_widget.xview)

    # Layout the scrollbars and text widget
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")
    text_widget.pack(fill="both", expand=True)

    # Insert the ASCII art and lock editing
    text_widget.insert("1.0", ascii_art)
    text_widget.config(state="disabled")

    # ── Bottom status bar ──
    line_count = ascii_art.count("\n") + 1
    col_count = len(ascii_art.split("\n")[0])
    status = tk.Label(
        root,
        text=f"Grid: {col_count} cols × {line_count} rows  |  Press Esc to close",
        font=("Courier New", 8),
        fg="#555555",
        bg="#0d0d0d",
        pady=3,
    )
    status.pack(fill="x")

    # Keyboard shortcut to close
    root.bind("<Escape>", lambda e: root.destroy())

    # Open window at a reasonable size (resizable)
    root.geometry("900x600")
    root.mainloop()


# ── 4. ENTRY POINT ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # You can pass an image path as a command-line argument:
    #   python ascii_image_gui.py photo.jpg
    # Or it will ask you to type one in.

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Enter path to your image file: ").strip()

    print(f"Converting '{path}' to ASCII art...")

    try:
        ascii_result = image_to_ascii(path, output_width=120)
        print("Done! Opening GUI window...")
        show_ascii_in_window(ascii_result, path)
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except Exception as e:
        print(f"Something went wrong: {e}")
