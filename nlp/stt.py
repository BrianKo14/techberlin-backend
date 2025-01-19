import pyaudio
import wave
import requests
import os

# Your OpenAI API key
api_key = os.environ["OPENAI_API_KEY"]

# API endpoint for Whisper transcription
url = "https://api.openai.com/v1/audio/transcriptions"

# Set the parameters for recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit resolution)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)
CHUNK = 1024  # Size of each audio chunk (buffer size)
TIME_LIMIT = 5  # Time limit for the recording in seconds
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

    # Record audio for the specified time limit
    for _ in range(0, int(RATE / CHUNK * TIME_LIMIT)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    print("Recording finished.")
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
    

def transcribe_audio(input_audio):
    """
    Records audio from the microphone, saves it as a .wav file,
    and sends it to the OpenAI Whisper API for transcription.
    """

    # Prepare the headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Prepare the file for upload and specify the model
    files = {
        "file": open(input_audio, "rb"),
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
