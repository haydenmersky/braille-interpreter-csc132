import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter

carry_over = ""  # Variable to hold leftover characters; used in the update_char_label function and
                 # couldn't find any other way to do it without using a global variable

word_archive = [] # List to hold the already loaded words

def load_gui():
    # Create the main window
    root = customtkinter.CTk()
    root.title("Braille Interpreter")
    root.geometry("1000x700")  # Set the window size
    
    # Right Frame: Display the recognized lines
    right_frame = customtkinter.CTkFrame(root, width=475, height=200, fg_color="white", border_color="lightblue", border_width=4)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Add a header label above the text widget
    textHeader_label = customtkinter.CTkLabel(right_frame, text="Scanned Text:", font=("Arial", 20))
    textHeader_label.pack(side="top", pady=3)  # Add padding for spacing

    # Add a container frame for the text widget and scrollbar
    text_container = customtkinter.CTkFrame(right_frame, fg_color="white")  # Container for text and scrollbar
    text_container.pack(expand=True, fill="both", padx=10, pady=5)

    # Add a scrollable text widget to display recognized lines
    text_widget = Text(text_container, wrap="word", yscrollcommand=lambda *args: text_scrollbar.set(*args), font=("Arial", 12))
    text_widget.pack(side="left", expand=True, fill="both")

    # Add the scrollbar to the container frame
    text_scrollbar = Scrollbar(text_container, command=text_widget.yview)
    text_scrollbar.pack(side="right", fill="y")

    # Load the recognized_lines.txt content for the bottom frame
    try:
        with open("recognized_lines.txt", "r") as file:
            scannedText = file.read()
    except FileNotFoundError:
        scannedText = "Scanned text not found."

    # Insert the text while the widget is in the "normal" state
    text_widget.config(state="normal")
    text_widget.insert("1.0", scannedText)
    text_widget.config(state="disabled")  # Make the widget read-only

    scannedText = scannedText.replace("\n", " ")

    # Bottom Frame: Display eleven characters at a time
    bottom_frame = customtkinter.CTkFrame(root, height=400, fg_color="white", border_color="lightblue", border_width=4)
    bottom_frame.pack(side="bottom", fill="x")

    displayHeader_label = customtkinter.CTkLabel(bottom_frame, text="Displayed Characters:", font=("Arial", 20))
    displayHeader_label.pack(pady=3)

    char_label = customtkinter.CTkLabel(bottom_frame, text="", font=("Arial", 32))
    char_label.pack(pady=4)

    # Left Frame: Display the image
    left_frame = customtkinter.CTkFrame(root, width=475, height=600, fg_color="white", border_color="lightblue", border_width=4)
    left_frame.pack(side="left", fill="both", expand=True)
    left_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Create a container frame for the image and its header
    image_container = customtkinter.CTkFrame(left_frame)
    image_container.pack(side="top", expand=True)  # Center the container vertically

    # Add the image header label
    imageHeader_label = customtkinter.CTkLabel(image_container, text="Captured Image:", font=("Arial", 20))
    imageHeader_label.pack(side="top")  # Add padding below the label

    # Load and display the image
    try:
        img = Image.open("cameraScan.png")
        img_tk = ImageTk.PhotoImage(img)
        img_label = customtkinter.CTkLabel(image_container, image=img_tk, text="")
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(side="top")  # Place the image below the header
    except FileNotFoundError:
        error_label = customtkinter.CTkLabel(image_container, text="Camera image not found.", font=("Arial", 16))
        error_label.pack(side="top")  # Place the error message below the header

    current_index = 0
    
    # Function to update the character label with eleven characters at a time
    def update_char_label(event=None):
        global carry_over
        global word_archive
        nonlocal scannedText, current_index

        if not scannedText.strip():  # If scannedText is empty or only contains whitespace
            char_label.configure(text="End of Text")
            return

        if current_index >= len(scannedText):  # If we've reached the end of the text
            char_label.configure(text="End of Text")
            return

        # Initialize an empty string to hold the next characters
        next_chars = carry_over
        carry_over = ""  # Reset carry_over for the next iteration

        # Iterate through the text starting from the current index
        while current_index < len(scannedText):
            char = scannedText[current_index]
            current_index += 1  # Increment current_index here to avoid infinite loop

            # Stop if the length reaches 11 characters
            if len(next_chars) >= 11:
                carry_over += char  # Save the leftover character for the next press
                break

            # Add the character to the current string
            next_chars += char

            # Stop if a space or newline is encountered
            if char == " ":
                break

        # Update the label with the collected characters
        char_label.configure(text=next_chars)
        word_archive.append(next_chars)  # Add the current string to the word archive
    
    def revert_char_label(event=None):
        global carry_over
        global word_archive
        nonlocal scannedText, current_index
        if not word_archive:
            char_label.configure(text="No history")
            return 
        # Pop the last entry from word_archive
        last_string = word_archive.pop()
        # Decrement current_index by the length of the last string
        current_index -= len(last_string)
        current_index = max(0, current_index)
        # Update the label with the previous string if available
        char_label.configure(text=word_archive[-1])  # Display the previous string
            
    update_char_label()  # Display the first eleven characters initially

    # Bind the spacebar key to update the label, and the z key to revert it
    root.bind("<space>", update_char_label)
    root.bind("<z>", revert_char_label) 

    # Run the main loop
    root.mainloop()

# Call the function to load the GUI
load_gui()