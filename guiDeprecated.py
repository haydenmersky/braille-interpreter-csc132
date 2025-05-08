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
    right_frame = customtkinter.CTkFrame(root, width=475, height=200)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

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
        text_widget.insert("1.0", "Scanned text not found.")

    # Bottom Frame: Display eleven characters at a time
    bottom_frame = customtkinter.CTkFrame(root, height=400)
    bottom_frame.pack(side="bottom", fill="x")

    displayHeader_label = customtkinter.CTkLabel(bottom_frame, text="Displayed Characters:", font=("Arial", 20))
    displayHeader_label.pack(pady=10)

    char_label = customtkinter.CTkLabel(bottom_frame, text="", font=("Arial", 32))
    char_label.pack(pady=10)

    # Left Frame: Display the image
    left_frame = customtkinter.CTkFrame(root, width=475, height=600)
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
        error_label = customtkinter.CTkLabel(image_container, text="cameraScan.png not found", font=("Arial", 16))
        error_label.pack(side="top")  # Place the error message below the header

    # Function to update the label with the next eleven characters
    def update_char_label(event=None):
        global carry_over
        nonlocal current_index
        if recognized_text:
            # Initialize an empty string to hold the next characters
            next_chars = carry_over
            carry_over = ""  # Reset carry_over for the next iteration

            # Check if we have reached the end of the text
            if current_index >= len(recognized_text):
                # Add the last word to the word_archive if it hasn't been added
                if next_chars:  # Add the last processed word if it exists
                    word_archive.append(next_chars)
                    current_index -= len(next_chars)  # Adjust current_index to point to the last word
                char_label.configure(text="End of Text")  # Display "End of Text"
                return

            # Iterate through the text starting from the current index
            while current_index < len(recognized_text):
                char = recognized_text[current_index]
                current_index += 1  # Increment current_index here to avoid infinite loop

                # Stop if the length reaches 11 characters
                if len(next_chars) >= 11:
                    carry_over += char  # Save the leftover character for the next press
                    break

                # Add the character to the current string
                next_chars += char

                # Stop if a space or newline is encountered
                if char == " " or char == "\n":
                    break
            
            # Remove any newline characters from the string
            next_chars = next_chars.replace("\n", "")

            # Update the label with the collected characters
            char_label.configure(text=next_chars)
            word_archive.append(next_chars)  # Add the current string to the word archive

    # Function to update the label with the previous eleven characters
    def revert_char_label(event=None):
        nonlocal current_index
        if word_archive:
            # Remove the last added string from the archive
            last_string = word_archive.pop()

            # Decrement current_index by the length of the last string
            current_index -= len(last_string)

            # Ensure current_index does not go below 0
            current_index = max(0, current_index)

            # Update the label with the previous string if available
            if word_archive:
                char_label.configure(text=word_archive[-1])
            else:
                char_label.configure(text="")  # Clear the label if no previous string exists
        else:
            # If word_archive is empty, reset the label and current_index
            char_label.configure(text="Start of text.")
            current_index = 0


    # Load the recognized_lines.txt content for the bottom frame
    try:
        with open("recognized_lines.txt", "r") as file:
            recognized_text = file.read()
    except FileNotFoundError:
        recognized_text = "Scanned text not found."

    current_index = 0
    update_char_label()  # Display the first eleven characters initially

    # Bind the spacebar key to update the label
    root.bind("<space>", update_char_label)
    root.bind("<z>", revert_char_label) 

    # Run the main loop
    root.mainloop()

# Call the function to load the GUI
load_gui()