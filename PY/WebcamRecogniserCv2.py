import cv2

# yolo v3 tiny model uses 13 x 13 feature maps
WEIGHT_PATH = 'models/yolov3-tiny/yolov3-tiny.weights'
CONFIG_PATH = 'models/yolov3-tiny/yolov3-tiny.cfg'
THRESHOLD = 0.5

# get the model
model = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHT_PATH)

# get webcam instance
webcam = cv2.VideoCapture(0)

# font preparation
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
textStartOffset = (10, 30)
fontScale = 0.5
fontColour = (0,255,0)
lineType = 1

# message var
message = 'NONE'

# output labels
outputLabels = {0: 'cardboard', 1: 'glass', 2: 'metal', 3: 'paper', 4: 'plastic', 5: 'trash'}

while True:
    # get the frame
    ret, frame = webcam.read()

    # put the text on the frame
    cv2.putText(frame, message, textStartOffset, font, fontScale, fontColour, lineType)
    cv2.imshow('frame', frame)

    # listen to the key
    c = cv2.waitKey(1)

    if c == ord('q'):
        break
    elif c == ord('d'):
        model.setInput(cv2.dnn.blobFromImage(frame, size=(416, 416), swapRB=True))
        output = model.forward()

        print(len(output))

webcam.release()
cv2.destroyAllWindows()