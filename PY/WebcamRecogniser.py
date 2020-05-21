import cv2
import tflite_runtime.interpreter as tflite
import numpy as np

MODEL_PATH = 'models/tr_inception3_lite.mdl'

# get webcam instance
webcam = cv2.VideoCapture(0)

# prepare the model
model = tflite.Interpreter(model_path=MODEL_PATH)
model.allocate_tensors()

# get input details and output details
inputDetails = model.get_input_details()
outputDetails = model.get_output_details()

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

while(True):
    # get the frame
    ret, frame = webcam.read()

    # put the text on the frame
    cv2.putText(frame, message, textStartOffset, font, fontScale, fontColour, lineType)
    cv2.imshow('frame', frame)

    c = cv2.waitKey(1)

    if c == ord('q'):
        break
    elif c == ord('d'):
        inputImage = cv2.resize(frame, (244, 244))
        inputImage = np.asarray(inputImage, dtype='float32')
        inputImage = np.expand_dims(inputImage, axis=0)
        inputImage /= 255.

        model.set_tensor(inputDetails[0]['index'], inputImage)
        model.invoke()

        output = model.get_tensor(outputDetails[0]['index'])
        message = outputLabels[np.argmax(output)]

webcam.release()
cv2.destroyAllWindows()