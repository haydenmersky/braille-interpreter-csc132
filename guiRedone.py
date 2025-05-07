import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter
import serial
import time
import subprocess
import pyttsx3

# Boolean to determine if the program should use serial communication with Arduino
USING_ARDUINO = False

# Initialize the text-to-speech engine
engine = pyttsx3.init()  

# Variable to hold leftover characters; used in the update_char_label function and
#       couldn't find any other way to do it without using a global variable
carry_over = ""  
                 
# List to hold the already loaded words
word_archive = [] 

# Flag to indicate if the program is currently processing a word
is_processing = False 

# Boolean that determines if the mouse wheel is being used to scroll through the text
mouse_wheel = False

if USING_ARDUINO:
    arduino = serial.Serial('COM3', 9600, timeout=1)

# Function to speak the text using pyttsx3
def speak_text(text):
    # Speech rate
    engine.setProperty('rate', 150)
    # Volume
    engine.setProperty('volume', 1)
    # Speaks the text
    engine.say(text)
     # Wait for the speech to finish
    engine.runAndWait() 

# Function to run the camera_scan.py script
def run_camera_scan(mode):
    try:
        subprocess.run(["python", "camera_scan.py", mode], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running camera_scan.py")

# 'method' is for determining the mode of operation (camera or PDF), so we can use the proper image
def load_gui(method):  
    # Creates the main window
    root = customtkinter.CTk()
    root.title("Braille Interpreter")
    root.geometry("1400x700")  
    
    # Right Frame: Displays the recognized lines
    right_frame = customtkinter.CTkFrame(root, width=475, height=200, fg_color="white", border_color="lightblue", border_width=4)
    right_frame.pack(side="right", fill="both", expand=True)
    # Prevents the frame from resizing
    right_frame.pack_propagate(False)  

    # Adds a header label above the text widget
    textHeader_label = customtkinter.CTkLabel(right_frame, text="Scanned Text:", font=("Trebuchet MS", 20))
    textHeader_label.pack(side="top", pady=3) 

    # Adds a container frame for the text widget and scrollbar
    text_container = customtkinter.CTkFrame(right_frame, fg_color="white")
    text_container.pack(expand=True, fill="both", padx=10, pady=5)

    # Adds a scrollable text widget to display recognized lines
    text_widget = Text(text_container, wrap="word", yscrollcommand=lambda *args: text_scrollbar.set(*args), font=("Trebuchet MS", 12))
    text_widget.pack(side="left", expand=True, fill="both")
    # Centers the text
    text_widget.tag_configure("center", justify="center") 
    
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
    # Make the widget read-only
    text_widget.config(state="disabled")  

    scannedText = scannedText.replace("\n", " ")

    # Bottom Frame 1: Buttons to use a new document
    button_frame = customtkinter.CTkFrame(root, height=100, fg_color="white", border_color="lightblue", border_width=4)
    button_frame.pack(side="bottom", fill="x")

    # Adds the buttons to use a new document
    newDoc_button = customtkinter.CTkButton(button_frame, text="Scan New Document", font=("Trebuchet MS", 16), command=lambda: scan_new_document())
    newDoc_button.pack(side="left", pady=10, padx=10)

    preexistingDoc_button1 = customtkinter.CTkButton(button_frame, text="Use PDF Ex. 1", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("testPDF.png"))
    preexistingDoc_button1.pack(side="left", pady=10)

    preexistingDoc_button2 = customtkinter.CTkButton(button_frame, text="Use PDF Ex. 2", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("syllabusPDF.png"))
    preexistingDoc_button2.pack(side="left", pady=10, padx=10)

    # Function to handle the button click
    def scan_new_document():
        # Run camera_scan.py with the camera mode
        run_camera_scan("camera")  
        # Close the current window
        root.destroy()  
        # Reload the GUI to update the displayed text
        load_gui("camera")  

    def use_preexisting_document(pdf):
        # Runs camera_scan.py with the specified PDF
        run_camera_scan(pdf)  
        root.destroy()
        load_gui(pdf)
        
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
    left_frame.pack_propagate(False)

    image_container = customtkinter.CTkFrame(left_frame, fg_color="white", width=450, height=550)
    image_container.pack(side="top", padx=10, pady=0, expand=True)
    
    # Adds the image header label
    if method == "cameraScan.png":
        imageHeader_label = customtkinter.CTkLabel(image_container, text="Captured Image:", font=("Trebuchet MS", 20))
    else:
        imageHeader_label = customtkinter.CTkLabel(image_container, text="Scanned Document:", font=("Trebuchet MS", 20))
    imageHeader_label.pack(side="top", pady=5)

    # Function to load the image into the GUI
    def load_image(image):
        try:
            img = Image.open(image)
            frame_width, frame_height = 450, 550
            # Resizes image while maintaining aspect ratio
            img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)  
            img_tk = ImageTk.PhotoImage(img)
            img_label = customtkinter.CTkLabel(image_container, image=img_tk, text="")
            img_label.pack(side="top", pady=5)
        except FileNotFoundError:
            if method == "cameraScan.png":
                error_label = customtkinter.CTkLabel(image_container, text="Camera image not found.", font=("Trebuchet MS", 16))
                error_label.pack(side="top", pady=5)
            else:
                error_label = customtkinter.CTkLabel(image_container, text="PDF image not found.", font=("Trebuchet MS", 16))
                error_label.pack(side="top", pady=5)

    load_image(method)

    brailleCharacters = {"a":"⠁", "b":"⠃", "c":"⠉", "d":"⠙", "e":"⠑", "f":"⠋", "g":"⠛", "h":"⠓",
                        "i":"⠊", "j":"⠚", "k":"⠅", "l":"⠇", "m":"⠍", "n":"⠝", "o":"⠕", "p":"⠏",
                        "q":"⠟", "r":"⠗", "s":"⠎", "t":"⠞", "u":"⠥", "v":"⠧", "w":"⠺", "x":"⠭",
                        "y":"⠽", "z":"⠵"}

    brailleNumbers = {"#":"⠼", "0":"⠴", "1":"⠁", "2":"⠃", "3":"⠉", "4":"⠙", "5":"⠑", "6":"⠋",
                        "7":"⠛", "8":"⠓", "9":"⠊"}

    # Function to translate the given text to braille
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

    # Function to bolden the text in the text widget that the display label is currently showing
    def boldenTextForward(length):
        # Unbold any bold text
        text_widget.tag_remove("bold", "1.0", "end")  
        if length > 0:
            try:
                # Finds the start and end indices of the text to bolden with current_index and length
                start_index = f"1.0 + {current_index - length} chars"
                end_index = f"1.0 + {current_index} chars"
                # Adds the bold tag
                text_widget.tag_add("bold", start_index, end_index)  
                text_widget.tag_configure("bold", font=("Trebuchet MS", 12, "bold"))
            except Exception:
                print(f"Error boldening text")

    # Same function as above, just in reverse
    def boldenTextBackward(length):
        text_widget.tag_remove("bold", "1.0", "end")
        if length > 0:
            try:
                start_index = f"1.0 + {current_index - length} chars"
                end_index = f"1.0 + {current_index} chars"
                text_widget.tag_add("bold", start_index, end_index)  
                text_widget.tag_configure("bold", font=("Trebuchet MS", 12, "bold"))
            except Exception:
                print(f"Error boldening text")

    # Function to send a string to the Arduino
    if USING_ARDUINO:
        def sendWord(word):
            global arduino
            # Sends the word to the Arduino through the USB port
            arduino.write(word.encode())  
            time.sleep(0.1)

    current_index = 0
    
    # Function to update the character label with eleven characters at a time
    def update_char_label(event=None):
        global carry_over, word_archive, is_processing
        nonlocal scannedText, current_index

        # If already processing, ignores the event
        if is_processing:  
            return
        
        # Sets the flag to indicate processing has started
        is_processing = True  

         # If we've reached the end of the text, display "End of Text"
        if current_index >= len(scannedText): 
            char_label.configure(text="End of Text")
            braille_label.configure(text=brailleTranslate("End of Text"))
            is_processing = False
            return

        # Initializes an empty string to hold the next characters
        # carry_over is used to hold the leftover character from the previous iteration
        next_chars = carry_over 
        # Resets carry_over for the next iteration
        carry_over = ""  

        # Iterates through the text starting from the current index
        while current_index < len(scannedText):
            char = scannedText[current_index]
            current_index += 1

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
                # Save the leftover character for the next press
                carry_over += char  
                break

            # Adds the character to the current string
            next_chars += char

            # Stops if a space or newline is encountered
            if char == " ":
                break

        # Updates the label with the collected characters
        char_label.configure(text=next_chars)
        braille_label.configure(text=brailleTranslate(next_chars))
        if USING_ARDUINO:
            sendWord(next_chars) 
        boldenTextForward(len(next_chars))
        word_archive.append(next_chars)
        # Resets the flag to indicate processing has finished
        is_processing = False  
    
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
            char_label.configure(text=word_archive[-1])
            braille_label.configure(text=brailleTranslate(word_archive[-1]))
            boldenTextBackward(len(word_archive[-1]))
            if USING_ARDUINO:
                sendWord(word_archive[-1])
        except IndexError:
            char_label.configure(text="No History")
            braille_label.configure(text=brailleTranslate("No History"))
            if USING_ARDUINO:
                sendWord("No History")
    
    # Displays the first eleven characters initially
    update_char_label()  

    # Binds LMB to update the label, and RMB to revert
    root.bind("<Button-1>", update_char_label)
    root.bind("<Button-3>", revert_char_label) 

    # Also binds x and z to update and revert respectively just in the case of no mouse
    root.bind("<x>", update_char_label)
    root.bind("<z>", revert_char_label)
    
    # Function to handle mouse wheel control of the label
    # Couldn't figure out how to set this up as a lambda function
    def mouseWheelControl():
        if not mouse_wheel:
            root.bind("<MouseWheel>", lambda event: revert_char_label() if event.delta > 0 else update_char_label())
        else:
            root.unbind("<MouseWheel>")

    # Binds ctrl to toggle for mouse wheel scrolling
    root.bind("<Control_L>", mouseWheelControl)

    # Runs the main loop
    root.mainloop()

# Runs the camera scan script to capture the image
run_camera_scan("testPDF.png")

# Calls the function to load the GUI
load_gui("testPDF.png")