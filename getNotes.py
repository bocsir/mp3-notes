import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa.display
from pydub import AudioSegment
AudioSegment.ffmpeg = "C:/ffmpeg"

def getNotes(path):
    #mp3 -> wav
    audio = AudioSegment.from_file(path)
    audio.export("raw.wav", format="wav")

    # Load the audio file. y = time series, sr = sample rate
    y, sr = librosa.load('raw.wav', sr=22050);

    # Only want harmonic portion of audio
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Pitch estimation:
    # fmin for low D whistle is D4, fmax for high D whistle is B6
    f0, voiced_flag, voiced_probs = librosa.pyin(y_harmonic, fmin=librosa.note_to_hz('D4'), fmax=librosa.note_to_hz('B6'))
    # f0 = array of estimated frequencies
    # voiced_flag = array of booleans indicating whether each frame has detectable pitch (voiced)
    # voiced_probs = array of probabilities of each frame being voiced (0 to 1)

    # Convert Hz to note
    def hz_to_note_with_threshold(frequency, voiced_prob, threshold=.9):
        # Get frequency if high likelyhood of valid pitch
        if frequency > 0 and voiced_prob > threshold:
            return librosa.hz_to_note(frequency)
        return "N/A"

    # Create list of notes
    notes = [hz_to_note_with_threshold(freq, prob) for freq, prob in zip(f0, voiced_probs)]

    # Convert to Pandas Series for easier processing
    notes_series = pd.Series(notes)

    # Remove consecutive duplicates and filter out "N/A"
    notes_series = notes_series[notes_series.shift() != notes_series]
    notes_series = notes_series[notes_series != "N/A"]

    # return notes array
    return(notes_series.tolist())

    # fig, ax = plt.subplots(2, 1, figsize=(14, 10))

    # # Plot the estimated pitch over time
    # times = librosa.times_like(f0)
    # ax[0].plot(times, f0, label='Estimated pitch', color='r')
    # ax[0].set_xlabel('Time (s)')
    # ax[0].set_ylabel('Frequency (Hz)')
    # ax[0].set_title('Estimated pitch over time')
    # ax[0].legend()

    # # Compute STFT array
    # D = np.abs(librosa.stft(y))
    # # Plot the spectrogram
    # img = librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, x_axis='time', y_axis='log', ax=ax[1])
    # fig.colorbar(img, ax=ax[1], format='%+2.0f dB')
    # ax[1].set_title('Spectrogram (dB)')

    # # Display the plots
    # plt.tight_layout()
    # plt.show()