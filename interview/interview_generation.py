
# NOTE: 'Interviews' is our early-concept phrasing for "Wingman calls".
# 'Interviews' are live-generated conversations between the AI Wingman and the user.
# They are designed to gather information as well as being engaging and fun.

import sys
sys.path.append('..')

import mistral_service


def get_next_question(context_dialogue):

	# NOTE: Prompting is crucial to obtain quality results from generative models.
	# Later research would have to delve into best practices.
	# We would need to design a more sophisticated prompting pipeline to guarantee variety and originality.
	# Ideally, we would fine-tune the model.


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
	
	Reply with a new question that hasn't been asked yet.
	"""

	response = mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" },
		model = "ministral-3b-latest" # NOTE: We use a smaller model for real-time performance
	)

	return response