import pickle
import numpy as np
from src.features.feature_extractor import JPEG

classifier = pickle.load(open("models/xgb.pkl", "rb"))

image = JPEG("tests/benign.jpg")
feature = image.decode()

feature = np.reshape(feature, (1, -1))


pred = classifier.predict(feature)

if pred == 1:
    print("This image is malicious!")
else:
    print("This is image is safe!")
