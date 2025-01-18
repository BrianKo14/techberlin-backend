
import sys
sys.path.append('..')

import mistral_service
import json
import os

from agents import data_retrieval


def get_transcript(filename):
	with open(filename, 'r') as f:
		transcript = f.read()

	return transcript



def format_transcript(transcript):

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<being transcript> 
	{transcript}
	<end transcript>

	Extract the following information from the transcript:
	- Name of the user.
	- Age of the user.
	- Which languages they speak.
	- A brief summary of their hobbies.

	Return the information in JSON format. Reply with the JSON object. That is, your response should being with a '{' and end with a '}'.
	
	Format fields template: 
		"Name": ?,
		"Age": ?,
		"Languages": [?, ?, ...]
		"Hobbies": <brief summary>
	"""

	response = mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" },
		model = "ministral-3b-latest"
	)

	return json.loads(response)



def generate_agent(transcript):

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<being transcript>
	{transcript}
	<end transcript>

	Generate a personality profile for an AI agent that will pretend to be the human in the call.
	Include in this profile general instructions on how the agent should behave, and an extensive description of the human.
	"""

	response = mistral_service.ask_mistral(prompt)

	return response



def update_agent(transcript, user_id):

	agent = data_retrieval.get_agent(user_id)

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<begin transcript>
	{transcript}
	<end transcript>

	Here is the current agent profile:

	{agent}

	Please update the agent profile to reflect the information in the transcript.
	"""

	return mistral_service.ask_mistral(prompt)


def digest_all_transcripts():
	agent = ""
	
	for filename in os.listdir("../data/user_transcripts"):
		transcript = get_transcript(f"../data/user_transcripts/{filename}")

		print(f"Digesting transcript {filename}...")

		if agent == "":
			agent = generate_agent(transcript)
		else:
			agent = update_agent(transcript, agent)

		print(f"Transcript {filename} digested.")

	save_agent(agent)

	
def save_agent(agent):
	with open("../data/profiles/user-agent.txt", 'w') as f:
		f.write(agent)
		