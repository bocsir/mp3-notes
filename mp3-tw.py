import librosa
import numpy as np
from pydub import AudioSegment
AudioSegment.ffmpeg = "C:/ffmpeg"

def convert_mp3_to_wav(mp3_file, wav_path):
    audio = AudioSegment.from_file(mp3_file)
    audio.export(wav_path, format="wav")

def extract_freq(wav_path):
    y, sr = librosa.load(wav_path) #'load as floating point time series'. y = time series, sr = sample rate
    D = np.abs(librosa.stft(y)) #short-time fourier transform outputting D[freq, time]
    freq = librosa.fft_frequencies(sr=sr)
    return freq, D
    
def extract_notes(freq, D):
    notes = []
    for idx, magnitude in enumerate(D):
        if magnitude.any():
            max_idx = np.argmax(magnitude)
            freq = freq[max_idx]
            note = librosa.hz_to_note(freq)
            notes.append(note)
    return notes

def save_notes_to_file(notes, output_file):
    with open(output_file, 'w') as f:
        for note in notes:
            f.write(f"{note}\n")

def main(mp3_path, output_file):
    wav_path = "temp.wav"
    convert_mp3_to_wav(mp3_path, wav_path)
    frequencies, D = extract_freq(wav_path)
    notes = extract_notes(frequencies, D)
    save_notes_to_file(notes, output_file)

# if __name__ == "__main__":
#     mp3_path = "input.mp3"
#     output_file = "output_notes.txt"

main('test.mp3', 'output_file.txt')