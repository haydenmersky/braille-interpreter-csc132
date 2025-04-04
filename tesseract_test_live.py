import cv2
import pytesseract
from pytesseract import Output
 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

freeze_frame = False

while True:
    # Capture frame-by-frame, unless 'f' is pressed
    if not freeze_frame:
        ret, frame = cap.read()
 
    d = pytesseract.image_to_data(frame, output_type=Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # don't show empty text
            if text and text.strip() != "":
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
 
    # Display the resulting frame
    cv2.imshow('frame', frame)

    keyPressed = cv2.waitKey(1) & 0xFF
    
    if keyPressed == ord('q'):
        break
    elif keyPressed == ord('f'):
        freeze_frame = not freeze_frame
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()