import cv2
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json

# Constant that determines if camera output is grayscale or not.
# Grayscale generally makes OCR more accurate.
GRAYSCALE = True

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
    img = DocumentFile.from_images("cameraScan.png")
    if img is None:
        raise ValueError("No image found to analyze.")
    # Sets result to the image passed through the OCR predictor model
    result = model(img)
    # Prints the result in JSON format for debugging; otherwise unnecessary  
    #result_json = result.export()
    #print(json.dumps(result_json, indent=4))
    # Show the results of the OCR process
    result.show()
    print("Image loaded.")

print("Loading model...")
# Load the OCR predictor model from doctr
model = ocr_predictor(pretrained=True)
print("Model loaded.")
takePhoto()
loadImage()