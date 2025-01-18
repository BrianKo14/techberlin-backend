
from agents import dialogue_generation, question_answering
import json

USERS_REF_PATH = "./data/users-reference.json"

def get_matches():
	""" Returns an object with the user's matches. """

	with open(USERS_REF_PATH, 'r') as f:
		users = json.load(f)

	for user in users["users"]:
		if user["id"] != 0:
			dialogue = dialogue_generation.generate_dialogue(0, user["id"])
			evaluation = dialogue_generation.evaluate_dialogue(dialogue)

			user["dialogue"] = dialogue
			user["evaluation"] = evaluation

	return users["users"]


def ask_question(dialogue_history, question, user_id):
	""" Receives a question and returns the answer. """

	answer = question_answering.ask(dialogue_history, question, user_id)

	return { 'answer': answer }
