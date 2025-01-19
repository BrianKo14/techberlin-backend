
# NOTE: The question-answering module is designed to search into agent profiles to provide further information about your potential match.

import sys
sys.path.append('..')

import mistral_service
from agents import data_retrieval



def ask(dialogue, question, user_id):

	me_user = data_retrieval.get_user_data(0)

	them_user = data_retrieval.get_user_data(user_id)
	them_agent = data_retrieval.get_agent(user_id)

	prompt = f"""
	Here is a chat history between two people, {me_user["name"]} and {them_user["name"]}:

	<begin dialogue>
	{dialogue}
	<end dialogue>

	Here is {them_user["name"]}'s personality profile:

	{them_agent}

	{me_user["name"]} asks: "{question}"

	Answer the question as {them_user["name"]} would.
	"""

	return mistral_service.ask_mistral(prompt)