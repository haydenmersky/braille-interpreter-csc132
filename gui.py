import tkinter
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk
import customtkinter
import serial
import time
import subprocess
import pyttsx3
import threading

# Boolean to determine if the program should use serial communication with Arduino
USING_ARDUINO = True

# Initialize the text-to-speech engine
engine = pyttsx3.init()  

# Variable to hold leftover characters; used in the update_char_label function and
#       couldn't find any other way to do it without using a global variable
carry_over = ""  
                 
# List to hold the already loaded words
word_archive = [] 

# Flag to indicate if the program is currently processing a word
is_processing = False 

# Similar as above, flag for if the TTS voice is already talking
is_talking = False

# Boolean that determines if the mouse wheel is being used to scroll through the text
mouse_wheel = False

# Boolean for later to allow for a double press system for the space bar function
# The first time won't do anything, but the second time will trigger the space bar function
firstSpace = True

# Looks for the Arduino and if it can't find it, it will just move on as if it isn't connected
# (Because it isn't)
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    print("Arduino connected.")
    USING_ARDUINO = True
except serial.SerialException:
    print("Arduino not found.")
    USING_ARDUINO = False

# Function to speak the text using pyttsx3
def speak_text(text):
    def run_speech():
        # Sets the speech rate
        engine.setProperty('rate', 150)
        # Sets th volume
        engine.setProperty('volume', 1)
        # Speaks the text
        engine.say(text)
        # runAndWait() is literally the only reason we're using threading
        # Doesn't work without it, but if you have it then the entire program
        #     stops until the speech is done
        engine.runAndWait() 
    # Starts the speech in a new thread
    threading.Thread(target=run_speech).start()

# Function to run the camera_scan.py script
def run_camera_scan(mode):
    try:
        subprocess.run(["python", "camera_scan.py", mode], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running camera_scan.py")

# Function for the TTS welcome message
def welcomeMessage(event=None):
    global is_talking
    if is_talking:
        return
    is_talking = True
    speak_text("Welcome! Use the left and right mouse buttons to move forward or backward through the text respectively. Press space twice to scan a new document. Press the mouse wheel to repeat this message.")
    is_talking = False

# 'method' is for determining the mode of operation (camera or PDF), so we can use the proper image
def load_gui(method, firstTime):  
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
    newDoc_button.pack(side="left", pady=10, padx=23)

    preexistingDoc_button1 = customtkinter.CTkButton(button_frame, text="Use PDF Ex. 1", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("northernlightsPDF.png.png"))
    # Excluding padx so I only have to worry about two buttons' numbers instead of four
    preexistingDoc_button1.pack(side="left", pady=10)

    preexistingDoc_button3 = customtkinter.CTkButton(button_frame, text="Use Ideal Scan", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("idealScan.png"))
    preexistingDoc_button3.pack(side="right", pady=10, padx=23)

    preexistingDoc_button2 = customtkinter.CTkButton(button_frame, text="Use PDF Ex. 2", font=("Trebuchet MS", 16), command=lambda: use_preexisting_document("syllabusPDF.png"))
    preexistingDoc_button2.pack(side="right", pady=10)

    # Function to handle the button click
    def scan_new_document():
        # Run camera_scan.py with the camera mode
        run_camera_scan("cameraScan.png")  
        # Close the current window
        root.destroy()  
        # Reload the GUI to update the displayed text
        load_gui("cameraScan.png", False)  

    def use_preexisting_document(pdf):
        # Runs camera_scan.py with the specified PDF
        run_camera_scan(pdf)  
        root.destroy()
        load_gui(pdf, False)
        
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

    # Braille characters and numbers dictionary for translation
    brailleCharacters = {"a":"⠁", "b":"⠃", "c":"⠉", "d":"⠙", "e":"⠑", "f":"⠋", "g":"⠛", "h":"⠓",
                        "i":"⠊", "j":"⠚", "k":"⠅", "l":"⠇", "m":"⠍", "n":"⠝", "o":"⠕", "p":"⠏",
                        "q":"⠟", "r":"⠗", "s":"⠎", "t":"⠞", "u":"⠥", "v":"⠧", "w":"⠺", "x":"⠭",
                        "y":"⠽", "z":"⠵"}

    brailleNumbers = {"#":"⠼", "0":"⠴", "1":"⠁", "2":"⠃", "3":"⠉", "4":"⠙", "5":"⠑", "6":"⠋",
                        "7":"⠛", "8":"⠓", "9":"⠊"}

    # Function to translate the given text to braille, builds the braille string character by character
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
    # event=None has to be there for a function to be bound to a key for some reason
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

    # Function to handle the space double press system
    # The first press will do nothing, but the second press will trigger the space bar function
    def spacePress(event=None):
        global firstSpace
        if firstSpace:
            print("First space press detected.")
            root.bind("<space>", spacePress)
        else:
            print("Second space press detected.")
            scan_new_document()
        firstSpace = not firstSpace

    # Function to handle mouse wheel control of the label
    # Couldn't figure out how to set this up as a lambda function, since it's technically two
    def mouseWheelControl(event=None): 
        global mouse_wheel
        if not mouse_wheel:
            root.bind("<MouseWheel>", lambda event: revert_char_label() if event.delta > 0 else update_char_label())
            mouse_wheel = True
            print("Mouse wheel scrolling enabled.")
        else:
            root.unbind("<MouseWheel>")
            mouse_wheel = False
            print("Mouse wheel scrolling disabled.")

    
    # Binds LMB to update the label, and RMB to revert
    root.bind("<Button-1>", update_char_label)
    root.bind("<Button-3>", revert_char_label) 

    # Binds MMB and v to repeat the welcome message
    root.bind("<Button-2>", welcomeMessage)
    root.bind("<v>", welcomeMessage) 

    # Also binds x and z to update and revert respectively just in the case of no mouse
    root.bind("<x>", update_char_label)
    root.bind("<z>", revert_char_label)

    # Binds ctrl to toggle for mouse wheel scrolling
    root.bind("<Control_L>", mouseWheelControl)
    root.bind("<Control_R>", mouseWheelControl)

    # Binds the space bar to the double press system
    root.bind("<space>", spacePress)

    # Doesn't welcome the user if the program is being reloaded
    # Literally the only reason firstTime is a parameter
    if firstTime:
        welcomeMessage()

    # Runs the main loop
    root.mainloop()

# Runs the camera scan script to capture the image
run_camera_scan("testPDF.png")

# Calls the function to load the GUI
load_gui("testPDF.png", True)

# Stops the TTS engine when the program exits
engine.stop()  