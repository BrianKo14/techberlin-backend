
import sys
sys.path.append('..')

import mistral_service
from agents import data_retrieval


def generate_dialogue(user1_id, user2_id):

	user1 = data_retrieval.get_user_data(user1_id)
	user2 = data_retrieval.get_user_data(user2_id)

	agent1 = data_retrieval.get_agent(user1_id)
	agent2 = data_retrieval.get_agent(user2_id)

	prompt = f"""
	
	Here is a description of {user1["name"]}:
	{agent1}

	Here is a description of {user2["name"]}:
	{agent2}

	Generate a message history between the two people. The dialogue should be a friendly conversation between two people who have just met.
	Don't copy from their profiles, but invent an original conversation that reflects their profiles but does not showcase them directly.

	Max. length: 10 turns.
	"""

	return mistral_service.ask_mistral(prompt)



def evaluate_dialogue(dialogue):

	prompt = f"""
	Here is a dialogue between two people who have just met:

	<begin dialogue>
	{dialogue}
	<end dialogue>

	We are evaluating the dialogue to decide if the two people will become a match.
	Return a JSON object with the following fields:
	- "Similarity": <very different, different, neutral, similar, very similar>
	- "Compatibility": <completely uncompatible, uncompatible, neutral, compatible, very compatible>
	- "Summary": <two-line summary of the evaluation>
	- "If these people were to have a first date, where or what should they do?": <suggestion>
	"""

	return mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" }
	)


