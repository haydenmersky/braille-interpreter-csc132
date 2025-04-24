import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter

def load_gui():
    # Create the main window
    root = customtkinter.CTk()
    root.title("Braille Interpreter")
    root.geometry("800x600")  # Set the window size

    # Left Frame: Display the image
    left_frame = customtkinter.CTkFrame(root, width=400, height=600)
    left_frame.pack(side="left", fill="both", expand=True)

    # Load and display the image
    try:
        img = Image.open("cameraScan.png")
        img = img.resize((380, 500), Image.Resampling.LANCZOS)  # Resize the image to fit the frame
        img_tk = ImageTk.PhotoImage(img)
        img_label = customtkinter.CTkLabel(left_frame, image=img_tk, text="")
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=20)
    except FileNotFoundError:
        error_label = customtkinter.CTkLabel(left_frame, text="cameraScan.png not found", font=("Arial", 16))
        error_label.pack(pady=20)

    # Right Frame: Display the recognized lines
    right_frame = customtkinter.CTkFrame(root, width=400, height=600)
    right_frame.pack(side="right", fill="both", expand=True)

    # Add a scrollable text widget to display recognized lines
    text_scrollbar = Scrollbar(right_frame)
    text_scrollbar.pack(side="right", fill="y")

    text_widget = Text(right_frame, wrap="word", yscrollcommand=text_scrollbar.set, font=("Arial", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_scrollbar.config(command=text_widget.yview)

    # Load and display the contents of recognized_lines.txt
    try:
        with open("recognized_lines.txt", "r") as file:
            lines = file.read()
            text_widget.insert("1.0", lines)  # Insert text at the beginning
    except FileNotFoundError:
        text_widget.insert("1.0", "recognized_lines.txt not found")

    # Run the main loop
    root.mainloop()

# Call the function to load the GUI
load_gui()