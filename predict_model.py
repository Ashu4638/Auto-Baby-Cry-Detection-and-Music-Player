
import librosa
import numpy as np
import pickle
import sounddevice as sd
from scipy.io.wavfile import write
import noisereduce as nr
# load data
from scipy.io import wavfile
from shutil import move




def predict():
    file = open("C:/Users/ashu_/PycharmProjects/Baby_Cry_Detection/AudioModel.pkl", "rb")
    Model = pickle.load(file)

    # Sampling frequency
    frequency = 44100

    # Recording duration in seconds
    duration = 6

    # to record audio from
    # sound-device into a Numpy
    recording = sd.rec(int(duration * frequency),
                       samplerate=frequency, channels=1)

    # Wait for the audio to complete
    sd.wait()

    # using scipy to save the recording in .wav format
    # This will convert the NumPy array
    # to an audio file with the given sampling frequency
    write("recording0.wav", rate=frequency, data=recording)
    rate, data = wavfile.read("recording0.wav")

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)

    wavfile.write("New.wav", rate=rate, data=reduced_noise)


    filename = "New.wav"
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')

    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)


    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

    predicted_label = Model.predict(mfccs_scaled_features)


    return predicted_label, filename