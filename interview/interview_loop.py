
# NOTE: This module implements the workflow for the Wingman call process.
# It provides the backend endpoints for receiving, processing and replying to user voice input.

import sys
sys.path.append('..')

from interview import interview_generation
from agents import transcript_digest
from nlp import stt, tts
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS_PATH = "../data/user_transcripts/"
TRANSCRIPTS_PATH = os.path.join(current_dir, TRANSCRIPTS_PATH)


FIRST_QUESTION = "Hey there! What's up? I'm Wingly, your Wingman. I'm here to get to know you better so I can help you find your perfect match. Ready to get started?"
NUMBER_OF_QUESTIONS = 5

INITIAL_CONTEXT = {
    "dialogue": [{
        "speaker": "AI",
        "text": FIRST_QUESTION
    }]
}


def start_interview():

    tts.synthesize_speech(FIRST_QUESTION)
    return 'output.wav', INITIAL_CONTEXT


def continue_interview(context_dialogue, reply_audio_path):

    # NOTE: Eventually, we would need to design a working dialogue tree to ensure accurate conversation flow.

    # Get reply
    user_reply = stt.transcribe_audio(reply_audio_path)
    context_dialogue["dialogue"].append({
        "speaker": "User",
        "text": user_reply
    })

    # Generate the next question
    next_question = interview_generation.get_next_question(context_dialogue)
    context_dialogue["dialogue"].append({
        "speaker": "AI",
        "text": next_question
    })

    print(f"Next question: {next_question}")

    tts.synthesize_speech(next_question)

    return 'output.wav', context_dialogue


# DEBUG: This runs the interview locally for debugging purposes
def start_interview_local():

    context_dialogue = INITIAL_CONTEXT
    
    user_reply = get_user_reply(FIRST_QUESTION)
    context_dialogue["dialogue"].append({
        "speaker": "User",
        "text": user_reply
    })

    for _ in range(NUMBER_OF_QUESTIONS):
        context_dialogue = continue_interview_local(context_dialogue)

    save_transcript(context_dialogue)


# DEBUG: This runs the interview locally for debugging purposes
def continue_interview_local(context_dialogue):

    # Generate the next question
    next_question = interview_generation.get_next_question(context_dialogue)
    context_dialogue["dialogue"].append({
        "speaker": "AI",
        "text": next_question
    })

    print(f"Next question: {next_question}")

    # Get reply
    user_reply = get_user_reply(next_question)
    context_dialogue["dialogue"].append({
        "speaker": "User",
        "text": user_reply
    })

    return context_dialogue


def get_user_reply(next_question):

    tts.synthesize_speech_and_play(next_question)
    return stt.record_and_transcribe()


def save_transcript(context_dialogue):

    # Generate output

    output = ""
    for turn in context_dialogue["dialogue"]:
        output += f"{turn['speaker']}: {turn['text']}\n"

    transcript_digest.update_agent(output, 0)


    # Save to file

    def get_unique_filename(base_path, base_name, extension):
        counter = 1
        while os.path.exists(f"{base_path}{base_name}{counter}{extension}"):
            counter += 1
        return f"{base_path}{base_name}{counter}{extension}"

    unique_filename = get_unique_filename(TRANSCRIPTS_PATH, "transcript", ".txt")
    with open(unique_filename, "w") as f:
        f.write(output)