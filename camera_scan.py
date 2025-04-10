import cv2
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json

# Constant that determines if camera output is grayscale or not.
# Grayscale generally makes OCR more accurate.
GRAYSCALE = True

# Global variable that determines which image to use for OCR
chosenImage = "cameraScan.png"

# Prompt user for input to choose image source
if input("Use pre-existing scan or camera? (p/c) ") == 'p':
    chosenImage = "testPDF.png"
else:
    chosenImage = "cameraScan.png"

def takePhoto():
    print("Starting capture...")
    # Capture from the default camera (0)
    cap = cv2.VideoCapture(0)
    # ret acts as a boolean to check if the frame was captured correctly
    # frame is the actual image captured from the camera
    ret, frame = cap.read()
    if GRAYSCALE:
        # Convert the frame to grayscale if GRAYSCALE is set to True
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Saves the frame to a file named 'cameraScan.png'
    cv2.imwrite('cameraScan.png', frame)
    print("Capture complete.")
    # Release the capture to free up the camera for other processes
    cap.release()

def loadImage():
    print("Loading image...")
    # Load the image using DocumentFile from doctr.io
    img = DocumentFile.from_images(chosenImage)
    if img is None:
        raise ValueError("No image found to analyze.")
    
    # Sets result to the image passed through the OCR predictor model
    result = model(img)

    # Prints the result in JSON format for debugging; otherwise unnecessary  
    result_json = result.export()
    #print(json.dumps(result_json, indent=4))

    # Extract the recognized words
    lines = []
    for page in result_json['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                line_text = []
                for word in line['words']:
                    if word != '-':
                        line_text.append(word['value'])  # Extract the word text
                lines.append(" ".join(line_text))
    
    # Print the extracted words
    print("Recognized Lines:")
    for i, line in enumerate(lines, 1):
        print(f"Line {i}: {line}")
    
    # Optionally, save the words to a file
    with open("recognized_lines.txt", "w") as f:
        f.write("\n".join(lines))
    
    print("Lines saved to recognized_words.txt")
    # Show the results of the OCR process
    result.show()
    print("Image loaded.")

print("Loading model...")
# Load the OCR predictor model from doctr
model = ocr_predictor(pretrained=True)
print("Model loaded.")
takePhoto()
loadImage()