
import sys
sys.path.append('..')

from interview import interview_generation
from agents import transcript_digest
from nlp import stt, tts
import os


FIRST_QUESTION = "Hi there! I’m here to help set up your dating profile. Can I ask you a few questions?"
TRANSCRIPTS_PATH = "../data/user_transcripts/"
NUMBER_OF_QUESTIONS = 5


def start_interview():

    context_dialogue = {
        "dialogue": [{
                "speaker": "AI",
                "text": FIRST_QUESTION
            }]
    }

    user_reply = get_user_reply(FIRST_QUESTION)
    context_dialogue["dialogue"].append({
        "speaker": "User",
        "text": user_reply
    })

    for _ in range(NUMBER_OF_QUESTIONS):
        context_dialogue = continue_interview(context_dialogue)

    save_transcript(context_dialogue)


def continue_interview(context_dialogue):

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