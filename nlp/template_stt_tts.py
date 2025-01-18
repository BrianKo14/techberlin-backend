import stt, tts

def start(name="Max"):
    promt = f"Hello, {name}. I need some information about yourself to find your perfect match. So let's get started. How old are you?"
    tts.synthesize_speech(promt)
    stt.record_and_transcribe("openAI-Key")
    