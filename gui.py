import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter

def load_gui():
    # Create the main window
    root = customtkinter.CTk()
    root.title("Braille Interpreter")
    root.geometry("1000x700")  # Set the window size

    # Bottom Frame: Display eleven characters at a time
    bottom_frame = customtkinter.CTkFrame(root, height=100)
    bottom_frame.pack(side="bottom", fill="x")

    char_label = customtkinter.CTkLabel(bottom_frame, text="", font=("Arial", 24))
    char_label.pack(pady=10)

    # Left Frame: Display the image
    left_frame = customtkinter.CTkFrame(root, width=475, height=600)
    left_frame.pack(side="left", fill="both", expand=True)
    left_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Right Frame: Display the recognized lines
    right_frame = customtkinter.CTkFrame(root, width=475, height=200)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Function to update the label with the next eleven characters
    def update_char_label(event=None):
        nonlocal current_index
        if recognized_text:
            # Initialize an empty string to hold the next characters
            next_chars = ""
        
            # Iterate through the text starting from the current index
            while current_index < len(recognized_text):
                char = recognized_text[current_index]
                current_index += 1  # Increment current_index here to avoid infinite loop
                if char == " ":  # Stop if a space is encountered
                    break
                next_chars += char
        
            # Update the label with the collected characters
            char_label.configure(text=next_chars)
        
            # Reset to the beginning if we reach the end of the text
            if current_index >= len(recognized_text):
                current_index = 0
        
            # Update the label with the collected characters
            char_label.configure(text=next_chars)
        
            # Reset to the beginning if we reach the end of the text
            if current_index >= len(recognized_text):
                current_index = 0

    # Load the recognized_lines.txt content for the bottom frame
    try:
        with open("recognized_lines.txt", "r") as file:
            recognized_text = file.read()
    except FileNotFoundError:
        recognized_text = "recognized_lines.txt not found"

    current_index = 0
    update_char_label()  # Display the first eleven characters initially

    # Bind the spacebar key to update the label
    root.bind("<space>", update_char_label)

    # Add a scrollable text widget to display recognized lines
    text_scrollbar = Scrollbar(right_frame)
    text_scrollbar.pack(side="right", fill="y")

    text_widget = Text(right_frame, wrap="word", yscrollcommand=text_scrollbar.set, font=("Arial", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_scrollbar.config(command=text_widget.yview)

    # Dynamically calculate the size of the text box
    text_box_width = 380  # Approximate width of the text box
    text_box_height = 500  # Approximate height of the text box

    # Load and display the image
    try:
        img = Image.open("cameraScan.png")
        img_tk = ImageTk.PhotoImage(img)
        img_label = customtkinter.CTkLabel(left_frame, image=img_tk, text="")
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=20)
    except FileNotFoundError:
        error_label = customtkinter.CTkLabel(left_frame, text="cameraScan.png not found", font=("Arial", 16))
        error_label.pack(pady=20)

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