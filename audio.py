import librosa

audio_signal, sample_rate = librosa.core.load("videos/pll1.mp4")
print(audio_signal.shape)