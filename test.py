import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from pydub import AudioSegment
AudioSegment.ffmpeg = "C:/ffmpeg"

#mp3 -> wav
audio = AudioSegment.from_file('test2.mp3')
audio.export("test.wav", format="wav")

# Load the audio file. y = time series, sr = sample rate
y, sr = librosa.load('test.wav', sr=22050);
# Compute the STFT
D = np.abs(librosa.stft(y))
# Get array of frequencies
freq = librosa.fft_frequencies(sr=sr)
print(freq)
# Plot the spectrogram
# plt.figure(figsize=(10, 6))
# librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, x_axis='time', y_axis='log')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Spectrogram (dB)')
# plt.show()

#extract notes
def hz_to_note(frequency):
    if frequency > 0:
        return librosa.hz_to_note(frequency)
    return "N/A"
notes = []

magnitude_threshold = 0.1
window_size = 5

for idx, magnitude in enumerate(D):
    notes = []
    num_frames = D.shape[1]
    for idx in range(0, num_frames, window_size):
        window_magnitudes = D[:, idx:idx+window_size]
        avg_magnitude = np.mean(window_magnitudes, axis=1)
        if avg_magnitude.any():
            max_idx = np.argmax(avg_magnitude)
            if avg_magnitude[max_idx] > magnitude_threshold:
                frequency = freq[max_idx]
                note = hz_to_note(frequency)
                if len(notes) == 0 or notes[-1] != note:  # Avoid repeating notes
                    notes.append(note)

print(notes)