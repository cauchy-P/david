import os
import datetime
import pyaudio
import wave
import speech_recognition as sr
import csv
from pathlib import Path
import sys
import contextlib
import sounddevice
# Ensure the records directory exists
RECORDS_DIR = 'records'
if not os.path.exists(RECORDS_DIR):
    os.makedirs(RECORDS_DIR)

def record_audio(duration=5):
    """Record audio from the system microphone and save it to a WAV file."""
    # Audio recording parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Suppress ALSA warnings during PyAudio initialization
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stderr(devnull):
            audio = pyaudio.PyAudio()
    
    # Try to open the default input device
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                           rate=RATE, input=True,
                           frames_per_buffer=CHUNK,
                           input_device_index=None)  # Use default device
    except OSError as e:
        print(f"Error opening audio device: {e}")
        print("Please ensure a microphone is connected and PulseAudio is running.")
        audio.terminate()
        return None
    
    print("Recording...")
    frames = []
    
    # Record for the specified duration
    try:
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except OSError as e:
        print(f"Error during recording: {e}")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        return None
    
    print("Recording finished.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Generate filename based on current date and time
    current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f'{RECORDS_DIR}/{current_time}.wav'
    
    # Save the recorded audio to a WAV file
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
    except Exception as e:
        print(f"Error saving audio file: {e}")
        return None
    
    return filename

def list_recordings_by_date(start_date, end_date):
    """List recording files within a specific date range (Bonus Task for Problem 1)."""
    try:
        start = datetime.datetime.strptime(start_date, '%Y%m%d')
        end = datetime.datetime.strptime(end_date, '%Y%m%d')
        recordings = []
        
        for file in os.listdir(RECORDS_DIR):
            if file.endswith('.wav'):
                file_date_str = file.split('-')[0]
                try:
                    file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
                    if start <= file_date <= end:
                        recordings.append(file)
                except ValueError:
                    continue
        
        return recordings
    except ValueError:
        print("Invalid date format. Use YYYYMMDD.")
        return []

def speech_to_text(audio_file):
    """Convert audio file to text using STT and save to CSV."""
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        # Use Google Speech Recognition for STT
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: {text}")
        
        # Generate CSV filename (same as audio file but with .csv extension)
        csv_filename = f"{RECORDS_DIR}/{Path(audio_file).stem}.csv"
        
        # Save to CSV (time, text)
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Text'])
            # Use file creation time as a placeholder
            file_time = datetime.datetime.fromtimestamp(os.path.getctime(audio_file)).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([file_time, text])
        
        return csv_filename
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"STT service error: {e}")
        return None

def search_keyword_in_csv(keyword):
    """Search for a keyword in all CSV files (Bonus Task for Problem 2)."""
    results = []
    for file in os.listdir(RECORDS_DIR):
        if file.endswith('.csv'):
            with open(f'{RECORDS_DIR}/{file}', 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2 and keyword.lower() in row[1].lower():
                        results.append((file, row[0], row[1]))
    return results

def main():
    """Main function to demonstrate the functionality."""
    # Record audio
    print("Starting audio recording...")
    audio_file = record_audio(duration=5)
    if not audio_file:
        print("Recording failed. Exiting.")
        return
    
    print(f"Audio saved to: {audio_file}")
    
    # Convert audio to text and save to CSV
    print("\nConverting audio to text...")
    csv_file = speech_to_text(audio_file)
    if csv_file:
        print(f"Text saved to: {csv_file}")
    
    # Bonus Task: List recordings in a date range
    print("\nListing recordings between 20250101 and 20251231...")
    recordings = list_recordings_by_date('20250101', '20251231')
    print("Recordings found:", recordings)
    
    # Bonus Task: Search for a keyword in CSV files
    keyword = input("\nEnter a keyword to search in CSV files: ")
    results = search_keyword_in_csv(keyword)
    if results:
        print("Search results:")
        for file, time, text in results:
            print(f"File: {file}, Time: {time}, Text: {text}")
    else:
        print("No matches found.")

if __name__ == '__main__':
    main()