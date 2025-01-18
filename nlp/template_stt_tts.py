
import sys
sys.path.append('..')

from interview import interview_generation
from nlp import stt, tts


FIRST_QUESTION = "Hi there! I’m here to help set up your dating profile. Can I ask you a few questions?"


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

    for _ in range(2):
        context_dialogue = continue_interview(context_dialogue)
        

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


# start_interview()

context_dialogue = {
        "dialogue": [{
                "speaker": "AI",
                "text": FIRST_QUESTION
            },
            {
                "speaker": "User",
                "text": "Yes, sure."
            }]
    }

continue_interview(context_dialogue)

    
    