
import sys
sys.path.append('..')

import mistral_service
import json


dialogue_starter = str({
	"dialogue": [
		{
			"speaker": "AI",
			"text": "Hi there! I’m here to help set up your dating profile. Can I ask you a few questions?"
		}
	]
})



def get_next_question(context_dialogue):

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<begin transcript>
	{context_dialogue}
	<end transcript>

	Please generate the next question that the AI agent should ask. The question should be relevant to the context of the conversation.

	Here are some questions that needs to be answered:
	- What is your name?
	- What is your age?
	- What are your hobbies?
	- Describe yourself
	- What are you looking for in a partner?
	
	On top of that, generate random questions that are fun and engaging.

	Reply with a new question that hasn't been asked yet.
	"""

	response = mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" },
		model = "ministral-3b-latest"
	)

	return response