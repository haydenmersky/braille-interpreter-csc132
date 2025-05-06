import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter
import serial
import time
import subprocess

USING_ARDUINO = False

carry_over = ""  # Variable to hold leftover characters; used in the update_char_label function and
                 # couldn't find any other way to do it without using a global variable

word_archive = [] # List to hold the already loaded words

is_processing = False # Flag to indicate if the program is currently processing a word

if USING_ARDUINO:
    arduino = serial.Serial('COM3', 9600, timeout=1)

# Function to run the camera_scan.py script
def run_camera_scan(mode):
    try:
        subprocess.run(["python", "camera_scan.py", mode], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running camera_scan.py")

def load_gui(method):  # 'method' parameter is for determining the mode of operation (camera or PDF), so we can use the proper image
    # Creates the main window
    root = customtkinter.CTk()
    root.title("Braille Interpreter")
    root.geometry("1400x700")  # Set the window size
    
    # Right Frame: Displays the recognized lines
    right_frame = customtkinter.CTkFrame(root, width=475, height=200, fg_color="white", border_color="lightblue", border_width=4)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Adds a header label above the text widget
    textHeader_label = customtkinter.CTkLabel(right_frame, text="Scanned Text:", font=("Trebuchet MS", 20))
    textHeader_label.pack(side="top", pady=3) 

    # Adds a container frame for the text widget and scrollbar
    text_container = customtkinter.CTkFrame(right_frame, fg_color="white")
    text_container.pack(expand=True, fill="both", padx=10, pady=5)

    # Adds a scrollable text widget to display recognized lines
    text_widget = Text(text_container, wrap="word", yscrollcommand=lambda *args: text_scrollbar.set(*args), font=("Trebuchet MS", 12))
    text_widget.pack(side="left", expand=True, fill="both")
    text_widget.tag_configure("center", justify="center") # Centers the text
    
    # Adds the scrollbar to the container frame
    text_scrollbar = Scrollbar(text_container, command=text_widget.yview)
    text_scrollbar.pack(side="right", fill="y")

    # Loads the recognized_lines.txt content for the bottom frame
    try:
        with open("recognized_lines.txt", "r") as file:
            scannedText = file.read()
    except FileNotFoundError:
        scannedText = "Scanned text not found."

    # Inserts the text while the widget can be edited
    text_widget.config(state="normal")
    text_widget.insert("1.0", scannedText, "center")
    text_widget.config(state="disabled")  # Make the widget read-only

    scannedText = scannedText.replace("\n", " ")

    # Bottom Frame 1: Button to use a new document
    button_frame = customtkinter.CTkFrame(root, height=100, fg_color="white", border_color="lightblue", border_width=4)
    button_frame.pack(side="bottom", fill="x")

    # Adds the button to use a new document
    newDoc_button = customtkinter.CTkButton(button_frame, text="Scan New Document", font=("Trebuchet MS", 16), command=lambda: scan_new_document())
    newDoc_button.pack(side="left", pady=10, padx=10)

    preexistingDoc_button = customtkinter.CTkButton(button_frame, text="Use PDF Ex. 1", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("pdf1"))
    preexistingDoc_button.pack(side="left", pady=10)

    # Function to handle the button click
    def scan_new_document():
        run_camera_scan("camera")  # Run camera_scan.py with the camera mode
        root.destroy()  # Close the current window
        load_gui("camera")  # Reload the GUI to update the displayed text

    def use_preexisting_document(pdf):
        run_camera_scan(pdf)  # Runs camera_scan.py with the specified PDF
        root.destroy()
        load_gui("pdf1")
        
    # Bottom Frame 2: Displays eleven characters at a time
    bottom_frame = customtkinter.CTkFrame(root, height=400, fg_color="white", border_color="lightblue", border_width=4)
    bottom_frame.pack(side="bottom", fill="x")

    displayHeader_label = customtkinter.CTkLabel(bottom_frame, text="Displayed Characters:", font=("Trebuchet MS", 20))
    displayHeader_label.pack(pady=3)

    char_label = customtkinter.CTkLabel(bottom_frame, text="", font=("Trebuchet MS", 32))
    char_label.pack(pady=4)

    braille_label = customtkinter.CTkLabel(bottom_frame, text="", font=("Arial", 32))
    braille_label.pack(pady=4)

    # Left Frame: Displays the image
    left_frame = customtkinter.CTkFrame(root, width=475, height=600, fg_color="white", border_color="lightblue", border_width=4)
    left_frame.pack(side="left", fill="x", expand=True)
    left_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Creates a container frame for the image and its header
    image_container = customtkinter.CTkFrame(left_frame, fg_color="white", width=450, height=550)  # Adjust size to fit within the left frame
    image_container.pack(side="top", padx=10, pady=0, expand=True)  # Add padding to prevent overflow
    
    # Adds the image header label
    imageHeader_label = customtkinter.CTkLabel(image_container, text="Captured Image:", font=("Trebuchet MS", 20))
    imageHeader_label.pack(side="top", pady=5)  # Add padding below the label

    # Loads and displays the image
    if method == "camera":
        try:
            img = Image.open("cameraScan.png")
            img_tk = ImageTk.PhotoImage(img)
            img_label = customtkinter.CTkLabel(image_container, image=img_tk, text="")
            img_label.pack(side="top", pady=5)
        except FileNotFoundError:
            error_label = customtkinter.CTkLabel(image_container, text="Camera image not found.", font=("Trebuchet MS", 16))
            error_label.pack(side="top", pady=5)
    elif method == "pdf1":
        try:
            img = Image.open("testPDF.png")
            frame_width, frame_height = 450, 550  # Dimensions of the frame
            img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = customtkinter.CTkLabel(image_container, image=img_tk, text="")
            img_label.pack(side="top", pady=5)
        except FileNotFoundError:
            error_label = customtkinter.CTkLabel(image_container, text="PDF not found.", font=("Trebuchet MS", 16))
            error_label.pack(side="top", pady=5)

    brailleCharacters = {"a":"⠁", "b":"⠃", "c":"⠉", "d":"⠙", "e":"⠑", "f":"⠋", "g":"⠛", "h":"⠓",
                        "i":"⠊", "j":"⠚", "k":"⠅", "l":"⠇", "m":"⠍", "n":"⠝", "o":"⠕", "p":"⠏",
                        "q":"⠟", "r":"⠗", "s":"⠎", "t":"⠞", "u":"⠥", "v":"⠧", "w":"⠺", "x":"⠭",
                        "y":"⠽", "z":"⠵"}
    brailleNumbers = {"#":"⠼", "0":"⠴", "1":"⠁", "2":"⠃", "3":"⠉", "4":"⠙", "5":"⠑", "6":"⠋",
                        "7":"⠛", "8":"⠓", "9":"⠊"}

    def brailleTranslate(message):
        nonlocal brailleCharacters, brailleNumbers
        message = message.lower()
        braille = ""
        for char in message:
            if char in brailleCharacters:
                braille += brailleCharacters[char]
            elif char in brailleNumbers:
                braille += brailleNumbers[char]
            else:
                braille += " "
        return braille

    def boldenTextForward(length):
        text_widget.tag_remove("bold", "1.0", "end")  # Unbold any bold text
        if length > 0:
            try:
                # Finds the start and end indices of the text to bolden with current_index and length
                start_index = f"1.0 + {current_index - length} chars"
                end_index = f"1.0 + {current_index} chars"
                text_widget.tag_add("bold", start_index, end_index)  # Adds the bold tag
                text_widget.tag_configure("bold", font=("Trebuchet MS", 12, "bold"))
            except Exception:
                print(f"Error boldening text")

    def boldenTextBackward(length):
        text_widget.tag_remove("bold", "1.0", "end")
        if length > 0:
            try:
                # Finds the start and end indices of the text to bolden
                start_index = f"1.0 + {current_index - length} chars"
                end_index = f"1.0 + {current_index} chars"
                text_widget.tag_add("bold", start_index, end_index)  # Adds the bold tag
                text_widget.tag_configure("bold", font=("Trebuchet MS", 12, "bold"))
            except Exception:
                print(f"Error boldening text")

    # Function to send a string to the Arduino
    if USING_ARDUINO:
        def sendWord(word):
            global arduino
            arduino.write(word.encode())  # Sends the word to the Arduino
            time.sleep(0.1)

    current_index = 0
    
    # Function to update the character label with eleven characters at a time
    def update_char_label(event=None):
        global carry_over, word_archive, is_processing
        nonlocal scannedText, current_index

        if is_processing:  # If already processing, ignores the event
            return
        
        is_processing = True  # Sets the flag to indicate processing has started

        if current_index >= len(scannedText):  # If we've reached the end of the text
            char_label.configure(text="End of Text")
            braille_label.configure(text=brailleTranslate("End of Text"))
            is_processing = False
            return

        # Initializes an empty string to hold the next characters
        next_chars = carry_over
        carry_over = ""  # Resets carry_over for the next iteration

        # Iterates through the text starting from the current index
        while current_index < len(scannedText):
            char = scannedText[current_index]
            current_index += 1  # Increment current_index here to avoid infinite loop

            # Checks if the character is a number. In braille, numbers are preceded by a #.
            # If the character is a number and the last character in next_chars is not a #, prefix it with a #
            if char in brailleNumbers:
                if len(next_chars) > 0:
                    if next_chars[-1] in brailleNumbers:
                        pass
                    else:
                        char = "#" + char
                else:
                    char = "#" + char

            # Stops if the length reaches 10 characters
            if len(next_chars) >= 10:
                carry_over += char  # Save the leftover character for the next press
                break

            # Adds the character to the current string
            next_chars += char

            # Stops if a space or newline is encountered
            if char == " ":
                break

        # Updates the label with the collected characters
        char_label.configure(text=next_chars)
        braille_label.configure(text=brailleTranslate(next_chars))  # Updates the braille label
        if USING_ARDUINO:
            sendWord(next_chars)  # Sends the string to the Arduino
        boldenTextForward(len(next_chars))  # Bolds the text in the text widget
        word_archive.append(next_chars)  # Adds the current string to the word archive
        is_processing = False  # Resets the flag to indicate processing has finished
    
    def revert_char_label(event=None):
        global carry_over
        global word_archive
        nonlocal scannedText, current_index
        # Checks if there are any words in the archive to revert to
        if not word_archive:
            char_label.configure(text="No History")
            braille_label.configure(text=brailleTranslate("No History"))
            return 
        # Deletes the last entry from word_archive
        last_string = word_archive.pop()
        # Decrements current_index by the length of the last string
        current_index -= len(last_string)
        current_index = max(0, current_index)
        # Updates the label with the previous string if available
        try:
            char_label.configure(text=word_archive[-1])  # Display the previous string
            braille_label.configure(text=brailleTranslate(word_archive[-1]))
            boldenTextBackward(len(word_archive[-1]))  # Bold the text in the text widget
            if USING_ARDUINO:
                sendWord(word_archive[-1])
        except IndexError:
            char_label.configure(text="No History")
            braille_label.configure(text=brailleTranslate("No History"))
            if USING_ARDUINO:
                sendWord("No History")
            
    update_char_label()  # Displays the first eleven characters initially

    # Binds LMB to update the label, and RMB to revert
    root.bind("<Button-1>", update_char_label)
    root.bind("<Button-3>", revert_char_label) 

    # Binds mouse wheel scrolling
    root.bind("<MouseWheel>", lambda event: revert_char_label() if event.delta > 0 else update_char_label())

    # Runs the main loop
    root.mainloop()

# Runs the camera scan script to capture the image
run_camera_scan("pdf1")

# Calls the function to load the GUI
load_gui("pdf1")