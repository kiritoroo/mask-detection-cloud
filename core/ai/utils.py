import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import ImageFont, ImageDraw, Image
from typing import Union
import numpy as np
import time
import cv2

def predict_mask(frame, face_net, mask_net) -> Union[list, list]:
    (h, w)= frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        frame,
        1.0,
        (224,224),
        (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    faces=[]
    locs=[]
    preds=[]
    
    for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence>0.5:
            box = detections[0,0,i,3:7]*np.array([w,h,w,h])
            (startX, startY, endX, endY)= box.astype("int")
                
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w-1, endX), min(h-1, endY))
                
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224,224))
            face = img_to_array(face)
            face = preprocess_input(face)
                
            faces.append(face)
            locs.append((startX, startY, endX, endY))
    
    if len(faces)>0:
        faces = np.array(faces, dtype="float32")
        preds = mask_net.predict(faces, batch_size=32)
        
    return (locs, preds)