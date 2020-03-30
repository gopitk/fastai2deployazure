from datetime import datetime
from fastai2.vision.all import *
from urllib.request import urlopen

import logging
import os
import sys
import fastai2

path = Path()
learn_inf = load_learner(path/'classify/export.pkl')

def predict_image_from_url(image_url):
    with urlopen(image_url) as testImage:
        img = PILImage.create(testImage)
        pred,pred_idx,probs = learn_inf.predict(img)

        response = {
            'created': datetime.utcnow().isoformat(),
            'prediction': pred,
            'confidence': probs[pred_idx.item()].item()
        }
        response
        logging.info(f'returning {response}')
        return response

if __name__ == '__main__':
    print(predict_image_from_url(sys.argv[1]))
