import cv2
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json
import sys

# Reads the mode argument from the command line, defaults to the first PDF image if not provided.
mode = sys.argv[1] if len(sys.argv) > 1 else "cameraScan.png"

# Constant that determines if camera output is grayscale or not.
# Grayscale generally makes OCR more accurate.
GRAYSCALE = False

# Global variable that determines which image to use for OCR
chosenImage = mode

def takePhoto():
    print("Starting capture...")
    # Captures from the default camera (0), when properly set up, switch to 1.
    cap = cv2.VideoCapture(1)
    # Sets the resolution (e.g., 1920x1080 for Full HD)
    # Sets the width
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
    # Sets the height 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # ret acts as a boolean to check if the frame was captured correctly
    # frame is the actual image captured from the camera
    ret, frame = cap.read()
    if GRAYSCALE:
        # Convert the frame to grayscale if GRAYSCALE is set to True
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Rotates the image 90 degrees clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # Saves the frame to a file named 'cameraScan.png'
    cv2.imwrite('cameraScan.png', frame)
    print("Capture complete.")
    # Releases the capture to free up the camera for other processes
    cap.release()

def loadImage():
    print("Loading image...")
    # Loads the image using DocumentFile from doctr.io
    img = DocumentFile.from_images(chosenImage)
    if img is None:
        raise ValueError("No image found to analyze.")
    
    # Sets result to the image passed through the OCR predictor model
    result = model(img)

    # Assigns the result in JSON format to a variable 
    result_json = result.export()

    # Extracts the recognized words
    lines = []

    # docTR divides its information into different classes. We need to use the line and word class for extraction.
    for page in result_json['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                line_text = []
                for word in line['words']:
                    if word != '-':
                        # Extracts the text
                        line_text.append(word['value'])  
                lines.append(" ".join(line_text))
    
    # Prints the extracted words
    print("Recognized Lines:")
    for i, line in enumerate(lines, 1):
        print(f"Line {i}: {line}")
    
    # Saves the words to a file
    with open("recognized_lines.txt", "w") as f:
        f.write("\n".join(lines))
    
    print("Lines saved to recognized_words.txt")
    # Shows the results of the OCR process
    print("Image loaded.")

print("Loading model...")
# Loads the OCR predictor model from doctr
model = ocr_predictor(pretrained=True)
print("Model loaded.")
if mode == "cameraScan.png":
    takePhoto()
loadImage()