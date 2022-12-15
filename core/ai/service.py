import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import base64

from .utils import predict_mask

prototxt_path = r"models/face_detect/face_detec.prototxt"
weights_path = r"models/face_detect/model.h5"
face_net = cv2.dnn.readNet(prototxt_path, weights_path)
mask_net = load_model("models/model.h5")

def image_process(image_base64_encode) -> any:
    if (len(image_base64_encode) < 10): return None
    image_base64 = image_base64_encode.split(';base64,').pop()
    image_base64_decode = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_base64_decode, dtype=np.uint8)
    image = cv2.imdecode(image_array, flags=cv2.IMREAD_UNCHANGED)
    if (image.shape[2] == 4):
        B, G, R, A = cv2.split(image)
        alpha = A / 255
        R = (255 * (1 - alpha) + R * alpha).astype(np.uint8)
        G = (255 * (1 - alpha) + G * alpha).astype(np.uint8)
        B = (255 * (1 - alpha) + B * alpha).astype(np.uint8)
        image = cv2.merge((B, G, R))
    cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    frame = image
    (locs, preds) = predict_mask(frame, face_net=face_net, mask_net=mask_net)
    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred
        
        label = ""
        color = (255, 255, 255)
        if mask > withoutMask:
            label = "Wearing Mask"
            color = (139, 247, 149)
        else:
            label = "No Mask"
            color = (73, 92, 255)

        fontpath = "./static/fonts/font.ttf"
        font = ImageFont.truetype(fontpath, 20)
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text((startX, startY-35), label, font = font, fill = color)
        frame = np.array(img_pil)

        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        cv2.rectangle(frame, (startX, endY - 20), (endX, endY), color, cv2.FILLED)
        cv2.putText(
            frame,
            "{:.2f}%".format(max(mask, withoutMask)*100),
            (startX + 6, endY - 6),
            cv2.FONT_HERSHEY_DUPLEX,
            0.5,
            (255, 255, 255),
            2)

    (_, encoded_image) = cv2.imencode('.jpg', frame)
    return base64.b64encode(bytearray(encoded_image)) 