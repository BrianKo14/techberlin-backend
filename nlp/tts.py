import asyncio

from lmnt.api import Speech


LMNT_API_KEY = "2b4e75c1e1b34aa287a78152394e316e"


def synthesize_speech(text, output_filename='output.wav', lmnt_key=LMNT_API_KEY):
    """
    Function to synthesize speech using the LMNT API and save the audio to a file.

    Parameters:
    - text (str): The text to be converted to speech.
    - output_filename (str): The name of the output file (default is 'output.wav').
    - LMNT_API_KEY (str): The LMNT API key for authentication.
    """
    async def main():
        async with Speech(lmnt_key) as speech:
            # Synthesize the speech
            synthesis = await speech.synthesize(text, voice='lily', format='wav')
            
            # Save the audio data to a file
            with open(output_filename, 'wb') as f:
                f.write(synthesis['audio'])
            
            # List available voices (optional)
            voices = await Speech(LMNT_API_KEY).list_voices()
            print(voices)

    # Run the asynchronous main function
    asyncio.run(main())

