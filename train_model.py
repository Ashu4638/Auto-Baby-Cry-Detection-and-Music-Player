
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

import pandas as pd
import os
import librosa
import numpy as np

import pickle

def features_extractor(file):
    audio, sample_rate = librosa.load(file)
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)

    return mfccs_scaled_features

def train_model():
    extracted_features = []

    cry_dir = "C:/Users/ashu_/PycharmProjects/Baby_Cry_Detection/Crying baby/"

    for file in os.scandir(cry_dir):
        final_class_label = 1
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    silence_dir = "C:/Users/ashu_/PycharmProjects/Baby_Cry_Detection/Silence/"
    for file in os.scandir(silence_dir):
        final_class_label = 0
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    extracted_features_df = pd.DataFrame(extracted_features, columns=['feature', 'class'])
    X = np.array(extracted_features_df['feature'].tolist())
    Y = np.array(extracted_features_df['class'].tolist())
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    model = KNeighborsClassifier()

    model.fit(X_train, y_train)
    file = open("AudioModel.pkl", "wb")
    pickle.dump(model, file)
    print("Success")