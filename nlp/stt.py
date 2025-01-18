import pyaudio
import wave
import requests
import os
import numpy as np

# Your OpenAI API key
api_key = os.environ["OPENAI_API_KEY"]

# API endpoint for Whisper transcription
url = "https://api.openai.com/v1/audio/transcriptions"

# Set the parameters for recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit resolution)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)
CHUNK = 1024  # Size of each audio chunk (buffer size)
SILENCE_THRESHOLD = 1000  # Threshold below which audio is considered silent
SILENCE_LIMIT = 2  # Number of consecutive silent chunks before stopping
OUTPUT_FILENAME = "recorded_audio.wav"  # Output file name

def record_and_transcribe():
    """
    Records audio from the microphone, saves it as a .wav file,
    and sends it to the OpenAI Whisper API for transcription.
    """
    # Initialize the audio recorder
    p = pyaudio.PyAudio()

    # Start recording
    print("Recording...")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0

    while True:
        # Read a chunk of data from the microphone
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert the data to numpy array for analysis
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Calculate the RMS (Root Mean Square) of the audio data to detect volume
        rms = np.sqrt(np.mean(audio_data**2))

        if rms < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # Stop recording if silence has lasted for the specified limit
        if silent_chunks >= SILENCE_LIMIT:
            print("Silence detected, stopping recording...")
            break

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a .wav file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {OUTPUT_FILENAME}")

    # Prepare the headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Prepare the file for upload and specify the model
    files = {
        "file": open(OUTPUT_FILENAME, "rb"),
    }

    # Adding the model parameter explicitly
    data = {
        "model": "whisper-1"  # Specify the Whisper model
    }

    # Make the POST request to the Whisper API
    print("Transcribing audio...")
    response = requests.post(url, headers=headers, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the transcription result
        transcription = response.json()
        print("Transcription result:", transcription["text"])
        return transcription["text"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example of calling the function
if __name__ == "__main__":
    transcription = record_and_transcribe()
    if transcription:
        print("Successfully transcribed:", transcription)
    else:
        print("Transcription failed.")