import librosa
from scipy import spatial
from scipy.signal import resample
import numpy as np
import cv2

def cosine_similarity(x, y):
     return 1 - spatial.distance.cosine(x, y)

def next_pow_2(x):
    """Smallest next power of two of a given value x."""
    return 1 << (x - 1).bit_length()


def mfccs(path):
    audio_signal, sample_rate = librosa.core.load(path)
    first_five_minutes = sample_rate * 60 * 5

    audio_signal_first_five_minutes = audio_signal[:first_five_minutes]
    number_of_audio_samples = len(audio_signal_first_five_minutes)
    audio_duration = float(
        number_of_audio_samples / float(sample_rate))

    audio_frame_size = next_pow_2(int(sample_rate / 4.0))  # i.e., about 0.25 seconds.
    audio_hop_size = int(audio_frame_size / 2.0)  # i.e., 50% overlap.

    mfccs_matrix = librosa.feature.mfcc(
        audio_signal_first_five_minutes, n_fft=audio_frame_size, hop_length=audio_hop_size)


    number_of_seconds = int(np.round(audio_duration))
    return np.array(resample(mfccs_matrix.transpose(), number_of_seconds))

ep1 = mfccs("videos/House.Of.Cards.S01E03.720p.BluRay.x265.mp4")
ep2 = mfccs("videos/House.Of.Cards.S01E04.720p.BluRay.x265.mp4")

scaledep1 = cv2.resize(ep1, (7200, 7200), interpolation=cv2.INTER_CUBIC)
scaledep2 = cv2.resize(ep2, (7200, 7200), interpolation=cv2.INTER_CUBIC)


np.save("np/House.Of.Cards.S01E03.720p.BluRay.x265.npy", scaledep1)
np.save("np/House.Of.Cards.S01E04.720p.BluRay.x265.npy", scaledep2)
